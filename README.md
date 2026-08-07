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
