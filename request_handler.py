from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from currencies import Currencies
from exchange_rates import ExchangeRates
import utils
import json

class RequestHandler(BaseHTTPRequestHandler):
    def currencies_page(self) -> None:
        try:
            utils.send_content(self, HTTPStatus.OK, "application/json")
            data = json.dumps(Currencies.get_currency_table())
            self.wfile.write(data.encode("utf-8"))
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def currency_page(self) -> None:
        try:
            code = utils.parse_code(self).pop()
            all_codes = Currencies.get_all_codes()
            if not code:
                utils.send_content(self, HTTPStatus.BAD_REQUEST)
            elif code in all_codes:
                utils.send_content(self, HTTPStatus.OK, "application/json")
                data = json.dumps(Currencies.get_currency(code))
                self.wfile.write(data.encode("utf-8"))
            else:
                utils.send_content(self, HTTPStatus.NOT_FOUND)
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)
        
    def exchanges_page(self) -> None:
        try:
            utils.send_content(self, HTTPStatus.OK, "application/json")
            data = json.dumps(ExchangeRates.get_exchange_table())
            self.wfile.write(data.encode("utf-8"))
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def currency_exchange_page(self) -> None:
        try:
            first_curr, second_curr = utils.parse_code(self)
            base_curr = ExchangeRates.get_all_base_currencies()
            target_curr = ExchangeRates.get_all_target_currencies()

            if not first_curr or not second_curr:
                utils.send_content(self, HTTPStatus.BAD_REQUEST)
            elif first_curr in base_curr and second_curr in target_curr:
                utils.send_content(self, HTTPStatus.OK, "application/json")
                data = json.dumps(ExchangeRates.get_exchange_rate(first_curr, second_curr))
                self.wfile.write(data.encode("utf-8"))
            elif first_curr not in base_curr or second_curr not in target_curr:
                utils.send_content(self, HTTPStatus.NOT_FOUND)
            else:
                utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def add_currency_page(self) -> None:
        try:
            params = utils.parse_body(self)
            name = params.get("name", "")
            code = params.get("code", "")
            sign = params.get("sign", "")

            if name == "" or code == "" or sign == "":
                utils.send_content(self, HTTPStatus.BAD_REQUEST)
            elif name in Currencies.get_all_names():
                utils.send_content(self, HTTPStatus.CONFLICT)
            else:
                Currencies.add_item(code, name, sign)
                utils.send_content(self, HTTPStatus.CREATED, "/")
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def add_exchange_rate_page(self) -> None:
        try:
            params = utils.parse_body(self)

            base = params.get("baseCurrencyCode", "")
            target = params.get("targetCurrencyCode", "")
            rate_str = params.get("rate", "")
            try:
                rate = float(rate_str)
            except (ValueError, TypeError):
                rate = -1  # чтобы сработал BAD_REQUEST

            baseId = Currencies.get_currency_id(base)
            targetId = Currencies.get_currency_id(target)

            exists = ExchangeRates.get_exchange_rate(base, target)

            if base == "" or target == "" or rate <= 0:
                utils.send_content(self, HTTPStatus.BAD_REQUEST)
            elif baseId is None or targetId is None:
                utils.send_content(self, HTTPStatus.NOT_FOUND)
            elif exists:
                utils.send_content(self, HTTPStatus.CONFLICT)
            else:
                ExchangeRates.add_item(baseId, targetId, rate)
                utils.send_content(self, HTTPStatus.CREATED, "/")
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def patch_exchange_rate(self) -> None:
        try:
            params = utils.parse_body(self)
            try:
                rate = float(params.get("rate", ""))
            except (ValueError, TypeError):
                rate = -1

            codes = utils.parse_code(self)
            base_currency = codes[0]
            target_currency = codes[1]

            all_base_currencies = ExchangeRates.get_all_base_currencies()
            all_target_currencies = ExchangeRates.get_all_target_currencies()

            if base_currency == "" or target_currency == "" or rate <= 0:
                utils.send_content(self, HTTPStatus.BAD_REQUEST)
            elif base_currency not in all_base_currencies or target_currency not in all_target_currencies:
                utils.send_content(self, HTTPStatus.NOT_FOUND)
            else:
                ExchangeRates.update_rate(base_currency, target_currency, rate)
                utils.send_content(self, HTTPStatus.OK)
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def convert_currency(self) -> None:
        try:
            params = utils.parse_url(self)
            base = params.get('from', "")
            target = params.get('to', "")
            amount = float(params.get('amount', ""))
            rate = ExchangeRates.get_exchange_rate(base, target)
            converted_amount = ExchangeRates.calculate_exchange(base, target, amount)
            if not converted_amount:
                utils.throw_error(self, 
                                  HTTPStatus.BAD_REQUEST, 
                                  "value for amount or currencies cannot be negative or zero"
                                  )
                return
            response = {
                'baseCurrency': base,
                'targetCurrency': target,
                'rate': rate,
                'amount': amount,
                'convertedAmount': converted_amount
            }
            utils.send_content(self, HTTPStatus.OK, None, "application/json")
            data = json.dumps(response)
            self.wfile.write(data.encode('utf-8'))
        except Exception as e:
            utils.throw_error(self, HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
        
