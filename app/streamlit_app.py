"""
Imaginate — Streamlit UI
Run with: streamlit run app/streamlit_app.py
"""

import sys
import os
import io

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import streamlit as st
from prompt_chain import enhance_prompt
from image_gen import generate_image

st.set_page_config(page_title="Imaginate", page_icon="✨", layout="wide")

# ---------------------------------------------------------------------------
# Theming: dark canvas, purple/pink gradient accent, glass panel
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg: #060606;
    --panel: rgba(255,255,255,0.045);
    --panel-border: rgba(255,255,255,0.14);
    --text: #f5f5f5;
    --muted: #8a8a8a;
    --accent1: #ffffff;
    --accent2: #d4d4d4;
}

.stApp {
    background:
        radial-gradient(ellipse 900px 600px at 15% -5%, rgba(255,255,255,0.06), transparent 60%),
        radial-gradient(ellipse 800px 600px at 90% 10%, rgba(255,255,255,0.04), transparent 60%),
        radial-gradient(ellipse 1000px 700px at 50% 110%, rgba(0,0,0,0.6), transparent),
        linear-gradient(180deg, #060606 0%, #0a0a0a 100%);
}

html, body, [class*="css"] { color: var(--text); font-family: 'Inter', sans-serif; }

h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; }

.imaginate-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2.6rem;
    color: #ffffff;
    text-shadow: 0 0 30px rgba(255,255,255,0.25);
    margin-bottom: 0;
}
.imaginate-subtitle {
    font-family: 'Inter', sans-serif;
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0;
    margin-bottom: 2rem;
}

/* Glass panels */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--panel);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--panel-border) !important;
    border-radius: 16px !important;
    padding: 4px;
}

/* Text input */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid var(--panel-border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    padding: 0.7rem 1rem !important;
    font-size: 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #ffffff !important;
    box-shadow: 0 0 0 1px #ffffff !important;
}

/* Buttons */
.stButton button {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1.4rem;
}
.stButton button[kind="primary"] {
    background: #ffffff;
    color: #060606;
    box-shadow: 0 8px 24px rgba(255,255,255,0.18);
}
.stButton button[kind="primary"]:hover {
    box-shadow: 0 8px 32px rgba(255,255,255,0.32);
    transform: translateY(-1px);
}
.stButton button[kind="secondary"] {
    background: rgba(255,255,255,0.06);
    color: var(--text);
    border: 1px solid var(--panel-border);
}
.stButton button[kind="secondary"]:hover {
    border-color: #ffffff;
    color: #ffffff;
}

/* Enhanced prompt chip */
.prompt-chip {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.9rem;
    color: #e8e8e8;
    line-height: 1.5;
}
.section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.8rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}

/* Generated image container */
[data-testid="stImage"] img {
    border-radius: 14px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="imaginate-title">✨ Imaginate</div>', unsafe_allow_html=True)
st.markdown('<p class="imaginate-subtitle">Rough idea → AI-enhanced prompt → generated image</p>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Example prompt chips
# ---------------------------------------------------------------------------
examples = ["a cat astronaut", "cyberpunk city at night", "a dragon made of glass", "cozy cabin in snow"]

if "idea_input" not in st.session_state:
    st.session_state.idea_input = ""

ex_cols = st.columns(len(examples))
for col, ex in zip(ex_cols, examples):
    with col:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state.idea_input = ex

# ---------------------------------------------------------------------------
# Main layout: input/prompt on left, image on right
# ---------------------------------------------------------------------------
left, right = st.columns([1, 1.2], gap="large")

with left:
    with st.container(border=True):
        st.markdown('<div class="section-label">What do you want to see?</div>', unsafe_allow_html=True)
        idea = st.text_input("idea", value=st.session_state.idea_input,
                              placeholder="e.g. a cat astronaut", label_visibility="collapsed")
        generate_clicked = st.button("Generate ✨", type="primary", use_container_width=True)

    enhanced_placeholder = st.empty()

with right:
    image_placeholder = st.empty()
    download_placeholder = st.empty()

if generate_clicked and idea.strip():
    with left:
        with st.spinner("Enhancing your prompt..."):
            try:
                enhanced = enhance_prompt(idea)
            except Exception as e:
                st.error(f"Prompt enhancement failed: {e}")
                st.stop()

        enhanced_placeholder.markdown(
            f'<div class="section-label" style="margin-top:1.2rem;">Enhanced Prompt</div>'
            f'<div class="prompt-chip">{enhanced}</div>',
            unsafe_allow_html=True
        )

    with right:
        with st.spinner("Generating image... this can take 10-30 seconds"):
            try:
                image = generate_image(enhanced)
            except Exception as e:
                st.error(f"Image generation failed: {e}")
                st.stop()

        image_placeholder.image(image, use_container_width=True)

        buf = io.BytesIO()
        image.save(buf, format="PNG")
        download_placeholder.download_button(
            "Download image", data=buf.getvalue(),
            file_name="imaginate_output.png", mime="image/png",
            use_container_width=True
        )

st.markdown(
    '<div style="margin-top:3rem; padding-top:1.2rem; border-top:1px solid rgba(255,255,255,0.08); '
    'color:#9a95ad; font-size:0.8rem;">Built by Vansh · LangChain + Gemini + Hugging Face + MCP</div>',
    unsafe_allow_html=True
)