import sqlite3

class Migration:
    @classmethod
    def create_currencies_db(cls) -> None:
        with sqlite3.connect("currencies.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Currencies (
            ID INTEGER PRIMARY KEY,
            Code TEXT NOT NULL,
            FullName TEXT NOT NULL,
            Sign TEXT NOT NULL
            );
            ''')
            connection.commit()

    @classmethod   
    def create_exchange_db(cls) -> None:
        with sqlite3.connect("exchange_rates.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ExchangeRates (
            ID INTEGER PRIMARY KEY,
            BaseCurrencyId TEXT NOT NULL,
            TargetCurrencyId TEXT NOT NULL,
            Rate REAL
            );
            ''')
            connection.commit()
    
    @classmethod
    def delete_currencies_db(cls) -> None:
        with sqlite3.connect("currencies.db") as connection:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS Currencies;")
            connection.commit()

    @classmethod
    def delete_exchange_db(cls) -> None:
        with sqlite3.connect("exchange_rates.db") as connection:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS ExchangeRates;")
            connection.commit()
