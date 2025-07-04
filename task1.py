import sys
import random

pictures = [
"""            
  _______
  |     |
  |
  |
  |
  |
__|________
""", 
""" 
  _______
  |     |
  |     O
  |
  |
  |
__|________
""",
"""
  _______
  |     |
  |     O
  |     |
  |     |
  |
__|________
""",
"""
  _______
  |     |
  |     O
  |    /|
  |     |
  |
__|________
""",
"""
  _______
  |     |
  |     O
  |    /|\\
  |     |
  |
__|________
""",
"""
  _______
  |     |
  |     O
  |    /|\\
  |     |
  |    /
__|________
""",
"""
  _______
  |     |
  |     O
  |    /|\\
  |     |
  |    / \\
__|________
""",]


def read_file(file_path: str) -> list[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().splitlines()


def choice_menu() -> str:
    print("======== Меню ========")
    print("1 - Начать новую игру")
    print("2 - Выйти из игры")
    choise = input("Выберите действие: ")
    return choise


def str_to_dict(str: str, dict: dict[str, list[int]]) -> None:
    for index, char in enumerate(str):
        if char not in dict:
            dict[char] = [index]
        else:
            dict[char].append(index)


def input_letter() -> str:
    while True:
          character = input("Введите букву: ").lower()
          if len(character) == 1:
              break
          print("Ошибка! Введите ровно один символ.")
    return character


def game_logic() -> None:
    mistakes = 0
    hidden_letters, used_letters = [],[]
    right_letters = {}
    allowed_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫБЬЭЮЯ"
    words = read_file("words.txt")
    word = random.choice(words)
    str_to_dict(word, right_letters)
    hidden_letters += "-" * len(word)

    while right_letters and mistakes != 6:
        print(pictures[mistakes])
        print("Количество ошибок: ", mistakes)
        print("Загаданное слово: " + "".join(hidden_letters))
        character = input_letter()
        print("====================================================")
        if character in right_letters and character not in used_letters:
            used_letters.append(character)
            for index in right_letters[character]:
                hidden_letters[index] = character
            del right_letters[character]
        elif character not in allowed_letters:
            print("Можно вводить только русские буквы")
        elif character in used_letters:
            print("Вы уже вводили данную букву")
        else:
            print("Такой буквы нет.")
            used_letters.append(character)
            mistakes += 1
    if mistakes == 6:
        print(pictures[mistakes])
        print("ПОРАЖЕНИЕ! УВЫ! В СЛЕДУЮЩИЙ РАЗ ПОВЕЗЁТ!")
        print("Загаданное слово: ", word)
    else:
        print(pictures[mistakes])
        print("УРА ПОБЕДА!!!")
        print("Загаданное слово: ", word)


def main() -> None:
    while True:
        
        choise = choice_menu()

        match choise:
            case "1":
                game_logic()
            case "2":
                sys.exit()
            case _:
                print("Нет такого выбора в меню")

if __name__ == "__main__":
    main()
