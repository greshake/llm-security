import http.server
import socketserver
import os
import json

PORT = 8007


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = str(body, 'utf-8')
        print(data)
        with open('data.txt', 'a') as f:
            f.write(data + '\n')
        self.send_response(200)
        self.end_headers()

# if it does not exist already, create the file data.txt
if not os.path.exists('data.txt'):
    with open('data.txt', 'w') as f:
        f.write('')
Handler = MyHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
