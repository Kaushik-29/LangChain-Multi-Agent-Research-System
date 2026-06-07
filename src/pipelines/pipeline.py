from concurrent.futures import ThreadPoolExecutor

from src.agents.agents import (
    planner_chain,
    writer_chain,
    critic_chain,
    rewrite_chain
)

from src.tools.tools import (
    search_multiple_queries,
    get_top_urls,
    scrape_url,
    format_search_results
)


def run_research_pipeline(topic: str):

    state = {}

    # ==========================================
    # STEP 1 - Planner
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 1 - Planning Research...")
    print("=" * 60)

    planner_output = planner_chain.invoke(
        {
            "topic": topic
        }
    )

    queries = [
        q.strip()
        for q in planner_output.split("\n")
        if q.strip()
    ]

    state["queries"] = queries

    print("\nGenerated Search Queries:\n")

    for q in queries:
        print(f"- {q}")

    # ==========================================
    # STEP 2 - Search
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 2 - Searching Web...")
    print("=" * 60)

    search_results = search_multiple_queries(
        queries
    )

    state["search_results"] = search_results

    print(
        f"\nFound {len(search_results)} search results"
    )

    # ==========================================
    # STEP 3 - Source Ranking
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 3 - Ranking Sources...")
    print("=" * 60)

    top_urls = get_top_urls(
        search_results,
        top_k=5
    )

    state["top_urls"] = top_urls

    print("\nSelected URLs:\n")

    for url in top_urls:
        print(url)

    # ==========================================
    # STEP 4 - Parallel Scraping
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 4 - Scraping Sources...")
    print("=" * 60)

    with ThreadPoolExecutor(
        max_workers=5
    ) as executor:

        scraped_contents = list(
            executor.map(
                scrape_url.invoke,
                top_urls
            )
        )

    articles = []

    for url, content in zip(
        top_urls,
        scraped_contents
    ):

        articles.append(
            {
                "url": url,
                "content": content
            }
        )

    state["articles"] = articles

    print(
        f"\nSuccessfully scraped "
        f"{len(articles)} articles"
    )

    # ==========================================
    # STEP 5 - Build Research Context
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 5 - Building Research Context...")
    print("=" * 60)

    search_text = format_search_results(
        search_results
    )

    article_text = ""

    for article in articles:

        article_text += f"""

SOURCE:
{article['url']}

CONTENT:
{article['content']}

--------------------------------------------------

"""

    research_context = f"""

SEARCH RESULTS

{search_text}


SCRAPED ARTICLES

{article_text}


IMPORTANT INSTRUCTIONS:

- Use only supplied information.
- Cite source URLs.
- Do not invent facts.
"""

    state["research_context"] = research_context

    # ==========================================
    # STEP 6 - Writer
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 6 - Writing Report...")
    print("=" * 60)

    draft_report = writer_chain.invoke(
        {
            "topic": topic,
            "research": research_context
        }
    )

    state["draft_report"] = draft_report

    print("\nDraft Report Generated")

    # ==========================================
    # STEP 7 - Critic
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 7 - Critic Reviewing...")
    print("=" * 60)

    feedback = critic_chain.invoke(
        {
            "report": draft_report
        }
    )

    state["feedback"] = feedback

    print("\nCritic Feedback:\n")
    print(feedback)

    # ==========================================
    # STEP 8 - Rewriter
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 8 - Improving Report...")
    print("=" * 60)

    final_report = rewrite_chain.invoke(
        {
            "report": draft_report,
            "feedback": feedback
        }
    )

    state["final_report"] = final_report

    print("\nFinal Report Generated")

    # ==========================================
    # Summary
    # ==========================================

    print("\n" + "=" * 60)
    print("RESEARCH PIPELINE COMPLETED")
    print("=" * 60)

    return state