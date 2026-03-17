#!/usr/bin/env python3
"""
Simple reverse proxy + static file server for TinyLlama chatbot.
Serves frontend on port 8081 and proxies API requests to llama.cpp on port 8080.
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
import socket
from pathlib import Path
from urllib.parse import urlparse

PORT = 8081
BACKEND_HOST = "http://localhost:8080"
FRONTEND_DIR = Path(__file__).parent / "frontend"


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve static files from frontend directory."""
        if self.path == "/":
            self.path = "/index.html"

        # Serve static files
        self.directory = str(FRONTEND_DIR)
        return super().do_GET()

    def do_POST(self):
        """Proxy API requests to llama.cpp backend."""
        if self.path == "/completion":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)

                # Forward to backend
                req = urllib.request.Request(
                    f"{BACKEND_HOST}/completion",
                    data=body,
                    headers={"Content-Type": "application/json"}
                )

                with urllib.request.urlopen(req, timeout=120) as response:
                    response_data = response.read().decode('utf-8')

                    # Send response with proper CORS headers
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(response_data.encode('utf-8'))

            except urllib.error.URLError as e:
                self.send_error(503, f"Backend unavailable: {str(e)}")
            except socket.timeout:
                self.send_error(504, "Backend request timeout")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON in request body")
            except Exception as e:
                self.send_error(500, f"Server error: {str(e)}")
        else:
            self.send_error(404, "Not found")

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """Simple logging."""
        print(f"[{self.client_address[0]}] {format % args}")


if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), ProxyHandler) as httpd:
        print(f"Server running on port {PORT}")
        print(f"Frontend: http://localhost:{PORT}")
        print(f"Backend proxy: {BACKEND_HOST}")
        httpd.serve_forever()
