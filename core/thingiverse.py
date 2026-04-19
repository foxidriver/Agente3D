import requests
import os
from typing import Optional

def search_models(query: str, result_count: Optional[int] = None) -> str:
    """
    Searches for 3D models on Thingiverse and returns formatted results.

    Args:
        query (str): Search term for 3D models.
        result_count (int, optional): Number of results to return. Uses THINGIVERSE_DEFAULT_RESULTS if not provided.

    Returns:
        str: Formatted string with search results or error message.
    """
    token = os.getenv("THINGIVERSE_TOKEN")
    if not token:
        return "Error: Thingiverse token not configured in environment variables."

    # Use default from .env if not provided
    if result_count is None:
        result_count = int(os.getenv("THINGIVERSE_DEFAULT_RESULTS", "5"))

    url = f"https://api.thingiverse.com/search/{query}"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"per_page": result_count}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()
    except requests.exceptions.RequestException as error:
        return f"Error fetching data from Thingiverse: {str(error)}"

    hits = results.get("hits", [])
    if not hits:
        return "No models found."

    output_text = ""
    for model in hits[:result_count]:
        name = model.get("name", "N/A")
        creator = model.get("creator", {}).get("name", "N/A")
        model_url = model.get("public_url", "N/A")
        like_count = model.get("like_count", 0)
        output_text += f"- **{name}** by {creator} | ❤️ {like_count} | [Link]({model_url})\n"

    return output_text