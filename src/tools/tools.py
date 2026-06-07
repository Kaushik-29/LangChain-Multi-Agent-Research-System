from langchain.tools import tool

import os
import re
import requests
import trafilatura

from dotenv import load_dotenv
from tavily import TavilyClient

from readability import Document
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

# ==========================================
# Tavily Client
# ==========================================

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

# ==========================================
# High Quality Domains
# ==========================================

HIGH_QUALITY_DOMAINS = {
    "reuters.com": 5,
    "wsj.com": 5,
    "mckinsey.com": 5,
    "nature.com": 5,
    "arxiv.org": 5,
    "ieee.org": 5,
    "forbes.com": 4,
    "gartner.com": 4,
    "mit.edu": 5,
    "stanford.edu": 5,
    "openai.com": 4,
    "anthropic.com": 4,
}

# ==========================================
# Search Tool
# ==========================================

@tool
def web_search(query: str):
    """
    Search the web and return structured results.
    """

    results = tavily.search(
        query=query,
        max_results=5
    )

    output = []

    for r in results["results"]:
        output.append(
            {
                "title": r["title"],
                "url": r["url"],
                "snippet": r["content"]
            }
        )

    return output


# ==========================================
# URL Cleaner
# ==========================================

def clean_url(url: str):

    if not url:
        return ""

    url = url.strip()

    url = url.rstrip(
        ".,);:*]}>"
    )

    return url


# ==========================================
# Domain Extractor
# ==========================================

def get_domain(url: str):

    try:
        return urlparse(url).netloc.replace(
            "www.",
            ""
        )
    except:
        return ""


# ==========================================
# Source Ranking
# ==========================================

def rank_sources(search_results):

    ranked = []

    for item in search_results:

        url = clean_url(
            item["url"]
        )

        domain = get_domain(url)

        score = 1

        if domain in HIGH_QUALITY_DOMAINS:
            score += HIGH_QUALITY_DOMAINS[
                domain
            ]

        if "linkedin" in domain:
            score -= 1

        if "blog" in domain:
            score -= 1

        ranked.append(
            {
                **item,
                "score": score
            }
        )

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked


# ==========================================
# Scraper Tool
# ==========================================

@tool
def scrape_url(url: str):
    """
    Scrape and extract clean readable content
    from a URL using multiple strategies.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        html = response.text

        # =====================================
        # Strategy 1 - Trafilatura
        # =====================================

        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False
        )

        if extracted:

            extracted = re.sub(
                r"\s+",
                " ",
                extracted
            )

            if len(extracted) > 200:
                return extracted[:6000]

        # =====================================
        # Strategy 2 - Readability
        # =====================================

        doc = Document(html)

        clean_html = doc.summary()

        soup = BeautifulSoup(
            clean_html,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        if len(text) > 200:
            return text[:6000]

        # =====================================
        # Strategy 3 - Full Page Fallback
        # =====================================

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text[:6000]

    except requests.exceptions.Timeout:

        return (
            f"Request timed out while "
            f"scraping: {url}"
        )

    except requests.exceptions.HTTPError as e:

        return (
            f"HTTP Error while scraping "
            f"{url}: {str(e)}"
        )

    except Exception as e:

        return (
            f"Failed to scrape "
            f"{url}\n\n{str(e)}"
        )


# ==========================================
# Multiple Query Search
# ==========================================

def search_multiple_queries(queries):
    """
    Run multiple Tavily searches
    generated by the Planner Agent.
    """

    all_results = []

    for query in queries:

        try:

            results = web_search.invoke(
                query
            )

            all_results.extend(
                results
            )

        except Exception as e:

            print(
                f"Search failed for "
                f"query '{query}': {e}"
            )

    return all_results


# ==========================================
# Get Top Ranked URLs
# ==========================================

def get_top_urls(
    search_results,
    top_k=5
):
    """
    Rank all search results and
    return the top URLs.
    """

    ranked = rank_sources(
        search_results
    )

    urls = []

    for item in ranked[:top_k]:

        urls.append(
            item["url"]
        )

    return urls


# ==========================================
# Format Search Results
# ==========================================

def format_search_results(
    search_results
):
    """
    Convert structured results
    into readable text.
    """

    formatted = []

    for item in search_results:

        formatted.append(
            f"""
Title: {item['title']}

URL: {item['url']}

Snippet:
{item['snippet']}
"""
        )

    return "\n\n".join(formatted)