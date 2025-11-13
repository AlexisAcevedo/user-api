"""
Servidor web simple para servir el frontend.
Ejecutar: python serve_frontend.py
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8001
FRONTEND_DIR = Path(__file__).parent / "frontend"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def end_headers(self):
        # Agregar headers para evitar caching en desarrollo
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(FRONTEND_DIR)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"""
╔══════════════════════════════════════════════════════╗
║        Frontend Server - Servidor Web Local          ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  🌐 URL: http://127.0.0.1:{PORT}                   ║
║  📁 Directorio: {FRONTEND_DIR}
║                                                      ║
║  ✓ Presiona Ctrl+C para detener el servidor        ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
        """)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✓ Servidor detenido correctamente")
