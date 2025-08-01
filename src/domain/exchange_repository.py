from src.domain.table_repository import TableRepository
from src.db.db_cursor import DBCursor
from src.domain.dto import ExchangeRateDTO

class ExchangeRepository(TableRepository):

    def get(self, id: int) -> tuple:
        with DBCursor() as cursor:
            cursor.execute(
                '''
                SELECT BaseCurrencyId, TargetCurrencyId, Rate
                FROM ExchangeRates
                WHERE ID = ?
                ''',
                (id,)
            )
            return cursor.fetchone()
        
    def get_currencies(self, curr_row: str) -> list[tuple]:
        with DBCursor() as cursor:
            cursor.execute(
                            f'''
                            SELECT curr.Code AS Currency
                            FROM ExchangeRates
                            JOIN Currencies AS curr ON ExchangeRates.{curr_row} = curr.ID;
                            '''
            )
            return cursor.fetchall()
    
    def get_exchange_rate(self, base: str, target: str) -> float | None:
        with DBCursor() as cursor:
            cursor.execute(
                            '''
                            SELECT Rate FROM ExchangeRates 
                            JOIN Currencies AS base ON ExchangeRates.BaseCurrencyId = base.ID
                            JOIN Currencies AS target ON ExchangeRates.TargetCurrencyId = target.ID
                            WHERE base.Code = ? AND target.Code = ?
                            ''',
                            (base, target)      
            )
            data = cursor.fetchone()
            if data is None:
                return None
            return data[0]
    
    def get_id(self, base: str, target: str) -> int:
        with DBCursor() as cursor:
            cursor.execute(
                '''
                SELECT ID
                FROM ExchangeRates
                JOIN Currencies AS base ON ExchangeRates.BaseCurrencyId = base.ID
                JOIN Currencies AS target ON ExchangeRates.TargetCurrencyId = target.ID
                WHERE base.Code = ? AND target.Code = ?
                ''',
                (base, target)
            )
            return cursor.fetchone()[0]
    
    def get_all(self) -> list:
        with DBCursor() as cursor:
            cursor.execute(
                '''
                SELECT base.Code AS BaseCurrency, target.Code AS TargetCurrency, ExchangeRates.Rate
                FROM ExchangeRates
                JOIN Currencies AS base ON ExchangeRates.BaseCurrencyId = base.ID
                JOIN Currencies AS target ON ExchangeRates.TargetCurrencyId = target.ID;
                '''
            )
            return cursor.fetchall()
    
    def add(self, entity: ExchangeRateDTO):
        with DBCursor() as cursor:
            cursor.execute(
                '''
                INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate)
                VALUES (?, ?, ?)
                ''',
                (entity.base_id, entity.target_id, entity.rate)
            )
        
    def update(self, entity: ExchangeRateDTO):
        with DBCursor() as cursor:
            cursor.execute(
                            '''
                            UPDATE ExchangeRates
                            SET Rate = ?
                            WHERE BaseCurrencyId = ?
                            AND TargetCurrencyId = ?
                            ''', 
                            (entity.rate, entity.base_id, entity.target_id)
            ) 
    
    # def delete(self, id: int):
    #     with DBCursor() as cursor:
    #         cursor.execute(
    #             '''
    #             DELETE FROM ExchangeRates
    #             WHERE ID = ?
    #             ''',
    #             (id,)
    #         )