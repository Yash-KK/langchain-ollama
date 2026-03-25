from langchain.tools import tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults



@tool
def web_search(query:str, max_results:int = 5) -> str:
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
