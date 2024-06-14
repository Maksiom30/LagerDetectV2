import http.server
import socketserver
import os
from getImages import getImages
from detect import detect_bottles

class RoutedHandler(http.server.SimpleHTTPRequestHandler):
   
    def do_GET(self):
        getImages()
        count = []
        for i in range(1, 4):
            count.append(detect_bottles(i))
            print(i)
        if self.path == '/':
            self.handle_root(count)
        elif self.path == '/img.jpg':
            self.handle_img()
        else:
            self.handle_404()

    def handle_root(self, bCount):
        with open(os.path.join(os.getcwd(), "templates/index.html"), "r") as file:
            html = file.read()
            file.close()
        html = html.replace("{count1}", str(bCount[0]))
        html = html.replace("{count2}", str(bCount[1]))
        html = html.replace("{count3}", str(bCount[2]))
        

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def handle_img(self):
        with open(os.path.join(os.getcwd(), "data/img.jpg"), "rb") as file:
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