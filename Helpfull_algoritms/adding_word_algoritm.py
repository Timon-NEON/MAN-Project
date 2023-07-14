"""DONE permutation algoritm, check compatibility of words, visualisation of crossword"""

from tkinter import *
from tkinter import font
import copy
import random


class Crossword:
    """Generate crossword puzzles"""

    def __init__(self):
        self.shown_index = 0

    def generate_all_crosswords (self, given_words:list):
        self.all_crossword = [0, []]
        length = 2
        alowed_values = given_words
        self.required_length = len(given_words)
        for word in alowed_values.copy():
            array = Crossword.__insert_word(self, word, False, 0, 0, [0, [], {}])
            alowed_values.remove(word)
            Crossword.__make_permutation_all_crosswords(self, length, array, alowed_values)
            alowed_values.append(word)


    def __make_permutation_all_crosswords (self, length:int, crossword:list, alowed_values:list):

        if length == self.required_length:
            word = alowed_values[0]
            exam_results = Crossword.__examine_word(self, word, copy.deepcopy(crossword))
            if bool(exam_results):
                for result in exam_results:
                    if result[0] == self.all_crossword[0]:
                        self.all_crossword[1].append(result.copy())
                    elif result[0] > self.all_crossword[0]:
                        self.all_crossword[0] = result[0]
                        self.all_crossword[1].clear()
                        self.all_crossword[1].append(result.copy())
        else:
            length += 1
            for word in alowed_values.copy():
                alowed_values.remove(word)
                exam_results = Crossword.__examine_word(self, word, copy.deepcopy(crossword))
                if bool(exam_results):
                    for result in exam_results:
                        Crossword.__make_permutation_all_crosswords(self, length, result, alowed_values)
                alowed_values.append(word)

    def generate_one_crossword(self, given_words:list, required_intersections):
        self.all_crossword = [0, []]
        self.required_intersections = required_intersections
        self.required_length = len(given_words)
        self.to_calculate = True
        length = 2
        alowed_values = []
        for temp in range(self.required_length):
            new_value = random.choice(given_words)
            alowed_values.append(new_value)
            given_words.remove(new_value)
        for word in alowed_values.copy():
            if self.to_calculate:
                array = Crossword.__insert_word(self, word, False, 0, 0, [0, [], {}])
                alowed_values.remove(word)
                Crossword.__make_permutation_one_crosswords(self, length, array, alowed_values)
                alowed_values.append(word)

    def __make_permutation_one_crosswords (self, length:int, crossword:list, alowed_values:list):
        if length == self.required_length and self.to_calculate:
            word = alowed_values[0]
            exam_results = Crossword.__examine_word(self, word, copy.deepcopy(crossword))
            if bool(exam_results):
                for result in exam_results:
                    if result[0] > self.required_intersections - 1 and self.to_calculate:
                        self.all_crossword[0] = result[0]
                        self.all_crossword[1].append(result.copy())
                        self.to_calculate = False
        elif self.to_calculate:
            length += 1
            for word in alowed_values.copy():
                if self.to_calculate:
                    alowed_values.remove(word)
                    exam_results = Crossword.__examine_word(self, word, copy.deepcopy(crossword))
                    if bool(exam_results):
                        for result in exam_results:
                            Crossword.__make_permutation_one_crosswords(self, length, result, alowed_values)
                    alowed_values.append(word)

    def __examine_word (self, word:str, crossword:list):
        possible_intersections = {}

        new_crosswords = []

        for coordinate, letter in crossword[2].items():                       #EXAM 0
            if letter in word:
                possible_intersections[coordinate] = letter

        for coordinate in possible_intersections.copy():      #EXAM 1
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
                        if temp_coordinate_y == len(word):
                            break
                        elif temp_coordinate_y == index:
                            temp_coordinate_y += 1
                            continue
                        while approve:
                            if (coordinate[0] + temp_coordinate_x, coordinate[1] - temp_coordinate_y + index) in crossword[2].keys():
                                if letter == crossword[2][(coordinate[0] + temp_coordinate_x, coordinate[1] - temp_coordinate_y + index)] and temp_coordinate_x == 0:
                                    intersections.append((coordinate[0] + temp_coordinate_x, coordinate[1] - temp_coordinate_y + index))
                                else:
                                    approve = False
                                    break
                            if temp_coordinate_x == 1:
                                break
                            temp_coordinate_x += 1

                        temp_coordinate_y += 1
                    if (coordinate[0], coordinate[1] + index + 1) in crossword[2].keys() or (coordinate[0], coordinate[1] - len(word) + index) in crossword[2].keys():
                        approve = False
                    if approve:
                        intersections.append(copy.deepcopy(coordinate))
                        temp_crossword = copy.deepcopy(crossword)
                        temp_crossword[1] += copy.deepcopy(intersections)
                        temp_crossword[0] += len(intersections.copy())
                        temp_crossword = Crossword.__insert_word(self, word, direction_vector, coordinate[0], coordinate[1] + index, copy.deepcopy(temp_crossword))
                        new_crosswords.append(temp_crossword.copy())
                    else:
                        continue

                else:
                    temp_coordinate_x = 0
                    while approve:
                        temp_coordinate_y = -1
                        if temp_coordinate_x == len(word):
                            break
                        elif temp_coordinate_x == index:
                            temp_coordinate_x += 1
                            continue
                        while approve:
                            if (coordinate[0] + temp_coordinate_x - index, coordinate[1] + temp_coordinate_y) in crossword[2].keys():
                                if letter == crossword[2][(coordinate[0] + temp_coordinate_x - index, coordinate[1] + temp_coordinate_y)] and temp_coordinate_y == 0:
                                    intersections.append((coordinate[0] + temp_coordinate_x - index, coordinate[1] + temp_coordinate_y))
                                else:
                                    approve = False
                                    break
                            if temp_coordinate_y == 1:
                                break
                            temp_coordinate_y += 1

                        temp_coordinate_x += 1
                    if (coordinate[0] - index - 1, coordinate[1]) in crossword[2].keys() or (coordinate[0] + len(word) - index, coordinate[1]) in crossword[2].keys():
                        approve = False
                    if approve:
                        intersections.append(copy.deepcopy(coordinate))
                        temp_crossword = copy.deepcopy(crossword)
                        temp_crossword[1] += copy.deepcopy(intersections)
                        temp_crossword[0] += len(intersections.copy())
                        temp_crossword = Crossword.__insert_word(self, word, direction_vector, coordinate[0] - index, coordinate[1], copy.deepcopy(temp_crossword))
                        new_crosswords.append(temp_crossword.copy())
                    else:
                        continue
        return new_crosswords


    def __insert_word (self, word : str, vector:bool, first_x : int, first_y: int, new_crossword:list):
        x = first_x
        y = first_y
        if vector == False:
            add_x = 1
            add_y = 0
        else:
            add_x = 0
            add_y = -1
        for letter in word:
            coordinate = (x, y)
            if not(coordinate in new_crossword[2].keys()):
                new_crossword[2][coordinate] = letter
            x += add_x
            y += add_y
        return new_crossword


    def create_visualisation (self):
        self.window = Tk()
        self.window.title('Тест кросворда')
        # root.geometry('700x300')

        self.crosword_interface = Frame()
        self.crosword_interface.grid(row=0, column=0)
        self.crossword_visual = Frame(master=self.crosword_interface)
        self.crossword_visual.grid(row=0, column=0, columnspan=2)

        if len(self.all_crossword[1]) != 0:
            self.shown_index = 0
            self.__create_crossword_structer(self.all_crossword[1][self.shown_index])
        else:
            self.__message_no_crosswords()

        btn_font = font.Font(size=16)
        if len(self.all_crossword[1]) > 1:
            button_forward = Button(master=self.crosword_interface, text="▶", width=3, height=1, font=btn_font,
                                    command=lambda: Crossword.__forward_visual_btncommand(self))
            button_forward.grid(row=1, column=1)
            button_backward = Button(master=self.crosword_interface, text="◀", width=3, height=1, font=btn_font,
                                     command=lambda: Crossword.__backward_visual_btncommand(self))
            button_backward.grid(row=1, column=0)

        self.window.mainloop()

    def __create_crossword_structer(self, crossword_displayed):
        max_x, min_x, max_y, min_y = Crossword.__get_size(self, crossword_displayed)
        # size_x = int (max_x - min_x)
        # size_y = int (max_y - min_y)
        for row, coordinate_y in enumerate(range(int(max_y), int(min_y) - 1, -1)):
            for column, coordinate_x in enumerate(range(int(min_x), int(max_x) + 1)):
                coordinate = (coordinate_x, coordinate_y)
                if coordinate in crossword_displayed[2].keys():
                    text = str(crossword_displayed[2][coordinate])
                else:
                    text = ''
                new_entry = Entry(master=self.crossword_visual, width=3)
                new_entry.grid(row=row, column=column)
                new_entry.insert(0, text)

    def __message_no_crosswords (self):
        message_label = Label(master=self.crossword_visual, text="Нажаль з наданих слів неможливо створити кросворди.\nСпробуйте інші слова")
        message_label.grid(row=0, column=0)

    def __clear_frame_crossword_visual(self):
        if self.crossword_visual.children:
            for widget in self.crossword_visual.winfo_children():
                widget.destroy()

    def __forward_visual_btncommand(self):
        if len(self.all_crossword[1]) - 1 > self.shown_index:
            self.shown_index += 1
            self.__clear_frame_crossword_visual()
            self.__create_crossword_structer(self.all_crossword[1][self.shown_index])

    def __backward_visual_btncommand(self):
        if self.shown_index > 0:
            self.shown_index -= 1
            self.__clear_frame_crossword_visual()
            self.__create_crossword_structer(self.all_crossword[1][self.shown_index])


    def __get_size (self, crossword:list):
        """get max_x, min_x, max_y, min_y coordinate from crossword"""

        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')
        for coordinate in crossword[2].keys():
            if coordinate[0] > max_x:
                max_x = coordinate[0]
            if coordinate[0] < min_x:
                min_x = coordinate[0]
            if coordinate[1] > max_y:
                max_y = coordinate[1]
            if coordinate[1] < min_y:
                min_y = coordinate[1]

        return max_x, min_x, max_y, min_y



#crossword_1 = Crossword()

#words = ["серветка", "словник", "букет"]

#crossword_1.add_words(words)

#crossword_1.create_visualisation()



