import unittest
from adding_word_algoritm import Crossword


crossword = Crossword()
crossword.add_words(["дума", "дім", "мул", "літо", "душа"])

print()
print (crossword.all_crossword)
for array in crossword.all_crossword[1]:
    print(str(array))

crossword.create_visualisation()
