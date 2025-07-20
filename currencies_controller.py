import sqlite3
import json

class CC:
  @classmethod
  def add_item(cls, Code: str, FullName: str, Sign: str) -> None:
    with sqlite3.connect("currencies.db") as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)', (Code, FullName, Sign))
                connection.commit()
  
  @classmethod
  def del_item(cls, Code: str) -> None:
      with sqlite3.connect("currencies.db") as connection:
                cursor = connection.cursor()
                cursor.execute('DELETE FROM Currencies WHERE Code = ?', (Code,))
                connection.commit()
  
  @classmethod
  def get_table(cls) -> list[dict]:
      with sqlite3.connect("currencies.db") as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Currencies')

        rows = cursor.fetchall()
        col_names = [description[0] for description in cursor.description]

        data = [dict(zip(col_names, row)) for row in rows]

        return data
  

  @classmethod
  def get_all_codes(cls):
       with sqlite3.connect("currencies.db") as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT Code FROM Currencies')

        rows = cursor.fetchall()

        codes = [row[0] for row in rows]

        return codes
  
  @classmethod
  def get_all_names(cls):
      with sqlite3.connect("currencies.db") as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT FullName FROM Currencies')

        rows = cursor.fetchall()
        names = [row[0] for row in rows]
        return names
  
  @classmethod
  def get_currency(cls, Code: str) -> dict:
        with sqlite3.connect("currencies.db") as connection:
             cursor = connection.cursor()
             cursor.execute('SELECT * FROM Currencies WHERE Code = ?', (Code,))

             row = cursor.fetchone()
             col_names = [description[0] for description in cursor.description]

             data = dict(zip(col_names, row))

             return data





# Добавляем нового пользователя
# cursor.execute('INSERT INTO Currencies (Code, FullName, Sign) VALUES ("JPY", "Japanese yen", "¥")')
# cursor.execute('UPDATE Currencies SET Sign = "¥" WHERE Code = "JPY"')
# cursor.execute('SELECT * FROM Currencies')
# users = cursor.fetchall

# # Выводим результаты
# for user in users:
#   print(user)