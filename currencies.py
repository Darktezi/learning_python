import utils

class Currencies:
    @staticmethod
    def add_item(Code: str, FullName: str, Sign: str) -> None:
        with utils.db_cursor("currencies.db") as cursor:
            cursor.execute(
                '''
                INSERT INTO Currencies (Code, FullName, Sign)
                VALUES (?, ?, ?)
                ''',
                (Code, FullName, Sign)
            )
    
    @staticmethod
    def del_item(Code: str) -> None:
        with utils.db_cursor("currencies.db") as cursor:
            cursor.execute(
                '''
                DELETE FROM Currencies
                WHERE Code = ?
                ''',
                (Code,)
            )

    @staticmethod
    def get_currency_table() -> list[dict]:
        with utils.db_cursor("currencies.db") as cursor:
            cursor.execute(
                '''
                SELECT Code, FullName, Sign
                FROM Currencies
                '''
            )
            rows = cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            data = [dict(zip(col_names, row)) for row in rows]
            return data

    @staticmethod
    def get_all_codes():
        with utils.db_cursor("currencies.db") as cursor:
            cursor.execute(
                '''
                SELECT Code
                FROM Currencies
                '''
            )
            rows = cursor.fetchall()
            codes = [row[0] for row in rows]
            return codes
    
    @staticmethod
    def get_all_names():
        with utils.db_cursor("currencies.db") as cursor:
            cursor.execute(
                '''
                SELECT FullName
                FROM Currencies
                '''
            )
            rows = cursor.fetchall()
            names = [row[0] for row in rows]
            return names
    
    @staticmethod
    def get_currency(Code: str) -> dict:
        with utils.db_cursor("currencies.db") as cursor:
            cursor.execute(
                '''
                SELECT Code, FullName, Sign
                FROM Currencies
                WHERE Code = ?
                ''',
                (Code,)
            )
            row = cursor.fetchone()
            col_names = [description[0] for description in cursor.description]
            data = dict(zip(col_names, row))
            return data

    @staticmethod
    def get_currency_id(Code: str) -> int:
        with utils.db_cursor("currencies.db") as cursor:
            cursor.execute(
                '''
                SELECT ID
                FROM Currencies
                WHERE Code = ?
                ''',
                (Code,)
            )
            ID = cursor.fetchone()
            return ID[0]