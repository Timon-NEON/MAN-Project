from tkinter import *
import math


class Crosswod:

    def __init__(self):
        self.crossword = [0, [], {}]

        self.possible_intersections = {}
        self.direction_vector = bool        # 1 vertical vector; 0 horizontal vector
        self.index = -1

        self.min_x, self.min_y = float('inf'), float('inf')
        self.max_x, self.max_y = float('-inf'), float('-inf')

    def add_words (self, given_words:list):
        array = [0, [], {}]
        length = 1
        alowed_values = given_words
        self.required_length = len(given_words)
        Crosswod.make_permutation(self, length, array, alowed_values)


    def make_permutation (self, length, crossword, alowed_values):
        if length == self.required_length :
            for word in alowed_values:
                exam_result = Crosswod.examine_word(self, word, crossword)
                if bool(exam_result):
                    pass




    def examine_word (self, word:str, crossword:list):
        self.possible_intersections = {}
        for coordination, letter in crossword:                       #EXAM 0
            if letter in word:
                self.possible_intersections[coordination] = letter

        for coordination in self.possible_intersections:      #EXAM 1
            if coordination in word[1]:
                self.possible_intersections.pop(coordination)

        for coordination, letter in self.possible_intersections.items():
            if ((coordination[0] - 1, coordination[1]) in crossword[2].keys() #EXAM 2
                or (coordination[0] + 1, coordination[1]) in crossword[2].keys()):
                self.direction_vector = True
            else:
                self.direction_vector = False

            for temp in range(word.count(letter)):                      #EXAM3
                self.index = word.index(letter, self.index + 1)
                if self.direction_vector:
                    pass #acrion1
                else:
                    pass #action2










    def create_visualisation (self):
        self.crossword_visual = Tk()
        self.crossword_visual.title('Тест кросворда')
        # root.geometry('700x300')

        size_x = int ( self.max_x - self.min_x)
        size_y = int (self.max_y - self.min_y)
        print(size_x, size_y)
        for row, coordinate_y in enumerate( range(int (self.max_y), int(self.min_y) - 1, -1)):
            print(row, coordinate_y)
            for column, coordinate_x in enumerate( range(int (self.min_x), int(self.max_x) + 1)):
                coordinate = (coordinate_x, coordinate_y)
                if coordinate in self.crossword[2].keys():
                    text = self.crossword[2][coordinate]
                else:
                    text = ''
                new_entry = Entry(self.crossword_visual, width=3)
                new_entry.grid(row=row, column=column)
                new_entry.insert(0, text)

        self.crossword_visual.mainloop()

crossword_1 = Crosswod()

words = ["серветка", "словник", "букет"]

crossword_1.add_words(words)

crossword_1.create_visualisation()

print(crossword_1.crossword)
print(crossword_1.max_x, crossword_1.max_y, crossword_1.min_x, crossword_1.min_y)


