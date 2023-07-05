from tkinter import *
import math
import unittest


class Crossword:

    def __init__(self):
        self.crossword = [0, [], {}]

        self.min_x, self.min_y = float('inf'), float('inf')
        self.max_x, self.max_y = float('-inf'), float('-inf')

    def add_words (self, given_words:list):
        self.all_crossword = [0, []]
        array = [0, [], {}]
        length = 1
        alowed_values = given_words
        self.required_length = len(given_words)
        Crossword.make_permutation(self, length, array, alowed_values)


    def make_permutation (self, length:int, crossword:list, alowed_values:list):
        if length == self.required_length :
            word = alowed_values[0]
            exam_results = Crossword.examine_word(self, word, crossword)
            if bool(exam_results):
                for result in exam_results:
                    if result[0] == self.all_crossword[0]:
                        self.all_crossword.append(result.copy())
                    elif result[0] > self.all_crossword[0]:
                        self.all_crossword[1].clear()
                        self.all_crossword.append(result.copy())
        else:
            length += 1
            for word in alowed_values.copy():
                alowed_values.remove(word)
                exam_results = Crossword.examine_word(self, word, crossword)
                if bool(exam_results):
                    for result in exam_results:
                        Crossword.make_permutation(self, length, result, alowed_values)
                alowed_values.append(word)




    def examine_word (self, word:str, crossword:list):
        possible_intersections = {}

        new_crosswords = []

        for coordinate, letter in crossword[2].items():                       #EXAM 0
            if letter in word:
                possible_intersections[coordinate] = letter

        for coordinate in possible_intersections:      #EXAM 1
            if coordinate in crossword[1]:
                possible_intersections.pop(coordinate)

        for coordinate, letter in possible_intersections.items():
            index = -1
            if ((coordinate[0] - 1, coordinate[1]) in crossword[2].keys()    #EXAM 2
                or (coordinate[0] + 1, coordinate[1]) in crossword[2].keys()):
                direction_vector = True # 1 vertical vector; 0 horizontal vector
            else:
                direction_vector = False

            for count in range(word.count(letter)):                      #EXAM3
                index = word.index(letter, index + 1)
                approve = True
                intersections = []
                if direction_vector:
                    temp_coordinate_y = 0
                    while approve:
                        temp_coordinate_x = -1
                        if temp_coordinate_y == index:
                            temp_coordinate_y += 1
                            continue
                        while approve:
                            if ((coordinate[0] + temp_coordinate_x,
                                 coordinate[1] - temp_coordinate_y)) in crossword[2].keys():
                                if letter == crossword[2][(coordinate[0] + temp_coordinate_x, coordinate[1] - temp_coordinate_y)] and temp_coordinate_x == 0:
                                    intersections.append((coordinate[0] - temp_coordinate_x, coordinate[1] + temp_coordinate_y))
                                else:
                                    approve = False
                                    break
                            if temp_coordinate_x == 1:
                                break
                            temp_coordinate_x += 1
                        if temp_coordinate_y == len(word) - 1:
                            break
                        temp_coordinate_y += 1

                    if approve:
                        temp_crossword = crossword
                        temp_crossword[1].append(intersections)
                        temp_crossword[0] += len(intersections)
                        temp_crossword = Crossword.insert_word(self, word, direction_vector, coordinate[0], coordinate[1], temp_crossword)
                        new_crosswords.append(temp_crossword)
                    else:
                        continue

                else:
                    temp_coordinate_x = 0
                    while approve:
                        temp_coordinate_y = -1
                        if temp_coordinate_x == index:
                            temp_coordinate_x += 1
                            continue
                        while approve:
                            if ((coordinate[0] - temp_coordinate_x,
                                 coordinate[1] + temp_coordinate_y)) in crossword[2].keys():
                                if letter == crossword[2][(coordinate[0] - temp_coordinate_x, coordinate[1] + temp_coordinate_y)] and temp_coordinate_y == 0:
                                    intersections.append((coordinate[0] - temp_coordinate_x, coordinate[1] + temp_coordinate_y))
                                else:
                                    approve = False
                                    break
                            if temp_coordinate_y == 1:
                                break
                            temp_coordinate_y += 1
                        if temp_coordinate_x == len(word) - 1:
                            break
                        temp_coordinate_x += 1

                    if approve:
                        temp_crossword = crossword
                        temp_crossword[1].append(intersections)
                        temp_crossword[0] += len(intersections)
                        temp_crossword = Crossword.insert_word(self, word, direction_vector, coordinate[0], coordinate[1], temp_crossword)
                        new_crosswords.append(temp_crossword)
                    else:
                        print(0)
                        continue
        print("END")
        return new_crosswords


    def insert_word (self, word : str, vector:bool, first_x : int, first_y: int, crossword:list):
        x = first_x
        y = first_y
        if vector == False:
            add_x = 1
            add_y = 0
            if x + len(word) - 1 > self.max_x: self.max_x = x + len(word) - 1
            if x < self.min_x: self.min_x = x
        else:
            add_x = 0
            add_y = -1
            if y > self.max_y: self.max_y = y
            if y - len(word) + 1  < self.min_y: self.min_y = y - len(word) + 1
        for letter in word:
            coordinate = (x, y)
            if not(coordinate in crossword[2].keys()):
                crossword[2][coordinate] = letter
            x += add_x
            y += add_y
        return crossword


    #def forward_visual_command (self):
    #    if len(self.new_crosswords)
#
    #    for row, coordinate_y in enumerate( range(int (self.max_y), int(self.min_y) - 1, -1)):
    #        print(row, coordinate_y)
    #        for column, coordinate_x in enumerate( range(int (self.min_x), int(self.max_x) + 1)):
    #            coordinate = (coordinate_x, coordinate_y)
    #            if coordinate in self.crossword_shown[2].keys():
    #                text = self.crossword_shown[2][coordinate]
    #            else:
    #                text = ''
    #            new_entry = Entry(crossword_visual, width=3)
    #            new_entry.grid(row=row, column=column)
    #            new_entry.insert(0, text)


    def create_visualisation (self, crossword_shown):
        window = Tk()
        window.title('Тест кросворда')
        # root.geometry('700x300')

        crosword_interface = Frame(window)
        crossword_visual = Frame(crosword_interface)

        size_x = int (self.max_x - self.min_x)
        size_y = int (self.max_y - self.min_y)
        print(size_x, size_y)
        for row, coordinate_y in enumerate( range(int (self.max_y), int(self.min_y) - 1, -1)):
            print(row, coordinate_y)
            for column, coordinate_x in enumerate( range(int (self.min_x), int(self.max_x) + 1)):
                coordinate = (coordinate_x, coordinate_y)
                if coordinate in crossword_shown[2].keys():
                    text = crossword_shown[2][coordinate]
                else:
                    text = ''
                new_entry = Entry(crossword_visual, width=3)
                new_entry.grid(row=row, column=column)
                new_entry.insert(0, text)

        #button_foward = Button(crosword_interface, text="▶", command=Crossword.forward_visual_command)

        window.mainloop()

#crossword_1 = Crossword()

#words = ["серветка", "словник", "букет"]

#crossword_1.add_words(words)

#crossword_1.create_visualisation()

#print(crossword_1.crossword)
#print(crossword_1.max_x, crossword_1.max_y, crossword_1.min_x, crossword_1.min_y)


