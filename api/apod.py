"""Vercel サーバーレス関数: NASA APOD API プロキシ"""

import json
import os
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler
from datetime import date


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        api_key = os.environ.get("NASA_API_KEY", "DEMO_KEY")
        target_date = date.today().isoformat()

        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={target_date}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)

        except urllib.error.HTTPError as e:
            body = e.read()
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
