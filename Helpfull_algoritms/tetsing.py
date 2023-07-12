import unittest
import time
from adding_word_algoritm import Crossword

start_time = time.time()

crossword = Crossword()
crossword.add_words(["молоко", "ручка", "ластик", "чашка", "игла"])

print()
#print (crossword.all_crossword)
#for array in crossword.all_crossword[1]:
#    print(str(array))

end_time = time.time()

print(round(end_time - start_time, 2))

crossword.create_visualisation()
