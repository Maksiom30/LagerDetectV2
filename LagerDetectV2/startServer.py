import http.server
import socketserver
import os
from getImages import getImages
from detect import detect_bottles

class RoutedHandler(http.server.SimpleHTTPRequestHandler):
        

    def do_GET(self):
        getImages()
        count = 0
        for i in range(12):
            count += detect_bottles(i+1)
        

        if self.path == '/':
            self.handle_root(count)
        elif self.path == '/img.jpg':
            self.handle_img()
        elif self.path == "/result.png":
            self.handle_logo()            
        elif self.path == "/favicon.ico":
            self.handle_favicon()
        else:
            self.handle_404()

    def handle_root(self, bCount):
        with open(os.path.join("/home/pi/LagerDetectV2", "templates/index.html"), "r") as file:
            html = file.read()
            file.close()
        html = html.replace("{count1}", str(bCount))


        

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def handle_img(self):
        with open("/home/pi/LagerDetectV2/data/img.jpg", "rb") as file:
            img = file.read()
            file.close()
        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()
        self.wfile.write(img)


    def handle_logo(self):
        with open("/home/pi/LagerDetectV2/templates/result.png", "rb") as file:
            img = file.read()
            file.close()
        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()
        self.wfile.write(img)

    def handle_favicon(self):
        with open("/home/pi/LagerDetectV2/templates/result.png", "rb") as file:
            img = file.read()
            file.close()
        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()
        self.wfile.write(img)

    def handle_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")

    

# Define the port on which you want to serve
def startServer(PORT=8000):
    socketserver.TCPServer.allow_reuse_address = True
    # Create the HTTP server and bind it to the specified port with the custom handler
    with socketserver.TCPServer(("", PORT), RoutedHandler) as httpd:
        print(f"Serving HTTP on port {PORT}")
        # Serve the HTTP server until interrupted
        httpd.serve_forever()

if __name__ == "__main__":
    startServer()