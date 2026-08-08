# Imaginate

Turn a rough idea into a generated image — a LangChain prompt-enhancement chain
expands your casual description into a detailed image prompt, which is then sent
to a text-to-image model. Also exposed as an **MCP tool**, so any MCP-compatible
AI agent (e.g. Claude Desktop) can call it directly.

## How it works

```
User idea ("a cat astronaut")
        │
        ▼
  LangChain LCEL chain (Gemini)   →  expands into a detailed, styled prompt
        │
        ▼
  Hugging Face Inference API      →  generates the actual image
        │
        ▼
  Streamlit UI  /  MCP tool call  →  shown to the user or returned to the agent
```

## Project Structure

```
imaginate/
├── src/
│   ├── prompt_chain.py     # LangChain LCEL: rough idea -> detailed prompt
│   ├── image_gen.py        # Hugging Face Inference API call
│   └── mcp_server.py       # Exposes generate_image_tool as an MCP tool
├── app/
│   └── streamlit_app.py    # UI
├── outputs/                 # generated images land here
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your keys:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   HF_API_KEY=your_huggingface_token
   ```
   - Gemini key: https://aistudio.google.com/app/apikey
   - Hugging Face token: https://huggingface.co/settings/tokens

## Run the Streamlit app

```bash
streamlit run app/streamlit_app.py
```

## Run as an MCP server

```bash
python src/mcp_server.py
```

To connect this to Claude Desktop, add this to your Claude Desktop MCP config
(`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "imaginate": {
      "command": "python",
      "args": ["/absolute/path/to/imaginate/src/mcp_server.py"]
    }
  }
}
```

Restart Claude Desktop, and you'll be able to ask it to generate an image using
the `imaginate` tool directly.

## Author

Vansh
[LinkedIn](https://www.linkedin.com/in/vansh-983217253/) |
[GitHub](https://github.com/vanshgurawalia) |
[LeetCode](https://leetcode.com/u/vanshh10/)
