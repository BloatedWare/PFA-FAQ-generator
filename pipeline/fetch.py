import requests

DEFAULT_HEADERS = {
    "User-Agent" : "Mozilla/5.0 (FAQ-Generator-PFA/1.0)"
}

def fetch_html(url: str, timeout: int = 15) -> str :
    """
    Downloads the HTML of a web page.
    - url: page URL
    - timeout: seconds before failing (in case site is too slow so it's not stuck forever)
    Returns: HTML content as string
    """
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.text

