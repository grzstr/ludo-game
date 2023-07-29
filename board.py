from tkinter import *
import time
import random
from PIL import ImageTk, Image



board = Tk()
board.title("Ludo Board Game")

#Loading images
img_board = ImageTk.PhotoImage(Image.open("board.png"))
img_yellow_counter = ImageTk.PhotoImage(Image.open("yellow_counter.png"))
img_red_counter = ImageTk.PhotoImage(Image.open("red_counter.png"))
img_green_counter = ImageTk.PhotoImage(Image.open("green_counter.png"))
img_blue_counter = ImageTk.PhotoImage(Image.open("blue_counter.png"))

#Layout
board_label = Label(image=img_board).grid(row=1, column=1)


button_quit = Button(board, text = "Zakończ grę", command = board.quit).grid(column=2, row = 4)

