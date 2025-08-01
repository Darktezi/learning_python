from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from src.domain.curr_repository import CurrRepository
from src.domain.exchange_repository import ExchangeRepository
from src.domain.dto import CurrencyDTO, ExchangeRateDTO
import src.utils as utils
import json

class RequestHandler(BaseHTTPRequestHandler):
    curr_rep = CurrRepository()
    exch_rep = ExchangeRepository()

    def currencies_page(self) -> None:
        try:
            utils.send_content(self, HTTPStatus.OK, None, "application/json")
            all_curr = self.curr_rep.get_all()
            data = utils.json_all_curr(all_curr)
            self.wfile.write(data.encode("utf-8"))
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def currency_page(self) -> None:
        try:
            code = utils.parse_code(self)
            id = self.curr_rep.get_id(code)
            all_codes = utils.codes_conversion(self.curr_rep.get_rows("Code"))
            if not code:
                utils.send_content(self, HTTPStatus.BAD_REQUEST)
            elif code in all_codes:
                utils.send_content(self, HTTPStatus.OK, None, "application/json")
                data = utils.json_one_curr(self.curr_rep.get(id))
                self.wfile.write(data.encode("utf-8"))
            else:
                utils.send_content(self, HTTPStatus.NOT_FOUND)
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)
        
    def exchanges_page(self) -> None:
        try:
            utils.send_content(self, HTTPStatus.OK, None, "application/json")
            all_rates = self.exch_rep.get_all()
            data = utils.json_all_rates(all_rates)
            self.wfile.write(data.encode("utf-8"))
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def currency_exchange_page(self) -> None:
        try:
            first_curr, second_curr = utils.parse_codes(self)
            raw_base_curr = self.exch_rep.get_currencies("BaseCurrencyId")
            raw_target_curr = self.exch_rep.get_currencies("TargetCurrencyId")
            base_curr = utils.codes_conversion(raw_base_curr)
            target_curr = utils.codes_conversion(raw_target_curr)

            if not first_curr or not second_curr:
                utils.send_content(self, HTTPStatus.BAD_REQUEST)
            elif first_curr in base_curr and second_curr in target_curr:
                utils.send_content(self, HTTPStatus.OK, None, "application/json")
                rate = self.exch_rep.get_exchange_rate(first_curr, second_curr)
                self.wfile.write(json.dumps(rate).encode("utf-8"))
            elif first_curr not in base_curr or second_curr not in target_curr:
                utils.send_content(self, HTTPStatus.NOT_FOUND)
            else:
                utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def add_currency_page(self) -> None:
        try:
            params = utils.parse_body(self)
            currency = CurrencyDTO(
                code = params.get("code", ""),
                name = params.get("name", ""),
                sign = params.get("sign", "")
            )

            if currency.name == "" or currency.code == "" or currency.sign == "":
                utils.send_content(self, HTTPStatus.BAD_REQUEST)
            elif currency.name in self.curr_rep.get_rows("FullName"):
                utils.send_content(self, HTTPStatus.CONFLICT)
            else:
                self.curr_rep.add(currency)
                utils.send_content(self, HTTPStatus.CREATED, "/")
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def add_exchange_rate_page(self) -> None:
        try:
            params = utils.parse_body(self)
            base = params.get("baseCurrencyCode", "")
            target = params.get("targetCurrencyCode", "")
            rate_str = params.get("rate", "")

            exc = ExchangeRateDTO(
                base_id = self.curr_rep.get_id(base),
                target_id = self.curr_rep.get_id(target),
                rate = float(rate_str)
            )

            if exc.base_id == None or exc.target_id == "" or exc.rate <= 0:
                utils.send_content(self, HTTPStatus.BAD_REQUEST)
            elif exc.base_id is None or exc.target_id is None:
                utils.send_content(self, HTTPStatus.NOT_FOUND)
            else:
                self.exch_rep.add(exc)
                utils.send_content(self, HTTPStatus.CREATED, "/")
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def patch_exchange_rate(self) -> None:
        try:
            params = utils.parse_body(self)
            codes = utils.parse_codes(self)
            exc = ExchangeRateDTO(
                base_id = self.curr_rep.get_id(codes[0]),
                target_id = self.curr_rep.get_id(codes[1]),
                rate = float(params.get("rate", ""))
            )

            if exc.base_id == None or exc.target_id == None or exc.rate <= 0:
                utils.send_content(self, HTTPStatus.BAD_REQUEST)
            else:
                self.exch_rep.update(exc)
                utils.send_content(self, HTTPStatus.OK)
        except Exception:
            utils.send_content(self, HTTPStatus.INTERNAL_SERVER_ERROR)

    def _calculate_exchange(self, base: str, target: str, amount: float) -> float | None:
        if amount <= 0:
            return None
            
        raw_base_currencies = self.exch_rep.get_currencies("BaseCurrencyId")
        raw_target_currencies = self.exch_rep.get_currencies("TargetCurrencyId")

        base_currencies = utils.codes_conversion(raw_base_currencies)
        target_currencies = utils.codes_conversion(raw_target_currencies)

        if base == target:
            return amount
        
        elif base in base_currencies and target in target_currencies:
            rate = self.exch_rep.get_exchange_rate(base, target)
            if not rate:
                return None
            converted_amount = amount * rate
            return converted_amount
        
        elif base in target_currencies and target in base_currencies:
            rate = self.exch_rep.get_exchange_rate(target, base)
            if not rate:
                return None
            reversed_rate = 1/rate
            converted_amount = amount * reversed_rate
            return converted_amount
        
        else:
            rateA = self.exch_rep.get_exchange_rate("USD", base)
            rateB = self.exch_rep.get_exchange_rate("USD", target)
            if not rateA or not rateB:
                return None
            rate = rateB/rateA
            converted_amount = amount * rate
            return float(round(converted_amount, 2))

    def convert_currency(self) -> None:
        try:
            params = utils.parse_url(self)
            base = params.get('from', "")
            target = params.get('to', "")
            amount = float(params.get('amount', ""))
            rate = self.exch_rep.get_exchange_rate(base, target)
            converted_amount = self._calculate_exchange(base, target, amount)
            if not converted_amount:
                utils.throw_error(
                            self,
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
        
