import unittest
import time
from crossword import Crossword

word = ''
describe = ''
crossword = Crossword()

#while True:
#    word = input()
#    describe = input()
#    if word == 'q':
#        break
#    else:
#        crossword.describe[word] = describe
#        print(crossword.describe)

crossword.describe = {"тригонометрія": "наука, про трикутники", "матаналіз": "наука про аналіз даних", "алгебра": "наука про обчислювання", "логіка":"мистецтво думати", "комбінаторика":"наука про випадки", "топологія":"наука про просторове уявлення", "статистика":"наука про вивчення процесів"}


start_time = time.time()


crossword.generate_one_crossword(1500)

#crossword.generate_all_crosswords(["молоко", "свиня", "яблоко"])

end_time = time.time()

#print (crossword.all_crosswords)
#for i in crossword.all_crosswords[1]:
#    print(i)
#print(len(crossword.all_crosswords[1]))
#print(round(end_time - start_time, 2))

#crossword.create_window()

#crossword.CreateInterface.create_visualisation()
crossword.all_crosswords[1] = [crossword.all_crosswords[2]]
print(crossword.all_crosswords[2])
print(crossword.describe)
crossword.create_window()
