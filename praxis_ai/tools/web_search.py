# tools/web_search.py

import ell
from tavily import TavilyClient
from ..utils.logging import logger
from ..config.settings import TAVILY_API_KEY
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from functools import lru_cache
import time

console = Console()

@lru_cache(maxsize=100)
def cached_search(query: str, num_results: int, search_depth: str):
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    return tavily_client.search(
        query=query,
        max_results=num_results,
        search_depth=search_depth
    )

def format_search_results(results):
    table = Table(title="Search Results", show_header=True, header_style="bold magenta")
    table.add_column("Title", style="dim", width=30)
    table.add_column("URL", style="dim")
    table.add_column("Snippet", width=50)

    for result in results:
        table.add_row(
            result['title'],
            result['url'],
            result['snippet'][:100] + "..." if len(result['snippet']) > 100 else result['snippet']
        )

    return table

def summarize_results(results):
    summary = "Summary of search results:\n"
    for i, result in enumerate(results, 1):
        summary += f"{i}. {result['title']}\n"
    return summary

@ell.tool()
def web_search(query: str, num_results: int = 5, search_depth: str = "basic", retries: int = 3):
    """
    Perform a web search using the Tavily API and return formatted search results.
    
    Args:
    query (str): The search query.
    num_results (int): Number of results to return (default: 5).
    search_depth (str): Depth of search, 'basic' or 'advanced' (default: 'basic').
    retries (int): Number of retries in case of failure (default: 3).
    
    Returns:
    str: Formatted search results and summary.
    """
    for attempt in range(retries):
        try:
            start_time = time.time()
            response = cached_search(query, num_results, search_depth)
            end_time = time.time()

            results = [
                {
                    "title": result['title'],
                    "url": result['url'],
                    "snippet": result['content']
                }
                for result in response['results']
            ]

            table = format_search_results(results)
            summary = summarize_results(results)

            console.print(Panel(table, title=f"Web Search Results for: {query}", expand=False))
            console.print(f"Search completed in {end_time - start_time:.2f} seconds.")

            return f"{summary}\n\nDetailed results:\n{table}"

        except Exception as e:
            if attempt < retries - 1:
                logger.warning(f"Search attempt {attempt + 1} failed. Retrying... Error: {str(e)}")
                time.sleep(1)  # Wait for 1 second before retrying
            else:
                error_message = f"Error performing web search after {retries} attempts: {str(e)}"
                logger.error(error_message)
                return error_message

    return "Web search failed after multiple attempts."