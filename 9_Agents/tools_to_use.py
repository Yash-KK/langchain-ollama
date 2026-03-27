import os
import sys

_repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

from langchain.tools import tool  # noqa: E402
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper  # noqa: E402
from langchain_community.tools import DuckDuckGoSearchResults  # noqa: E402
from langchain_openai import ChatOpenAI  # noqa: E402
from helpers.common import langfuse_handler, TOGETHER_API_KEY  # noqa: E402


@tool
def web_search(query:str, max_results:int = 3) -> str:
  """Search the web using DuckDuckGo.
    
  Args:
    query: Search query string
    num_results: Number of results to return (default: 10)
    
  Returns:
    Formatted search results with titles, descriptions, and URLs
  """  

  wrapper = DuckDuckGoSearchAPIWrapper(region="us-en",time="d", max_results=max_results)
  search = DuckDuckGoSearchResults(api_wrapper=wrapper, output_format="list")
  response = search.invoke(query)

  return response


model_1 = "Qwen/Qwen3.5-9B"
model_2 = "OpenAI/gpt-oss-20B"

basic_model = ChatOpenAI(
  api_key=TOGETHER_API_KEY,
  model=model_1,
  base_url="https://api.together.xyz/v1",
  callbacks=[langfuse_handler]
)

advanced_model = ChatOpenAI(
  api_key=TOGETHER_API_KEY,
  model=model_2,
  base_url="https://api.together.xyz/v1",
  callbacks=[langfuse_handler]
)

