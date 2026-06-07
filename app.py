import streamlit as st

from src.pipelines.pipeline import (
    run_research_pipeline
)

# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide"
)

# ==========================================
# Header
# ==========================================

st.title("🔎 Multi-Agent Research System")

st.markdown(
    """
Generate detailed research reports using:

- Planner Agent
- Web Search
- Source Ranking
- Parallel Scraping
- Writer Agent
- Critic Agent
- Rewriter Agent
"""
)

# ==========================================
# Topic Input
# ==========================================

topic = st.text_input(
    "Enter Research Topic",
    placeholder="Example: Impact of AI on Software Development"
)

# ==========================================
# Run Pipeline
# ==========================================

if st.button("🚀 Generate Report"):

    if not topic.strip():

        st.warning(
            "Please enter a research topic."
        )

    else:

        with st.spinner(
            "Running Multi-Agent Research Pipeline..."
        ):

            result = run_research_pipeline(
                topic
            )

        st.success(
            "Research Completed!"
        )

        # ======================================
        # Tabs
        # ======================================

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📄 Final Report",
                "📝 Critic Feedback",
                "🔗 Sources",
                "🔍 Search Queries"
            ]
        )

        # ======================================
        # Report
        # ======================================

        with tab1:

            st.markdown(
                result["final_report"]
            )

            st.download_button(
                label="⬇ Download Report",
                data=result["final_report"],
                file_name="research_report.md",
                mime="text/markdown"
            )

        # ======================================
        # Feedback
        # ======================================

        with tab2:

            st.text_area(
                "Critic Feedback",
                value=result["feedback"],
                height=400
            )

        # ======================================
        # Sources
        # ======================================

        with tab3:

            for url in result["top_urls"]:

                st.markdown(
                    f"- {url}"
                )

        # ======================================
        # Queries
        # ======================================

        with tab4:

            for query in result["queries"]:

                st.markdown(
                    f"- {query}"
                )