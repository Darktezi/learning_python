import utils


def create_cdb() -> None:
    with utils.db_cursor("currencies.db") as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Currencies (
            ID INTEGER PRIMARY KEY,
            Code TEXT NOT NULL,
            FullName TEXT NOT NULL,
            Sign TEXT NOT NULL
            );
            '''
        )


def create_edb() -> None:
    with utils.db_cursor("exchange_rates.db") as cursor:
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS ExchangeRates (
            ID INTEGER PRIMARY KEY,
            BaseCurrencyId INTEGER,
            TargetCurrencyId INTEGER,
            Rate REAL,
            FOREIGN KEY(BaseCurrencyId) REFERENCES Currencies(ID),
            FOREIGN KEY(TargetCurrencyId) REFERENCES Currencies(ID)
            );
            '''
        )


def delete_cdb() -> None:
    with utils.db_cursor("currencies.db") as cursor:
        cursor.execute("DROP TABLE IF EXISTS Currencies;")


def delete_edb() -> None:
    with utils.db_cursor("exchange_rates.db") as cursor:
        cursor.execute("DROP TABLE IF EXISTS ExchangeRates;")