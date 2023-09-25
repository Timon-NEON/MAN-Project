import unittest
import time
from crossword import Crossword

start_time = time.time() #початок прорахування часу

crossword = Crossword() #створення об'єкту класу Crossword


#crossword.read_file('source.txt', '—')


crossword.describe = {"тригонометрія": "наука, про трикутники", "матаналіз": "наука про аналіз даних", "алгебра": "наука про обчислювання", "логіка":"мистецтво думати", "комбінаторика":"наука про випадки", "топологія":"наука про просторове уявлення", "статистика":"наука про вивчення процесів"}



crossword.generate(30, -1)

end_time = time.time() #кінець прорахування часу
print("Час генерації: ", round(end_time - start_time, 2))


crossword.create_window()

#crossword.draw(15)

end_time = time.time() #кінець прорахування часу

print("Час виконання програми: ", round(end_time - start_time, 2))