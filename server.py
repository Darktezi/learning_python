from http.server import HTTPServer
from request_handler import RequestHandler
import utils

class HttpProcessor(RequestHandler):
    def do_GET(self) -> None:
        if self.path == "/" or self.path == '/index.html':
            utils.serve_file(self, 'index.html', 'text/html')

        elif self.path.endswith('.css'):
            utils.serve_file(self, self.path[1:], 'text/css')

        elif self.path.endswith('.js'):
            utils.serve_file(self, self.path[1:], 'application/javascript')

        elif self.path == "/currencies":
            self.currencies_page()
        
        elif self.path == "/exchangeRates":
            self.exchanges_page()
        
        elif self.path.startswith("/currency/"):
            self.currency_page()
        
        elif self.path.startswith("/exchangeRate/"):
            self.currency_exchange_page()
        
        elif self.path.startswith("/exchange"):
            self.convert_currency()
    
    def do_POST(self) -> None:
        if self.path == ("/currencies"):
            self.add_currency_page()
        
        elif self.path == ("/exchangeRates"):
            self.add_exchange_rate_page()
    
    def do_PATCH(self) -> None:
        if self.path.startswith("/exchangeRate/"):
            self.patch_exchange_rate()


def main() -> None:
    with HTTPServer(('', 8000), HttpProcessor) as server:
        print("Server started on port 8000...")
        server.serve_forever()


if __name__ == "__main__":
    main()