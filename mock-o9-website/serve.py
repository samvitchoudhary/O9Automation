#!/usr/bin/env python3
"""
Simple HTTP server for mock O9 website
Run this from the mock-o9-website directory
"""
import http.server
import socketserver
import os

PORT = 3001
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("=" * 60)
        print(f"Mock O9 Website Server")
        print("=" * 60)
        print(f"Serving at: http://localhost:{PORT}")
        print(f"Directory: {DIRECTORY}")
        print("=" * 60)
        print("Test URLs:")
        print(f"  Login:    http://localhost:{PORT}/index.html")
        print(f"  Dashboard: http://localhost:{PORT}/dashboard.html")
        print(f"  Forecast:  http://localhost:{PORT}/forecast.html")
        print(f"  BOM:       http://localhost:{PORT}/bom-setup.html")
        print("=" * 60)
        print("Press Ctrl+C to stop")
        print("=" * 60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            httpd.shutdown()

