import http.server
import os
import argparse
import cgi 

PORT = 8090


class CoolHandler(http.server.BaseHTTPRequestHandler):

    static = os.curdir + os.sep + 'static'
    downloads = os.curdir + os.sep + 'downloads'

    def respond(self, content=None, c_type='text/html'):
        self.send_response(200)
        self.send_header('Content-Type', c_type)
        self.end_headers()   
        self.wfile.write(content)

    def do_GET(self):
        if self.path == '/':
            self.path = 'task.html'

        if self.path.endswith('.html'):
            mimetype='text/html'
        if self.path.endswith('.js'):
            mimetype='application/javascript'
        if self.path.endswith('.css'):
            mimetype='text/css'

        with open(self.static + os.sep + self.path, 'rb') as f:
            self.respond(f.read(), mimetype)
                

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={
                'REQUEST_METHOD':'POST',
                'CONTENT_TYPE':self.headers['Content-Type'],
            })
        def form_recursive(form):
            for field in form.list:
                if isinstance(field, list):
                   form_recursive(field)
                elif field.filename:
                    print(f'\t{field.name}: {field.filename}')
                    with open(self.downloads + os.sep + field.filename, 'wb') as f:
                        f.write(field.value)
                else:
                    print(f'\t{field.name}: {field.value}')
        form_recursive(form)
        self.respond(b'Quest complete!')

def run(server_class=http.server.HTTPServer, handler_class=CoolHandler, addr='localhost', port=PORT):
    httpd = server_class((addr, port), handler_class)
    print(f'Starting httpd server on {addr}:{port}')   
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        httpd.socket.close()    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=PORT,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)

    