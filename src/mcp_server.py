
import base64
import io
import uuid

from mcp.server.fastmcp import FastMCP

from prompt_chain import enhance_prompt
from image_gen import generate_image, save_image

mcp = FastMCP("imaginate")


@mcp.tool()
def generate_image_tool(idea: str) -> dict:
    """
    Generate an image from a rough text idea.

    Takes a short, casual description (e.g. "a cat astronaut"), expands it
    into a detailed image-generation prompt using an LLM, then generates
    an image from that prompt.

    Args:
        idea: A rough, casual description of the image to create.

    Returns:
        A dict with the enhanced prompt used and the saved file path.
    """
    enhanced = enhance_prompt(idea)
    image = generate_image(enhanced)

    filename = f"{uuid.uuid4().hex[:8]}.png"
    path = save_image(image, filename)

    return {
        "original_idea": idea,
        "enhanced_prompt": enhanced,
        "saved_path": path,
    }


if __name__ == "__main__":
    mcp.run()
