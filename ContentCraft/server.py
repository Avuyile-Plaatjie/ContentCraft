"""ContentCraft local web server and Ollama bridge. Python standard library only."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
import threading
import webbrowser

ROOT = Path(__file__).resolve().parent
HOST, PORT = "127.0.0.1", 8765
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, body):
        data = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            try:
                with urlopen("http://127.0.0.1:11434/api/tags", timeout=2) as response:
                    tags = json.loads(response.read().decode("utf-8"))
                models = [item.get("name", "") for item in tags.get("models", [])]
                self.send_json(200, {"ollama": True, "models": models})
            except Exception:
                self.send_json(200, {"ollama": False, "models": []})
            return
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        data = (ROOT / "index.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/generate":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 2 or length > 1_000_000:
                return self.send_json(400, {"error": "Please provide a prompt under 1 MB."})
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            model = str(payload.get("model", "qwen2.5-coder:1.5b")).strip()
            messages = payload.get("messages")
            if not model or not isinstance(messages, list) or not messages:
                return self.send_json(400, {"error": "Choose a model and enter a content brief."})
            body = json.dumps({"model": model, "messages": messages, "stream": False,
                               "options": {"temperature": 0.7}}).encode("utf-8")
            req = Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
            with urlopen(req, timeout=900) as response:
                result = json.loads(response.read().decode("utf-8"))
            text = result.get("message", {}).get("content", "").strip()
            if not text:
                return self.send_json(502, {"error": "The model returned an empty draft. Try again or choose another model."})
            self.send_json(200, {"text": text})
        except HTTPError as exc:
            try:
                details = json.loads(exc.read().decode("utf-8")).get("error", "")
            except Exception:
                details = ""
            message = details or ("Ollama could not find that model. Use Setup model.bat or choose an installed model." if exc.code == 404 else f"Ollama returned HTTP {exc.code}.")
            self.send_json(502, {"error": message})
        except URLError:
            self.send_json(503, {"error": "Ollama is not running. Install and start Ollama, then use Setup model.bat."})
        except TimeoutError:
            self.send_json(504, {"error": "The model took too long to respond. Try a smaller model or shorter brief."})
        except Exception as exc:
            self.send_json(500, {"error": f"Could not generate the draft: {exc}"})

    def log_message(self, *_args):
        pass


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}"
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    print(f"ContentCraft is running at {url}. Close this window to stop it.")
    print("Your prompts stay on this computer. The local Ollama model creates the drafts.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
