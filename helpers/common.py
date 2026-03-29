import os
from dotenv import load_dotenv
from langfuse import get_client
from langchain_tavily import TavilySearch
from langfuse.langchain import CallbackHandler
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

load_dotenv()

GEMMA_MODEL = "gemma3:4b"
DEEPSEEK_MODEL = "deepseek-r1:1.5b"
QWEN_MODEL = "qwen2.5:7b"
NOMIC_EMBEDDING_MODEL = "nomic-embed-text:latest"

BASE_URL = "http://localhost:11434/"

TOGETHER_API_KEY= os.getenv('TOGETHER_API_KEY')
TAVILY_SEARCH_API_KEY= os.getenv("TAVILY_SEARCH_API_KEY")

langfuse = get_client()
langfuse_handler = CallbackHandler()

ollama_llm = ChatOllama(
  model=GEMMA_MODEL,
  base_url=BASE_URL,
  validate_model_on_init=False
)

model_1 = "OpenAI/gpt-oss-20B"
model_2 = "Qwen/Qwen3.5-9B"
together_ai_llm = ChatOpenAI(
  api_key=TOGETHER_API_KEY,
  model=model_1,
  base_url="https://api.together.xyz/v1",
  callbacks=[langfuse_handler],
  temperature=0
)


tavily_search = TavilySearch(
    max_results=3,
    topic="general",
    tavily_api_key=TAVILY_SEARCH_API_KEY
)