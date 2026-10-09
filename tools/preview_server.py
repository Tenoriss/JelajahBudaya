"""Serve the interactive browser preview and its original game data/art.

Run from any working directory with:
    python3 tools/preview_server.py
Then open http://localhost:4173/ (or the Arena live preview).
"""
from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("PORT", "4173"))


class PreviewHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        if urlsplit(self.path).path in ("/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/preview/")
            self.end_headers()
            return
        super().do_GET()

    def end_headers(self) -> None:  # noqa: N802 - stdlib handler API
        path = urlsplit(self.path).path
        if path == "/preview/" or (path.startswith("/preview/") and path.endswith((".html", ".css", ".js", ".json"))):
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def log_message(self, fmt: str, *args: object) -> None:
        print("[preview] " + (fmt % args))


def main() -> None:
    handler = partial(PreviewHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("0.0.0.0", PORT), handler)
    print(f"Nusantara browser preview listening on 0.0.0.0:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
