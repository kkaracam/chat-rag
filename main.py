#from langchain.chat_models.openai import ChatOpenAI
from langchain_openai import ChatOpenAI
#from langchain.chains.llm import LLMChain
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser


from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(temperature=0)
search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="intermediate_answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]
chat_with_tools = chat.bind_tools(tools)

memory = ConversationBufferMemory(
    chat_memory=FileChatMessageHistory("chat_history.json"),
    memory_key="chat_history",
    return_messages=True
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but don't know current events." 
            "When asked about current events, search for answers using provided tools.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | chat_with_tools
    | OpenAIToolsAgentOutputParser()
)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

while True:
    content = input(">> ")
    # print(content)
    result = agent_executor.invoke({"input":content})

    print(result["output"])
