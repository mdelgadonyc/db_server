# BaseHTTPServer is an HTTP server library. It understands the HTTP protocol and let your code handle requests. It does
# not have any "logic" of its own and serves as a base for implementing some development server for a web application.
#
# The BaseHTTPRequestHandler.handle() method in the BaseHTTPRequestHandler class handles HTTP requests. It is called by
# the HTTPServer.serve_forever() method when a new HTTP request is received. The handle() method parses the HTTP
# request, extracts the request method and path, and then calls the appropriate do_METHOD() method to handle the
# request. The do_METHOD() methods are responsible for generating the HTTP response for the request.
#
# https://docs.python.org/3/library/http.server.html
# http.server — classes for implementing HTTP servers
# https://docs.python.org/3/library/socketserver.html
# socketserver — A framework for network servers¶

import http.server
import socketserver
import json
from urllib.parse import urlparse

PORT = 4000
saved_values = {}


class requestHandler(http.server.BaseHTTPRequestHandler):
    def complete_response(self, found_values=None):
        if found_values is None:
            found_values = {}

        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

        output_data = {'status': 'OK'}
        for key, value in found_values.items():
            output_data[key] = value
        output_json = json.dumps(output_data)

        self.wfile.write(output_json.encode('utf-8'))

    def do_GET(self):
        found_values = {}
        url_result = urlparse(self.path)

        if url_result.path == '/get':
            keys = url_result.query.split('&')
            for key in keys:
                if key in saved_values:
                    print(f"saved_values[{key}]: {saved_values[key]}")
                    found_values[key] = saved_values[key]
                else:
                    print(f"The key [{key}] was not found in saved_value.")

        self.complete_response(found_values=found_values)

    def do_POST(self):
        url_result = urlparse(self.path)
        print(f"self.path: {self.path}")

        if url_result.path == '/set':
            pairs = url_result.query.split('&')
            for pair in pairs:
                if pair:
                    query_list = pair.split("=")
                    print(f"pair: {pair}")
                    # Attempt to save key and value pair only if both are detected
                    if len(query_list) == 2:
                        saved_values[query_list[0]] = query_list[1]
            print(f"saved_values: {saved_values}")

        length = int(self.headers['Content-Length'])
        if length:
            input_json = self.rfile.read(length)
            input_data = json.loads(input_json)
            print(input_data)

        self.complete_response()


req_handler = requestHandler

with socketserver.TCPServer(("", PORT), req_handler) as server:
    server.serve_forever()
