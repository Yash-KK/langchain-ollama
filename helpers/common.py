import os
from dotenv import load_dotenv
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langchain_openai import ChatOpenAI

load_dotenv()

GEMMA_MODEL = "gemma3:4b"
DEEPSEEK_MODEL = "deepseek-r1:1.5b"
QWEN_MODEL = "qwen2.5:7b"
NOMIC_EMBEDDING_MODEL = "nomic-embed-text:latest"

BASE_URL = "http://localhost:11434/"

TOGETHER_API_KEY= os.getenv('TOGETHER_API_KEY') 
langfuse = get_client()
langfuse_handler = CallbackHandler()


together_ai_llm = ChatOpenAI(
  api_key=TOGETHER_API_KEY,
  model="OpenAI/gpt-oss-20B",
  base_url="https://api.together.xyz/v1",
  callbacks=[langfuse_handler]
)