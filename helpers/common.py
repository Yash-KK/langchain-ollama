from dotenv import load_dotenv
from langfuse import get_client
from langfuse.langchain import CallbackHandler

load_dotenv()

GEMMA_MODEL = "gemma3:4b"
DEEPSEEK_MODEL = "deepseek-r1:1.5b"
QWEN_MODEL = "qwen2.5:7b"
NOMIC_EMBEDDING_MODEL = "nomic-embed-text:latest"

BASE_URL = "http://localhost:11434/"

langfuse = get_client()
langfuse_handler = CallbackHandler()
