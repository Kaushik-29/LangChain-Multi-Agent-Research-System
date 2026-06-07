from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ==========================================
# Gemini Model
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# ==========================================
# Planner Chain
# ==========================================

planner_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a professional research planner.

Your job is to generate multiple search queries
that will help gather high-quality information
about a topic.

Return exactly 5 search queries.

One query per line.
No numbering.
No explanations.
"""
    ),
    (
        "human",
        """
Research Topic:

{topic}
"""
    )
])

planner_chain = planner_prompt | llm | StrOutputParser()

# ==========================================
# Writer Chain
# ==========================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a senior research analyst.

Rules:

- Use ONLY provided research.
- Do NOT invent facts.
- Cite source URLs whenever possible.
- Be detailed and professional.
- Explain findings clearly.
"""
    ),
    (
        "human",
        """
Topic:
{topic}

Research Material:
{research}

Create a detailed report.

Structure:

# Introduction

# Methodology

Explain how the information was collected.

# Key Findings

At least 3 major findings.

Include citations:

(Source: URL)

# Conclusion

# Sources

List all URLs used.
"""
    )
])

writer_chain = writer_prompt | llm | StrOutputParser()

# ==========================================
# Critic Chain
# ==========================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a strict research reviewer.

Evaluate:

- Accuracy
- Research depth
- Citations
- Structure
- Clarity

Be constructive.
"""
    ),
    (
        "human",
        """
Review this report.

Report:

{report}

Respond exactly in this format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...
"""
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()

# ==========================================
# Rewriter Chain
# ==========================================

rewrite_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a senior editor.

Improve the report using critic feedback.

Fix:
- Missing citations
- Weak explanations
- Poor structure
- Missing methodology
- Missing details

Return ONLY the improved report.
"""
    ),
    (
        "human",
        """
Original Report:

{report}

Critic Feedback:

{feedback}
"""
    )
])

rewrite_chain = rewrite_prompt | llm | StrOutputParser()