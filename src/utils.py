from http import HTTPStatus
from typing import Optional
from urllib import parse
import json


def send_content(handler, code: HTTPStatus, location: Optional[str] = None, content_type: Optional[str] = None) -> None:
    handler.send_response(code)
    if content_type:
        handler.send_header("Content-Type", content_type)
    if location:
        handler.send_header("Location", location)
    handler.end_headers()

def parse_code(self) -> str:
    parsed_path = parse.urlparse(self.path)
    path_parts = parsed_path.path.strip("/").split("/")
    code = path_parts.pop()
    return code

def parse_codes(self) -> list[str]:
    parsed_path = parse.urlparse(self.path)
    path_parts = parsed_path.path.strip("/").split("/")
    if len(path_parts) == 2:
        return [path_parts[1][:3], path_parts[1][3:]]
    else:
        self.send_response(HTTPStatus.BAD_REQUEST)
        return []

def parse_url(self) -> dict:
    parsed_path = parse.urlparse(self.path)
    params = dict(parse.parse_qsl(parsed_path.query))
    return params

def parse_body(self) -> dict:
    content_length = int(self.headers.get("Content-Length", 0))
    body = self.rfile.read(content_length)
    fields = dict(parse.parse_qsl(body.decode()))
    return fields

def throw_error(handler, status: HTTPStatus, message: str) -> None:
    send_content(handler, status, content_type="application/json")
    error = {"error": message}
    handler.wfile.write(json.dumps(error).encode('utf-8'))

def serve_file(self, filepath, content_type) -> None:
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND, 'File Not Found')

def json_all_curr(data: list[tuple]) -> str:
    currencies = [
    {"code": code, "name": name, "sign": sign}
    for code, name, sign in data
    ]
    return json.dumps(currencies)

def json_one_curr(data: tuple) -> str:
    currency_dict = {
        "code": data[0],
        "name": data[1],
        "sign": data[2]
    }
    return json.dumps(currency_dict)

def json_all_rates(data: list[tuple]) -> str:
    rates_dict = [
        {
        "baseCurrency": {"code": base},
        "targetCurrency": {"code": target},
        "rate": rate
        } for base, target, rate in data
    ]
    return json.dumps(rates_dict)

def codes_conversion(codes) -> list:
    return [code for (code,) in codes]
