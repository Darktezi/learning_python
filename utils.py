from http import HTTPStatus
from typing import Optional
from urllib import parse
from contextlib import contextmanager
import sqlite3
import json

def send_content(self, code: HTTPStatus, location: Optional[str]=None, content_type: Optional[str]=None) -> None:
    self.send_response(code)
    if content_type:
        self.send_header("Content-Type", content_type)
    elif location:
        self.send_header("Location", location)
    self.end_headers()

def parse_code(self) -> list[str]:
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

def throw_error(self, status: HTTPStatus, message: str) -> None:
    send_content(self, status, None, "application/json")
    error = json.dumps({"message": message})
    self.wfile.write(error.encode('utf-8'))

def serve_file(self, filename, content_type) -> None:
        try:
            with open(filename, 'rb') as f:
                content = f.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND, 'File Not Found')

@contextmanager
def db_cursor(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        connection.close()