import sqlite3

class DBCursor:
    def __init__(self) -> None:
        self.db_path = "data/currencies.db"
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
            
        self.conn.close()
        return False