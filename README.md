# Chatbot with RAG and Conversation Memory

A Chatbot application can search the web for information and incorporate the retrieved information when generating an answer. 
This enables the chatbot to be aware of current events and up-to-date information.
The application also stores the chat history as a JSON file so the information can persist and be referred to by the chatbot during each session.

## Requirements
* OpenAI API Key
* Serper API Key
* Python Version 3.11

## Usage
1. Create a virtual environment using the provided `requirements.txt` file.
2. Inside the working directory, create a `.env` file and save the API keys inside:
  ```
  OPENAI_API_KEY=...
  SERPER_API_KEY=...
  ```
3. Run `python main.py`
4. Enjoy your chat!
