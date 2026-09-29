# ContentCraft — Local AI Content Generator

This is a working source-code project for generating blogs, emails, social posts, meeting summaries, and code with a real language model running locally through Ollama. It is a small Python web server with a colorful HTML/JavaScript interface. **It is not a Streamlit app.** It needs no API key and makes no cloud AI calls.

## Windows quick start

1. Install Python 3 if it is not already installed: <https://www.python.org/downloads/windows/>. No Python packages need to be installed.
2. Install Ollama: <https://ollama.com/download/windows>.
3. Extract this ZIP, then double-click **Setup model.bat**. This downloads `qwen2.5-coder:1.5b` (about 1 GB), the local model used for content and code generation. This is a one-time download.
4. Double-click **run_windows.bat**. It starts the local web app and opens it in your browser.
5. Choose a prompt, enter your brief, and click **Generate with AI**. For code, choose **Generate code**, **Debug or improve code**, or **Explain code**. Generated code can be downloaded with its file extension (such as `.py`, `.js`, or `.html`).

Keep the black server window open while using the app. Close that window to stop the server. The app shows a clear status message if Ollama or the model is missing. The downloaded model runs on your computer; generation speed depends on your computer's memory and processor/GPU. You may change the model name in the app to any model installed in Ollama.

## Prompt library

12 starter prompts with category filters and search: blog article, how-to guide, email newsletter, promotional email, outreach email, social post, LinkedIn post, social captions, code generation, code debugging, code explanation, and meeting summary. Prompts specify the requested task; the brief also includes audience, tone, length, output language, and extra instructions.

## Project files

- `server.py` — Python local web server and private bridge to Ollama's local API
- `index.html` — colorful UI, prompt library, and browser-side controls
- `run_windows.bat` — starts the app and opens the browser
- `Setup model.bat` — downloads the default Ollama model
- `requirements.txt` — documents that there are no pip dependencies

The server listens only on `127.0.0.1` (your own computer). Your prompt is sent to the local Ollama service at `127.0.0.1:11434`, not to a hosted AI provider. The project contains no API keys.
