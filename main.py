from tkinter import *
import math


class Crosswod:

    def __init__(self):
        self.crossword = {}
        self.min_x, self.min_y = float('inf'), float('inf')
        self.max_x, self.max_y = float('-inf'), float('-inf')

    def add_word (self, word : str, vector : str, first_x : int, first_y: int):
        x = first_x
        y = first_y
        if vector == "right":
            add_x = 1
            add_y = 0
            if x + len(word) - 1 > self.max_x: self.max_x = x + len(word) - 1
            if x < self.min_x: self.min_x = x
        elif vector == "down":
            add_x = 0
            add_y = -1
            if y > self.max_y: self.max_y = y
            if y - len(word) + 1  < self.min_y: self.min_y = y - len(word) + 1
        for letter in word:
            coordinate = (x, y)
            if not(coordinate in self.crossword.keys()):
                self.crossword[coordinate] = letter
            x += add_x
            y += add_y

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
                if coordinate in self.crossword.keys():
                    text = self.crossword[coordinate]
                else:
                    text = ''
                new_entry = Entry(self.crossword_visual, width=3)
                new_entry.grid(row=row, column=column)
                new_entry.insert(0, text)

        self.crossword_visual.mainloop()

crossword_1 = Crosswod()

crossword_1.add_word("серветка", "right", 0, 3)
crossword_1.add_word("словник", "down", 0, 3)
crossword_1.add_word("букет", "down", 5, 7)

crossword_1.create_visualisation()

print(crossword_1.crossword)
print(crossword_1.max_x, crossword_1.max_y, crossword_1.min_x, crossword_1.min_y)


