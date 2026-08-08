"""
prompt_chain.py — LangChain LCEL chain that turns a rough idea into a
detailed, structured image-generation prompt using Gemini.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def get_api_key(key_name: str) -> str:
    """
    Reads an API key from Streamlit secrets (used on Streamlit Cloud)
    if available, otherwise falls back to a local .env file.
    """
    try:
        import streamlit as st
        if key_name in st.secrets:
            return st.secrets[key_name]
    except Exception:
        pass
    return os.getenv(key_name)

SYSTEM_INSTRUCTIONS = """You are an expert prompt engineer for text-to-image AI models.
Given a rough, casual idea from a user, expand it into a single, detailed image-generation
prompt. Include:
- Subject and action (what's happening)
- Art style (e.g. photorealistic, digital painting, anime, watercolor)
- Lighting and mood
- Camera angle / composition
- Extra descriptive detail (colors, textures, background)

Rules:
- Output ONLY the final prompt text. No explanations, no preamble, no quotes.
- Keep it to 1-3 sentences, dense with visual detail.
- Do not change the core subject the user asked for.
"""

_prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_INSTRUCTIONS),
    ("human", "{idea}"),
])


def build_chain():
    """Builds and returns the LCEL chain: prompt template -> Gemini -> string output."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        google_api_key=get_api_key("GOOGLE_API_KEY"),
        temperature=0.8,
    )
    # LCEL pipe syntax: each stage's output feeds into the next stage's input
    chain = _prompt_template | llm | StrOutputParser()
    return chain


def enhance_prompt(idea: str) -> str:
    """Takes a rough idea string, returns an enhanced, detailed image prompt."""
    chain = build_chain()
    result = chain.invoke({"idea": idea})
    return result.strip()


if __name__ == "__main__":
    # Quick manual test: python src/prompt_chain.py
    test_idea = "a cat astronaut"
    print("Rough idea:", test_idea)
    print("Enhanced prompt:", enhance_prompt(test_idea))