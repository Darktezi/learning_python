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

file_path = "words.txt"

def read_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
      words = file.read().splitlines()
  return words

def choise_menu():
    print("======== Меню ========")
    print("1 - начать новую игру")
    print("2 - выйти из игры")
    choise = input("Выберите действие: ")
    return choise

def game_logic():
    mistakes = 0
    hiden_symbols = []
    symbols = {}
    suggested_letter = []
    word = random.choice(words)
    for index, char in enumerate(word):
        if char not in symbols:
            symbols[char] = [index]
        else:
            symbols[char].append(index)
        hiden_symbols += "-"
    while symbols and mistakes != 6:
        print(pictures[mistakes])
        print("Количество ошибок: ", mistakes)
        print("Загаданное слово: " + "".join(hiden_symbols))
        character = input("Введите букву: ")
        print("====================================================")
        if character in symbols and character not in suggested_letter:
            suggested_letter.append(character)
            for index in symbols[character]:
                hiden_symbols[index] = character
            del symbols[character]
        elif character in suggested_letter:
            print("Вы уже вводили данную букву")
        else:
            print("Такой буквы нет.")
            suggested_letter.append(character)
            mistakes += 1
        if mistakes == 6:
            print(pictures[mistakes])
            print("ПОРАЖЕНИЕ! УВЫ! В СЛЕДУЮЩИЙ РАЗ ПОВЕЗЁТ!")
        if not symbols:
            print(pictures[mistakes])
            print("УРА ПОБЕДА!!!")

words = read_file(file_path)

while True:
    choise = choise_menu()

    match choise:
        case "1":
            game_logic()
        case "2":
            sys.exit()
        case _:
            print("нет такого выбора в меню")
