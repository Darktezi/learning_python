import utils

class ExchangeRates:
    @staticmethod
    def add_item(BaseCurrencyId: int, TargetCurrencyId: int, Rate: float) -> None:
        with utils.db_cursor("exchange_rates.db") as cursor:
            cursor.execute(
                            '''
                            INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) 
                            VALUES (?, ?, ?)
                            ''', 
                            (BaseCurrencyId, TargetCurrencyId, Rate)
            )
    
    @staticmethod
    def del_item(BaseCurrencyId: int, TargetCurrencyId: int) -> None:
        with utils.db_cursor("exchange_rates.db") as cursor:
            cursor.execute(
                           '''
                           DELETE FROM ExchangeRates 
                           WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?
                           ''', 
                           (BaseCurrencyId, TargetCurrencyId))
  
    @staticmethod
    def get_all_base_currencies() -> list[str]:
        with utils.db_cursor("exchange_rates.db") as cursor:
            cursor.execute("ATTACH DATABASE 'currencies.db' AS curr")
            cursor.execute(
                            '''
                            SELECT base.Code AS BaseCurrency
                            FROM ExchangeRates
                            JOIN curr.Currencies AS base ON ExchangeRates.BaseCurrencyId = base.ID;
                            '''
            )
            rows = cursor.fetchall()
            base = [row[0] for row in rows]
            return base
    
    @staticmethod
    def get_all_target_currencies() -> list[str]:
        with utils.db_cursor("exchange_rates.db") as cursor:
            cursor.execute("ATTACH DATABASE 'currencies.db' AS curr")
            cursor.execute(
                            '''
                            SELECT target.Code AS TargetCurrency
                            FROM ExchangeRates
                            JOIN curr.Currencies AS target ON ExchangeRates.TargetCurrencyId = target.ID;
                            '''
            )
            rows = cursor.fetchall()
            base = [row[0] for row in rows]
            return base
        
    @staticmethod
    def get_exchange_rate(Base: str, Target: str) -> float | None:
        with utils.db_cursor("exchange_rates.db") as cursor:
            cursor.execute("ATTACH DATABASE 'currencies.db' AS curr")
            cursor.execute(
                            '''
                            SELECT Rate FROM ExchangeRates 
                            JOIN curr.Currencies AS base ON ExchangeRates.BaseCurrencyId = base.ID
                            JOIN curr.Currencies AS target ON ExchangeRates.TargetCurrencyId = target.ID
                            WHERE base.Code = ? AND target.Code = ?
                            ''',
                            (Base, Target)
                        
            )
            data = cursor.fetchone()
            if data is None:
                return None
            return data[0]

    @staticmethod
    def get_exchange_table() -> list[dict]:
        with utils.db_cursor("exchange_rates.db") as cursor:
            cursor.execute("ATTACH DATABASE 'currencies.db' AS curr")
            cursor.execute(
                            '''
                            SELECT base.Code AS BaseCurrency, target.Code AS TargetCurrency, ExchangeRates.Rate
                            FROM ExchangeRates
                            JOIN curr.Currencies AS base ON ExchangeRates.BaseCurrencyId = base.ID
                            JOIN curr.Currencies AS target ON ExchangeRates.TargetCurrencyId = target.ID;
                            '''
            )   
            rows = cursor.fetchall()
            data = []
            for row in rows:
                base_code, target_code, rate = row
                item = {
                    "baseCurrency": {"code": base_code},
                    "targetCurrency": {"code": target_code},
                    "rate": rate
                }
                data.append(item)
            return data
    
    @staticmethod
    def update_rate(BaseCurrencyCode, TargetCurrencyCode, Rate) -> None:
        with utils.db_cursor("exchange_rates.db") as cursor:
            cursor.execute("ATTACH DATABASE 'currencies.db' AS curr")
            cursor.execute(
                            '''
                            UPDATE ExchangeRates
                            SET Rate = ?
                            WHERE BaseCurrencyId = (SELECT ID FROM curr.Currencies WHERE Code = ?)
                            AND TargetCurrencyId = (SELECT ID FROM curr.Currencies WHERE Code = ?)
                            ''', 
                            (Rate, BaseCurrencyCode, TargetCurrencyCode)
            ) 
    
    @staticmethod
    def print_table() -> None:
        with utils.db_cursor("exchange_rates.db") as cursor:
            cursor.execute('SELECT * FROM ExchangeRates')
            items = cursor.fetchall()
            for item in items:
                print(item)
    
    @staticmethod
    def calculate_exchange(base: str, target: str, amount: float) -> float | None:
        if amount < 0:
            return None
            
        base_currencies = ExchangeRates.get_all_base_currencies()
        target_currencies = ExchangeRates.get_all_target_currencies()

        if base == target:
            return amount
        
        elif base in base_currencies and target in target_currencies:
            rate = ExchangeRates.get_exchange_rate(base, target)
            if not rate:
                return None
            converted_amount = amount * rate
            return converted_amount
        
        elif base in target_currencies and target in base_currencies:
            rate = ExchangeRates.get_exchange_rate(target, base)
            if not rate:
                return None
            reversed_rate = 1/rate
            converted_amount = amount * reversed_rate
            return converted_amount
        
        else:
            rateA = ExchangeRates.get_exchange_rate("USD", base)
            rateB = ExchangeRates.get_exchange_rate("USD", target)
            if not rateA or not rateB:
                return None
            rate = rateB/rateA
            converted_amount = amount * rate
            return round(converted_amount, 2)

