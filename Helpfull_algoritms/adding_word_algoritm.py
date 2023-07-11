"""DONE permutation algoritm, check compatibility of words, visualisation of crossword"""

from tkinter import *
import copy


class Crossword:

    def __init__(self):
        #self.crossword = [0, [], {}]
        self.shown_index = 0

    def add_words (self, given_words:list):
        self.all_crossword = [0, []]
        length = 2
        alowed_values = given_words
        self.required_length = len(given_words)
        for word in alowed_values.copy():
            array = Crossword.__insert_word(self, word, False, 0, 0, [0, [], {}])
            #print()
            #print(array)
            alowed_values.remove(word)
            Crossword.__make_permutation(self, length, array, alowed_values)
            alowed_values.append(word)


    def __make_permutation (self, length:int, crossword:list, alowed_values:list):

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
                        Crossword.__make_permutation(self, length, result, alowed_values)
                alowed_values.append(word)




    def __examine_word (self, word:str, crossword:list):
        possible_intersections = {}

        new_crosswords = []

        for coordinate, letter in crossword[2].items():                       #EXAM 0
            if letter in word:
                possible_intersections[coordinate] = letter

        #print("Exam 0: " + str (possible_intersections))

        for coordinate in possible_intersections.copy():      #EXAM 1
            if coordinate in crossword[1]:
                possible_intersections.pop(coordinate)

        #print("Exam 1: " + str (possible_intersections))

        for coordinate, letter in possible_intersections.items():
            index = -1
            if ((coordinate[0] - 1, coordinate[1]) in crossword[2].keys()    #EXAM 2
                or (coordinate[0] + 1, coordinate[1]) in crossword[2].keys()):
                direction_vector = True # 1 vertical vector; 0 horizontal vector
            else:
                direction_vector = False

            #print("Exam 2: " + str(direction_vector))

            for count in range(word.count(letter)):                      #EXAM3
                index = word.index(letter, index + 1)
                #print("index: " + str(index))
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
                            #print(coordinate, str(temp_coordinate_x), str(temp_coordinate_y))
                            if (coordinate[0] + temp_coordinate_x, coordinate[1] - temp_coordinate_y + index) in crossword[2].keys():
                                #print("1.1 Ok")
                                if letter == crossword[2][(coordinate[0] + temp_coordinate_x, coordinate[1] - temp_coordinate_y + index)] and temp_coordinate_x == 0:
                                    intersections.append((coordinate[0] + temp_coordinate_x, coordinate[1] - temp_coordinate_y + index))
                                    print("1.2 Ok")
                                else:
                                    print("1.2 NOT")
                                    approve = False
                                    #print("DisApprove True")
                                    break
                            if temp_coordinate_x == 1:
                                break
                            temp_coordinate_x += 1

                        temp_coordinate_y += 1
                    if (coordinate[0], coordinate[1] + index + 1) in crossword[2].keys() or (coordinate[0], coordinate[1] - len(word) + index) in crossword[2].keys():
                        approve = False
                    if approve:
                        intersections.append(coordinate)
                        temp_crossword = crossword.copy()
                        temp_crossword[1] += intersections.copy()
                        temp_crossword[0] += len(intersections.copy())
                        temp_crossword = Crossword.__insert_word(self, word, direction_vector, coordinate[0], coordinate[1] + index, temp_crossword)
                        print(crossword)
                        print(temp_crossword, word)
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
                                #print("2.1 OK")
                                if letter == crossword[2][(coordinate[0] + temp_coordinate_x - index, coordinate[1] + temp_coordinate_y)] and temp_coordinate_y == 0:
                                    print("2.2 OK")
                                    intersections.append((coordinate[0] + temp_coordinate_x - index, coordinate[1] + temp_coordinate_y))
                                else:
                                    print("2.2 NOT")
                                    approve = False
                                    break
                            if temp_coordinate_y == 1:
                                break
                            temp_coordinate_y += 1

                        temp_coordinate_x += 1
                    if (coordinate[0] - index - 1, coordinate[1]) in crossword[2].keys() or (coordinate[0] + len(word) - index, coordinate[1]) in crossword[2].keys():
                        approve = False
                    if approve:
                        intersections.append(coordinate)
                        temp_crossword = crossword.copy()
                        temp_crossword[1] += intersections.copy()
                        temp_crossword[0] += len(intersections.copy())
                        temp_crossword = Crossword.__insert_word(self, word, direction_vector, coordinate[0] - index, coordinate[1], temp_crossword)
                        print(crossword)
                        print(temp_crossword, word)
                        new_crosswords.append(temp_crossword.copy())
                    else:
                        continue
        #print("END")
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
            if coordinate in new_crossword[2].keys() and letter != new_crossword[2][coordinate]:
                print()
                print()
                print("BUG")
            if not(coordinate in new_crossword[2].keys()):
                new_crossword[2][coordinate] = letter
            x += add_x
            y += add_y
        #print("WOW: " + str(new_crossword))
        return new_crossword


    def forward_visual_command(self):
        if len(self.all_crossword[1]) - 1 > self.shown_index:
            self.shown_index += 1


    def create_visualisation (self):
        window = Tk()
        window.title('Тест кросворда')
        # root.geometry('700x300')

        crosword_interface = Frame()
        crosword_interface.grid(row=0, column=0)
        crossword_visual = Frame(master=crosword_interface)
        crossword_visual.grid(row=0, column=0)

        self.shown_index = 20
        crossword_shown = self.all_crossword[1][self.shown_index]

        max_x, min_x, max_y, min_y = Crossword.__get_size(self, crossword_shown)
        #size_x = int (max_x - min_x)
        #size_y = int (max_y - min_y)
        for row, coordinate_y in enumerate( range(int (max_y), int(min_y) - 1, -1)):
            for column, coordinate_x in enumerate( range(int (min_x), int(max_x) + 1)):
                coordinate = (coordinate_x, coordinate_y)
                if coordinate in crossword_shown[2].keys():
                    text = str (crossword_shown[2][coordinate])
                else:
                    text = ''
                new_entry = Entry(master=crossword_visual, width=3)
                new_entry.grid(row=row, column=column)
                new_entry.insert(0, text)

        #button_foward = Button(master=crosword_interface, text="▶")
        #button_foward.bind("<Button-1>", button_foward(self))
        #button_foward.grid(row=1, column=0)


        window.mainloop()

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

#print(crossword_1.crossword)
#print(crossword_1.max_x, crossword_1.max_y, crossword_1.min_x, crossword_1.min_y)


