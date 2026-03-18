from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

import os
import sys
import streamlit as st

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.common import ollama_llm, langfuse_handler



DB_PATH = "sqlite:///chat_history.db"  
def get_session_history(session_id: str) -> SQLChatMessageHistory:
  return SQLChatMessageHistory(
    session_id=session_id,
    connection=DB_PATH
  )

def chat_with_memory(user_input: str, session_id: str = "default") -> str:

    for message in chat.stream({
      "input": user_input,
    },
    config={"configurable": {"session_id": session_id}, "callbacks": [langfuse_handler],"run_name": "Chat Bot",    "metadata": {"langfuse_tags": ["gemma-chatbot"]}}
    ):
      yield message

system_message = SystemMessagePromptTemplate.from_template("You are a helpful assistant. You remember the conversation.")
human_message = HumanMessagePromptTemplate.from_template("{input}")
messages = [
  system_message,
  MessagesPlaceholder(variable_name="history", optional=True),
  human_message
]
chat_prompt = ChatPromptTemplate(messages)
chain = chat_prompt | ollama_llm

chat = RunnableWithMessageHistory(
  chain,
  get_session_history,
  input_messages_key="input",
  history_messages_key="history"
)

session_id = "yash"

## STREAMLIT CODE
st.title("Chatbot")
st.title("Chat with Ollama Model")

if "chat_history" not  in st.session_state:
  st.session_state.chat_history = []

if st.button("Start a Convo"):
  st.session_state.chat_history = []
  history = get_session_history(session_id)
  history.messages.clear()

for message in st.session_state.chat_history:
  with st.chat_message(message['role']):
    st.markdown(message['content'])

user_input = st.chat_input("What is up?")

if user_input:
  st.session_state.chat_history.append({
    "role": "user",
    "content": user_input
  })

  with st.chat_message("user"):
    st.markdown(user_input)

  with st.chat_message("assistant"):
    response = st.write_stream(chat_with_memory(user_input, session_id))

  st.session_state.chat_history.append({
    "role": "assistant",
    "content": response
  })