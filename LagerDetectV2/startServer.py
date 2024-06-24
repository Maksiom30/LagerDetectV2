import http.server
import socketserver
import os
from getImages import getImages
from detect import detect_bottles

class Kasten():
    id = 0
    def __init__(self, name: str, max: int) -> None:
        self.id = Kasten.id
        self.name = name
        self.max = max
        self.nBottles = 0
        Kasten.id += 1

def init_data() -> list:  
    kaesten = [
        ["Früh Kölsch", 24],
        ["Irish Ale", 24],
        ["Spezi", 20],
        ["Rhodius Classic", 24],
        ["Bergmann Spezial", 20],
        ["Pinkus Special", 20],
        ["Fritz Cola", 24],
        ["Club Mate", 20],
        ["Bergmann Export", 20],
        ["Fritz Cola", 24],
        ["Club Mate Icetea", 20],
        ["Bionade", 24]
    ]
    kasten_list = []
    for kasten in kaesten:
        kasten_list.append(Kasten(kasten[0], kasten[1]))
    return kasten_list


class RoutedHandler(http.server.SimpleHTTPRequestHandler):
    kasten_list = init_data()
    def do_GET(self):
        getImages()
        self.sumCount = 0
        for kasten in self.kasten_list:
            kasten.nBottles = detect_bottles(kasten.id + 1)
            self.sumCount += kasten.nBottles
        print(self.path[:4])
        if self.path == '/':
            self.handle_root()
        elif self.path == '/img.jpg':
            self.handle_img()
        elif self.path == "/result.png":
            self.handle_logo()            
        elif self.path == "/favicon.ico":
            self.handle_favicon()
        elif self.path[:4] == "/scr":
            self.handle_scr()
        else:
            self.handle_404()

    def handle_root(self):
        with open(os.path.join("/home/pi/LagerDetectV2", "templates/index.html"), "r") as file:
            html = file.read()
            file.close()
        for kasten in self.kasten_list:
            html = html.replace("{namex}". replace("x", str(kasten.id + 1)), kasten.name)
            html = html.replace("{countx}".replace("x", str(kasten.id + 1)), str(kasten.nBottles))
            html = html.replace("{empt_countx}".replace("x", str(kasten.id + 1)), str(kasten.max - kasten.nBottles))
            html = html.replace("{prc_countx}".replace("x", str(kasten.id + 1)), str(round(kasten.nBottles / kasten.max * 100)) + "%")
        html = html.replace("{count_all}", str(self.sumCount))
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

    def handle_scr(self):
        print(f"/home/pi/LagerDetectV2/templates/scr/{self.path[5:]}")
        with open(f"/home/pi/LagerDetectV2/templates/scr/{self.path[5:]}", "rb") as file:
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