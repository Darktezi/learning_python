import sqlite3

class CC:
  @classmethod
  def add_item(cls, BaseCurrencyId: str, TargetCurrencyId: str, Rate: float) -> None:
    with sqlite3.connect("exchange_rates.db") as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)', (BaseCurrencyId, TargetCurrencyId, Rate))
                connection.commit()
  
  # @classmethod
  # def del_item(cls, Code: str) -> None:
  #     with sqlite3.connect("exchange_rates.db") as connection:
  #               cursor = connection.cursor()
  #               cursor.execute('DELETE FROM ExchangeRates WHERE Code = ?', (Code,))
  #               connection.commit()
  
  @classmethod
  def print_table(cls):
      with sqlite3.connect("exchange_rates.db") as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM ExchangeRates')
        users = cursor.fetchall()
        for user in users:
          print(user)

