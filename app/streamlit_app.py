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

st.set_page_config(page_title="Imaginate", page_icon="✨", layout="centered")

st.title("✨ Imaginate")
st.caption("Rough idea → AI-enhanced prompt → generated image")

idea = st.text_input("What do you want to see?", placeholder="e.g. a cat astronaut")

if st.button("Generate", type="primary") and idea.strip():
    with st.spinner("Enhancing your prompt..."):
        try:
            enhanced = enhance_prompt(idea)
        except Exception as e:
            st.error(f"Prompt enhancement failed: {e}")
            st.stop()

    st.markdown("**Enhanced prompt:**")
    st.info(enhanced)

    with st.spinner("Generating image... this can take 10-30 seconds"):
        try:
            image = generate_image(enhanced)
        except Exception as e:
            st.error(f"Image generation failed: {e}")
            st.stop()

    st.image(image, caption=idea, use_container_width=True)

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    st.download_button("Download image", data=buf.getvalue(),
                        file_name="imaginate_output.png", mime="image/png")

st.markdown("---")
st.caption("Built by Vansh · LangChain + Gemini + Hugging Face + MCP")
