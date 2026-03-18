from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from helpers.common import ollama_llm, langfuse_handler


DB_PATH = "sqlite:///chat_history.db"  

system_message = SystemMessagePromptTemplate.from_template("You are a helpful assistant. You remember the conversation.")

human_message = HumanMessagePromptTemplate.from_template("{input}")
messages = [
  system_message,
  MessagesPlaceholder(variable_name="history", optional=True),
  human_message
]

chat_prompt = ChatPromptTemplate(messages)

chain = chat_prompt | ollama_llm



def get_session_history(session_id: str) -> SQLChatMessageHistory:
  return SQLChatMessageHistory(
    session_id=session_id,
    connection=DB_PATH
  )


chat = RunnableWithMessageHistory(
  chain,
  get_session_history,
  input_messages_key="input",
  history_messages_key="history"
)

def chat_with_memory(user_input: str, session_id: str = "default") -> str:

    for message in chat.stream({
      "input": user_input,
    },
    config={"configurable": {"session_id": session_id}, "callbacks": [langfuse_handler],"run_name": "Chat Bot",    "metadata": {"langfuse_tags": ["gemma-chatbot"]}}
    ):
      print(message.content, end="")


reply = chat_with_memory("Hi! My name is Yash Kharche.", session_id="session_1")
