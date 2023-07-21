import unittest
import time
from adding_word_algoritm import Crossword

start_time = time.time()

crossword = Crossword()
crossword.generate_one_crossword(["нафта", "метан", "жири", "вуглеводи", "алкани",  "спирти",
                                  "кислоти", "естери", "білки", "карбон", "оксиген",
                                  "гідроген"], 11)

#crossword.generate_all_crosswords(["молоко", "свиня", "яблоко"])

end_time = time.time()

print(round(end_time - start_time, 2))

crossword.create_visualisation()
