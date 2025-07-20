from http import HTTPStatus
from http.server import BaseHTTPRequestHandler,HTTPServer
from currencies_controller import CC
import urllib.parse
import json

class HttpProcessor(BaseHTTPRequestHandler):
    def test_page(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('content-type','text/html; charset=UTF-8')
        self.end_headers()

        self.wfile.write("<h1> Hello world</h1>".encode("utf-8"))

    def currencies_page(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        data = json.dumps(CC.get_table())
        self.wfile.write(data.encode("utf-8"))
    
    def currency_page(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")
        code = ''
        all_codes = CC.get_all_codes()
        if len(path_parts) == 2:
            code = path_parts[1]
        else:
            self.send_response(HTTPStatus.BAD_REQUEST)

        if code in all_codes:
            data = json.dumps(CC.get_currency(code))
            self.wfile.write(data.encode("utf-8"))
        elif code not in all_codes:
            self.send_response(HTTPStatus.NOT_FOUND)
        else:
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)

    def currency_form(self):
        with open("currency_form.html", "r", encoding="utf-8") as f:
            html = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
    
    def add_currency_page(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        fields = dict(urllib.parse.parse_qsl(body.decode()))

        name = fields.get("name", "")
        code = fields.get("code", "")
        sign = fields.get("sign", "")

        if name == "" or code == "" or sign == "":
            self.send_response(HTTPStatus.BAD_REQUEST)
        elif name in CC.get_all_names():
            self.send_response(HTTPStatus.CONFLICT)
        else:
            CC.add_item(code, name, sign)
            self.send_response(HTTPStatus.CREATED)

    def do_GET(self):
        if self.path == "/":
            self.test_page()

        elif self.path == "/currencies":
            self.currencies_page()
        
        elif self.path.startswith("/currency/"):
            self.currency_page()
        
        elif self.path == "/currency":
            self.currency_form()
    
    def do_POST(self):
        if self.path == ("/currency"):
            self.add_currency_page()


if __name__ == "__main__":
    with HTTPServer(('', 8000), HttpProcessor) as server:
        server.serve_forever()