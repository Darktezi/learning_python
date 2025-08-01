from src.db.db_cursor import DBCursor
from src.domain.dto import CurrencyDTO
from src.domain.table_repository import TableRepository

class CurrRepository(TableRepository):
    def add(self, entity: CurrencyDTO) -> None:
        with DBCursor() as cursor:
            cursor.execute(
                '''
                INSERT INTO Currencies (Code, FullName, Sign)
                VALUES (?, ?, ?)
                ''',
                (entity.code, entity.name, entity.sign)
            )
    
    # def delete(self, id: int) -> None:
    #     with DBCursor() as cursor:
    #         cursor.execute(
    #             '''
    #             DELETE FROM Currencies
    #             WHERE ID = ?
    #             ''',
    #             (id,)
    #         )

    def get(self, id: int) -> tuple:
        with DBCursor() as cursor:
            cursor.execute(
                '''
                SELECT Code, FullName, Sign
                FROM Currencies
                WHERE ID = ?
                ''',
                (id,)
            )
            return cursor.fetchone()
    
    def get_all(self) -> list:
        with DBCursor() as cursor:
            cursor.execute(
                '''
                SELECT Code, FullName, Sign
                FROM Currencies
                '''
            )
            return cursor.fetchall()
    
    def get_rows(self, row_name: str):
        with DBCursor() as cursor:
            cursor.execute(
                f'''
                SELECT {row_name}
                FROM Currencies
                '''
            )
            return cursor.fetchall()
    
    def get_id(self, code: str) -> int:
        with DBCursor() as cursor:
            cursor.execute(
                '''
                SELECT ID
                FROM Currencies
                WHERE Code = ?
                ''',
                (code,)
            )
            return cursor.fetchone()[0]
    