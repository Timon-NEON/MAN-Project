import unittest
from adding_word_algoritm import Crossword

class Testing ():

    def test_examining_word (word:str, crossword:Crossword):
        """word check correctness test"""

        new_crossword = crossword.examine_word(word, crossword)
        print(new_crossword)


crossword = Crossword()
crossword.crossword = crossword.add_word("серветка", False, 0, 3, crossword.crossword)
crossword.crossword = crossword.add_word("словник", True, 0, 3, crossword.crossword)
crossword.crossword = crossword.add_word("букет", True, 5, 7, crossword.crossword)

print(crossword.crossword)

crossword.examine_word("воля", crossword.crossword)
crossword.print_all_variants()
