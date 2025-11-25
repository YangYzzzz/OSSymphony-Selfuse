import requests
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple
from requests.auth import HTTPBasicAuth

class PastSearcherAgent:
    """
    Abstract base class for search agents.
    Defines a common interface that all search agents must adhere to.
    """
    def __init__(self, search_api: str, search_top_k: int, search_enable_reranker: bool, search_reranker_api: str):
        if not search_api or (search_enable_reranker and not search_reranker_api):
            raise ValueError("The 'search_api' or 'search_reranker_api' is missing from the 'engine_params' configuration.")
        
        self.search_api = search_api
        self.search_top_k = search_top_k
        self.search_enable_reranker = search_enable_reranker
        self.search_reranker_api = search_reranker_api

    def search(self, query: str) -> str:
        """
        Executes a search based on the given query and returns a formatted result string.
        This is a virtual method that subclasses must implement.
        """
        raise NotImplementedError("Subclasses must implement the 'search' method")

    def rerank(self, query, documents):
        data = {
            "query": query,
            "documents": documents
        }
        response = requests.post(
            url=self.search_reranker_api, 
            json=data, 
            auth=HTTPBasicAuth("5ad34100ee055a4bae66370a5e683bac", "607de8249657a3b3bd036dc96d4c0b2f"))
        return response.json()


    def organize(self, query: str, results: List) -> str:
        """
        A unified interface to organize and format search results.

        Args:
            query (str): The original search query.
            results (List): A list of result dictionaries from the search API.

        Returns:
            str: A formatted string containing the top search results.
        """
        if not results:
            return f"No search results found for '{query}'."

        if self.search_enable_reranker:
            documents = []
            reverse_dict = {}
            for i, r in enumerate(results):
                title = r.get("title", "No Title")
                description = r.get("description", r.get("content", "No Description")).strip()
                reverse_dict[title + description] = i
                documents.append(title + description)
            # List[Dict] {"relevance_score": xxx, "document": xxx}
            rerank_response = self.rerank(query=query, documents=documents)[:self.search_top_k]
            top_results = []
            for res in rerank_response:
                top_results.append(reverse_dict[res['document']])
            result_parts: List[str] = [f'The reranked search results for "{query}"(sorted by relevance):\n']
        else:
            top_results: List[Dict[str, str]] = results[:self.search_top_k]
            result_parts: List[str] = [f'Search results for "{query}":\n']
            
        for i, result in enumerate(top_results, 1):
            title = result.get("title", "No Title")
            url = result.get("url", "No URL")
            # Use 'description' if available, otherwise fall back to 'content', then a default message.
            description = result.get("description", result.get("content", "No Description")).strip()

            result_block = (
                f"[Result {i}]\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Description: {description}\n"
            )
            result_parts.append(result_block)

        return "\n".join(result_parts)
    
    @staticmethod
    def create(engine_params: dict) -> 'PastSearcherAgent':
        """
        Factory method to create and return a concrete search agent instance
        based on the provided parameters.
        """
        if engine_params.get("searcher_type", "searxng") == "searxng":
            return SearcherAgentSearXNG(engine_params=engine_params)
        else:
            return SearcherAgentJinaAI(engine_params=engine_params)

# --- JinaAI Search Agent Implementation ---

class SearcherAgentJinaAI(PastSearcherAgent):
    """
    A search agent that uses the Jina AI Search API (s.jina.ai).
    """
    def __init__(self, engine_params: dict) -> None:
        """
        Initializes the JinaAI search agent.

        Args:
            engine_params (dict): A dictionary containing search engine configurations.
                Required keys:
                - "search_api_key" (str): The Jina AI API key for authentication.
                Optional keys:
                - "search_top_k" (int): The number of results to return, defaults to 10.
        """
        super().__init__(
            search_api="https://s.jina.ai/",
            search_top_k=engine_params.get("search_top_k", 10), 
            search_enable_reranker=engine_params.get("search_enable_reranker", False),
            search_reranker_api=engine_params.get("search_reranker_api", "")
        )
        
        self.search_api_key = engine_params.get("search_api_key")
        if not self.search_api_key:
            raise ValueError("The 'search_api_key' is missing from the 'engine_params' configuration.")
        
        self.search_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.search_api_key}",
        }

    def search(self, query: str) -> str:
        """
        Performs a search using Jina AI.
        
        Args:
            query (str): The search query string.

        Returns:
            str: The formatted search results from the API, or an error message.
        """
        # URL-encode the query. `quote_plus` encodes spaces as '+'.
        encoded_query = urllib.parse.quote_plus(query)
        
        # Jina AI expects the query to be part of the URL path.
        url = f"{self.search_api}{encoded_query}"
        
        try:
            response = requests.get(url, headers=self.search_headers, timeout=15)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            results = response.json().get("data", [])
            return self.organize(query=query, results=results)

        except requests.exceptions.RequestException as e:
            return f"Error: Jina AI search request failed. Details: {e}"

class SearcherAgentSearXNG(PastSearcherAgent):
    """
    A search agent that uses a SearXNG instance as its backend.
    """
    def __init__(self, engine_params: dict) -> None:
        """
        Initializes the SearXNG search agent.

        Args:
            engine_params (dict): A dictionary containing search engine configurations.
                Required keys:
                - "search_api" (str): The API endpoint URL of the SearXNG instance.
                Optional keys:
                - "search_engine" (str): The search engines to use, defaults to "google".
                - "search_top_k" (int): The number of results to return, defaults to 10.
        """
        super().__init__(
            search_api=engine_params.get("search_api", ""),
            search_top_k=engine_params.get("search_top_k", 10),
            search_enable_reranker=engine_params.get("search_enable_reranker", False),
            search_reranker_api=engine_params.get("search_reranker_api", "")
        )
        self.search_engines: str = engine_params.get("search_engine", "google")
        self.headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }

    def search(self, query: str) -> str:
        """
        Performs a search and returns a formatted string optimized for Large Language Models (LLMs).

        Args:
            query (str): The search query string.

        Returns:
            str: A formatted string containing the search results, or an error/status message.
        """
        # [BEST PRACTICE] The requests library automatically handles URL encoding for the params dictionary.
        params = {
            "q": query,
            "format": "json",
            "engines": self.search_engines
        }

        try:
            response = requests.get(url=self.search_api, params=params, headers=self.headers, timeout=15)
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return f"Error: SearXNG search request failed. Details: {e}"

        try:
            data: Dict[str, Any] = response.json()
        except requests.exceptions.JSONDecodeError:
            return f"Error: Failed to decode JSON from search engine response. Response text: {response.text[:200]}"

        results = data.get("results", [])
        return self.organize(query=query, results=results)

# --- Test Functions ---

def searxng_test():
    """Function to test the SearXNG search agent."""
    # The port should match the port exposed by the running SearXNG Docker container.
    url = "http://127.0.0.1:8999/search"

    # Search parameters
    params = {
        "q": "How to get OpenAI",
        "format": "json",
        "engines": "chrome"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    # Make a GET request
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        print("--- SearXNG Test ---")
        print(data)
        print("\nNumber of search results:", len(data.get("results", [])))
        for i, result in enumerate(data.get("results", []), start=1):
            print(f"{i}. {result.get('title')}")
            print(f"   {result.get('url')}")
            print(f"   {result.get('content')}")
    else:
        print(f"SearXNG test failed with status code: {response.status_code}")

def jina_search_test():
    """Function to test the Jina AI search agent."""
    # [SECURITY BEST PRACTICE] Avoid hardcoding API keys.
    # It's better to load them from environment variables or a secure config file.
    # Example: import os; api_key = os.getenv("JINA_API_KEY")
    engine_params = {
        "search_type": "jina_ai",
        "search_api_key": "jina_1fcf08bf8acc48e583c182c814333614txS2oROhmHe-4SMKeuHWtkVe8WP4",  # <-- Replace with your actual Jina AI key
        "search_top_k": 5
    }

    print("--- Jina AI Test ---")
    if "YOUR_API_KEY_HERE" in engine_params["search_api_key"]:
        print("Please replace 'jina_...YOUR_API_KEY_HERE...' with your actual Jina AI API key to run this test.")
        return

    search_agent = SearcherAgent.create(engine_params=engine_params)
    results = search_agent.search("How to create a webpage shortcut using Chrome on the desktop?")
    print(results)


if __name__ == "__main__":
    # jina_search_test()
    print("\n" + "="*50 + "\n")
    # You can uncomment the line below to test SearXNG if you have an instance running.
    searxng_test()
