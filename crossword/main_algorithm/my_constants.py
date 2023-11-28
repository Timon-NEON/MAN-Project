import platform

#crossword_app_PATH = '/home/timon/Github/crossword_app/crossword_app/MAN-Project/'
if platform.system() == 'Windows':
    crossword_app_PATH = 'D:/Coding/PycharmProjects/MAN_clone/MAN-Project/'
else:
    crossword_app_PATH = '/home/crosswordsUa/MAN-Project/'

read_describe_separator = '\n'
read_pair_separator = '-'
draw_ratio_word_in_row = 2