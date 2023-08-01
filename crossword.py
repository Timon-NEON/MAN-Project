"""DONE permutation algoritm, check compatibility of words, visualisation of crossword"""

from tkinter import *
from tkinter import font
import copy
import random
import time


class Crossword:
    """Generate crossword puzzles"""
    #structure of list of crossoword: [ number of intersections (int type), [ intersections of crossword (tuple type) ], { coordinate (tupple type) : letter (string type) } ]

    def __init__(self):
        self.describe = {}
        self.all_crosswords = [0, [], {}, {}]



    def generate_all_crosswords (self, given_words:list):
        """Main public function that make preparing and start generate all variant of crosswords"""

        self.all_crosswords = [0, []] #main list that keeps 2 values: 1st (int value) shows maximum naumber of intersections, 2nd (list value) keeps all crosswords that have intersections value that is equal to 1st value of self.all_crosswords
        self.required_length = len(given_words)  #preparing of the parametr of required length of crossword for permutation function
        length = 2 #preparing of length parametr of crossword for permutation function
        alowed_values = given_words #list that keeps words that should be added to crossword
        for word in alowed_values.copy(): #start permutation
            array = Crossword.__insert_word(self, word, False, 0, 0, [0, [], {}]) #add first word to crossword
            alowed_values.remove(word)
            Crossword.__make_permutation_all_crosswords(self, length, array, alowed_values)
            alowed_values.append(word)

    def __make_permutation_all_crosswords (self, length:int, crossword:list, alowed_values:list):
        """Recursive private function that generate all variants of crosswords"""

        if length == self.required_length: #checking that the crossword is almost done
            word = alowed_values[0]
            exam_results = Crossword.__examine_word(self, word, copy.deepcopy(crossword)) #checking that word can be added to crossword
            if bool(exam_results): #checking that list keeps values (it can be empty)
                for result in exam_results:
                    if result[0] == self.all_crosswords[0]: #checking that crossword have the same intersections value like the values of intersections from self.all_crosswords
                        self.all_crosswords[1].append(result.copy()) #adding new crossword to the self.all_crosswords
                    elif result[0] > self.all_crosswords[0]: #checking that crossword have the bigger intersections value than the value of intersections from self.all_crosswords
                        self.all_crosswords[0] = result[0] #updating the values of intersection self.all_crosswords
                        self.all_crosswords[1].clear() #deleting all variants of crosswords in self.all_crosswords (they have the less value of intersections)
                        self.all_crosswords[1].append(result.copy()) #adding new crossword to the self.all_crosswords
        else:
            length += 1
            for word in alowed_values.copy(): #adding to crossword words from alowed_values
                alowed_values.remove(word)
                exam_results = Crossword.__examine_word(self, word, copy.deepcopy(crossword)) #checking that word can be added to crossword
                if bool(exam_results): #checking that list keeps values (it can be empty)
                    for result in exam_results:
                        Crossword.__make_permutation_all_crosswords(self, length, result, alowed_values) #making recursive to adding all words to crossword
                alowed_values.append(word)

    def generate_one_crossword(self, required_options: int):
        """Main public function that make preparing and start generate for one variant of crossword"""
        given_words = list(self.describe.keys())
        self.all_crosswords = [0, []] #main list that keeps 2 values: 1st (int value) shows maximum naumber of intersections, 2nd (list value) keeps all crosswords that have intersections value that is equal to 1st value of self.all_crosswords
        self.required_options = required_options #parameter keeps number of required options of crossword for searching best variant
        self.required_length = len(given_words) #preparing of the parametr of required length of crossword for permutation function

        start_time = time.time()
        for i in range(self.required_options):
            if time.time() - start_time < 10:
                self.to_calculate = True  # preparing of boolean parametr for permutation function which determines whether the program still need to look for acceptable variant of crossword
                length = 2  # preparing of length parametr of crossword for permutation function
                alowed_values = []  # list that keeps words that should be added to crossword
                given_words = list(self.describe.keys())

                for temp in range(self.required_length): #generating random word order for alowed_values (for making different crosswords from the same input words)
                    new_value = random.choice(given_words)
                    alowed_values.append(new_value)
                    given_words.remove(new_value)

                for word in alowed_values.copy(): #start permutation
                    if self.to_calculate:
                        array = Crossword.__insert_word(self, word, False, 0, 0, [0, [], {}, {}])
                        alowed_values.remove(word)
                        Crossword.__make_permutation_one_crosswords(self, length, array, alowed_values)
                        alowed_values.append(word)
            else:
                break
        #analysis
        for count in range (len(self.all_crosswords[1])):
            points = self.__get_size_point(self.all_crosswords[1][count])
            self.all_crosswords[1][count].append(points)
            if count != 0:
                if points < self.all_crosswords[2][4]:
                    self.all_crosswords[2] = self.all_crosswords[1][count]
            else:
                self.all_crosswords.append(self.all_crosswords[1][count])


    def __make_permutation_one_crosswords (self, length:int, crossword:list, alowed_values:list):
        """Recursive private function that generate one variant of crossword"""

        if length == self.required_length and self.to_calculate: #checking that the crossword is almost done and whether the program still need to look for acceptable variant of crossword
            word = alowed_values[0]
            exam_results = Crossword.__examine_word(self, word, copy.deepcopy(crossword)) #checking that word can be added to crossword
            if bool(exam_results): #checking that list keeps values (it can be empty)
                for result in exam_results:
                    if self.to_calculate:
                        self.all_crosswords[0] = result[0]
                        self.all_crosswords[1].append(result.copy())
                        self.to_calculate = False  # change search status
        elif self.to_calculate: #checking whether the program still need to look for acceptable variant of crossword
            length += 1
            for word in alowed_values.copy(): #adding to crossword words from alowed_values
                if self.to_calculate:
                    alowed_values.remove(word)
                    exam_results = Crossword.__examine_word(self, word, copy.deepcopy(crossword))
                    if bool(exam_results): #checking that list keeps values (it can be empty)
                        for result in exam_results:
                            Crossword.__make_permutation_one_crosswords(self, length, result, alowed_values) #making recursive to adding all words to crossword
                    alowed_values.append(word)

    def __examine_word (self, word:str, crossword:list):
        """Auxiliary private function that checks whether a word can be added to a given crossword.
        If it`s true, function return list with all variants of crosswords with a new word.
        Else function return empty list"""

        possible_intersections = {} #dictionary with key (tuple type) is coordinate of letter and values (string type) is letter, that coincides with letter in crossword
        new_crosswords = [] #list that keeps all variants of crosswords with a new word

        for coordinate, letter in crossword[2].items(): #preparing possible intersections
            if letter in word:
                possible_intersections[coordinate] = letter

        for coordinate in possible_intersections.copy(): #CHECKING 1: removing from possible intersections a intersrction if this intersection have crossword (second value keeps all crossword`s intersections)
            if coordinate in crossword[1]:
                possible_intersections.pop(coordinate)

        for coordinate, letter in possible_intersections.items():
            index = -1
            if ((coordinate[0] - 1, coordinate[1]) in crossword[2].keys() #CHECKING 2: definition of the derection vector of word
                or (coordinate[0] + 1, coordinate[1]) in crossword[2].keys()):
                direction_vector = True # 1 vertical vector; 0 horizontal vector
            else:
                direction_vector = False

            for count in range(word.count(letter)): #CHECKING 3: checking for empty cells next to those cells in which the program wants to add a word
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
        return new_crosswords #returning answer of function

    def __insert_word (self, word: str, vector: bool, first_x: int, first_y: int, new_crossword: list):
        """Auxiliary private function that insert a word into given crossword by given parametrs and return it"""

        x = first_x #start x coordinate
        y = first_y #start y coordinate
        if vector: #checking vector and giving instructions
            add_x = 0
            add_y = -1
        else:
            add_x = 1
            add_y = 0
        for letter in word: #inserting a word into a given crossword
            coordinate = (x, y)
            if not(coordinate in new_crossword[2].keys()):
                new_crossword[2][coordinate] = letter
            x += add_x
            y += add_y
        new_crossword[3][word] = [(first_x, first_y), vector]
        return new_crossword #returning answer of function

    def __get_size_point (self, crossword:list):
        """Auxiliary private function that give max_x, min_x, max_y, min_y coordinate from crossword"""

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
        size_x = max_x - min_x
        size_y = max_y - min_y

        size_point = ((size_x + size_y) / 2) * ((max(size_x, size_y) ** (1/4)) / (min(size_x, size_y) ** (1/4)))
        return size_point

    def create_window(self):
        self.CreateInterface = CreateInterface(self.all_crosswords)
        self.CreateInterface.create_visualisation()




class CreateInterface:

    def __init__(self, all_crosswords):
        self.all_crosswords = all_crosswords

    def create_visualisation (self):
        """Main public function that make visualisation of crossword"""

        self.window = Tk() #main window
        self.window.title('Crossword puzzle')

        self.crosword_interface = Frame() #frame that keeps buttons and frame with crossword
        self.crosword_interface.grid(row=0, column=0)
        self.crossword_visual = Frame(master=self.crosword_interface) #frame that keeps crossword
        self.crossword_visual.grid(row=0, column=0, columnspan=2)

        if len(self.all_crosswords[1]) != 0: #checking that availability of variants of crosswords
            self.shown_index = 0
            self.__create_crossword_structer(self.all_crosswords[1][self.shown_index]) #creating crossword structure
        else:
            self.__message_no_crosswords() #outputting message about none variants of crosswords

        btn_font = font.Font(size=16) #creating font for buttons
        if len(self.all_crosswords[1]) > 1: #checking that crossword have more than 1 variant for buttons
            button_forward = Button(master=self.crosword_interface, text="▶", width=3, height=1, font=btn_font,
                                    command=lambda: CreateInterface.__forward_visual_btncommand(self))
            button_forward.grid(row=1, column=1)
            button_backward = Button(master=self.crosword_interface, text="◀", width=3, height=1, font=btn_font,
                                     command=lambda: CreateInterface.__backward_visual_btncommand(self))
            button_backward.grid(row=1, column=0)

        self.window.mainloop()

    def __create_crossword_structer(self, crossword_displayed):
        """Auxiliary private function that create crossword in frame self.crossword_visual"""

        max_x, min_x, max_y, min_y = CreateInterface.__get_size(self, crossword_displayed)
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

    def __get_size (self, crossword:list):
        """Auxiliary private function that give max_x, min_x, max_y, min_y coordinate from crossword"""

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

    def __message_no_crosswords (self):
        """Auxiliary private function that output message about none variants of crosswords in frame self.crossword_visual"""

        message_label = Label(master=self.crossword_visual, text="Нажаль з наданих слів неможливо створити кросворди.\nСпробуйте інші слова")
        message_label.grid(row=0, column=0)

    def __forward_visual_btncommand(self):
        """Auxiliary private function that create after pressed button_forward next crossword if it exist"""

        if len(self.all_crosswords[1]) - 1 > self.shown_index:
            self.shown_index += 1
            self.__clear_frame_crossword_visual()
            self.__create_crossword_structer(self.all_crosswords[1][self.shown_index])

    def __backward_visual_btncommand(self):
        """Auxiliary private function that create after pressed button_backward previos crossword if it exist"""

        if self.shown_index > 0:
            self.shown_index -= 1
            self.__clear_frame_crossword_visual()
            self.__create_crossword_structer(self.all_crosswords[1][self.shown_index])

    def __clear_frame_crossword_visual(self):
        """Auxiliary private function that clearing frame self.crossword_visual before creating new crossword"""

        if self.crossword_visual.children:
            for widget in self.crossword_visual.winfo_children():
                widget.destroy()