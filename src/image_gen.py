"""
image_gen.py — Calls the Hugging Face Inference API to generate an image
from a text prompt using a Stable Diffusion model.
"""

import os
import io
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image

load_dotenv()

# Free-tier friendly model. Swap for another text-to-image model on HF if you like.
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"


def get_client() -> InferenceClient:
    return InferenceClient(model=MODEL_ID, token=os.getenv("HF_API_KEY"))


def generate_image(prompt: str) -> Image.Image:
    """Generates an image from a text prompt. Returns a PIL Image."""
    client = get_client()
    image = client.text_to_image(prompt)
    return image


def save_image(image: Image.Image, filename: str) -> str:
    """Saves a PIL image into outputs/ and returns the file path."""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    image.save(path)
    return path


if __name__ == "__main__":
    # Quick manual test: python src/image_gen.py
    test_prompt = "a photorealistic cat astronaut floating in space, cinematic lighting"
    print("Generating image for:", test_prompt)
    img = generate_image(test_prompt)
    path = save_image(img, "test_output.png")
    print("Saved to:", path)
