from tkinter import *
import random
from PIL import ImageTk, Image
import sqlite3


class Counter:
    def __init__(self, color, number, dock_pos):
        self.color = color
        self.position = []
        self.number = number
        self.is_inside = True
        self.dock_pos = dock_pos
        self.position = list(self.dock_pos[color][number-1])
        
    def set_dock_pos(self):
        self.position = list(self.dock_pos[color][number-1])

class Player:
    def __init__(self, color, dock_pos, nickname = "Player"):
        self.counter_number = 4
        self.counters = []
        self.chosen_counter = 1
        self.color = color
        self.finished_the_game = False
        self.podium = 0
        self.in_dock = 4
        self.dock_pos = dock_pos
        self.points = 100
        self.nickname = nickname
        self.roll = random.randint(1, 6)

        for i in range(1, 5):
            self.counters.append(Counter(color, i, self.dock_pos))

class Virtual_Player(Player):
    def virtual_move(self):
        self.chosen_counter = random.randint(1, 4)

class Ludo:
    def __init__(self):
        self.virtual_player = []
        self.colors = ["red", "yellow", "blue", "green"]
        self.used_colors = []
        self.winners = []
        self.real_player = []
        self.chosen_color = ""
        self.select = 1
        self.continue_game = True
        self.hide_roll_button = NORMAL
        self.hide_select_button = DISABLED
        self.dice_unknown = True
        self.start_game = False
        self.chosen_type = ""
        self.chosen_index = 0
        self.chosen_language = 0
        self.show_counters_pos = False
        
        self.start_pos = {"red":(1, 5), 
                          "blue":(7, 1), 
                          "green":(11, 7), 
                          "yellow":(5, 11) }

        self.dock_pos = {"red":((2,2),(3,2),(2,3),(3,3)), 
                          "blue":((9,2),(10,2),(9,3),(10,3)), 
                          "green":((9,9),(10,9),(9,10),(10,10)), 
                          "yellow":((2,9),(3,9),(2,10),(3,10)) }

        self.end_pos = {"red":(5, 6), 
                         "blue":(6, 5), 
                         "green":(7, 6), 
                         "yellow":(6, 7) }

        self.languages = {"languages": ("English", "polski"),
                            "lan_yes": ("Yes", "Tak"),
                            "lan_no": ("No", "Nie"), 
                            "colors": (("red", "blue", "green", "yellow"),("czerwony", "niebieski", "zielony", "żółty"))}

    def add_player_to_save(self, c, player, type):
        c.execute("""INSERT INTO players VALUES (
            :nickname, 
            :color, 
            :type, 
            :points, 
            :podium, 
            :counter_1_pos_x, 
            :counter_1_pos_y, 
            :counter_2_pos_x,
            :counter_2_pos_y,
            :counter_3_pos_x,
            :counter_3_pos_y,
            :counter_4_pos_x,
            :counter_4_pos_y)""", 
                {
                    "nickname": player.nickname, 
                    "color": player.color, 
                    "type": type, 
                    "points": player.points, 
                    "podium": player.podium, 
                    "counter_1_pos_x integer": player.counters[0].position[0], 
                    "counter_1_pos_y integer": player.counters[0].position[1], 
                    "counter_2_pos_x integer": player.counters[1].position[0],
                    "counter_2_pos_y integer": player.counters[1].position[1],
                    "counter_3_pos_x integer": player.counters[2].position[0],
                    "counter_3_pos_y integer": player.counters[2].position[1],
                    "counter_4_pos_x integer": player.counters[3].position[0],
                    "counter_4_pos_y integer": player.counters[3].position[1]
                }
                )       
        c.commit()

    def save_game(self):
        save = sqlite3.connect('saved_game.db')
        c = save.cursor()
        c.execute("""CREATE TABLE if not exists players (
                nickname text,
                color text,
                type text,
                points integer,
                podium integer,
                counter_1_pos_x integer,
                counter_1_pos_y integer,
                counter_2_pos_x integer,
                counter_2_pos_y integer,
                counter_3_pos_x integer,
                counter_3_pos_y integer,
                counter_4_pos_x integer,
                counter_4_pos_y integer
                )""")    
        
        for player in self.real_player:
            self.add_player_to_save(c, player, "real")
        for player in self.virtual_player:
            self.add_player_to_save(c, player, "real")

        c.close()

    def update_dice_img(self):
        if self.chosen_type == "real":
            #roll_label = Label(text=self.real_player[self.chosen_index].roll)
            roll_label = Label(image=dice[self.real_player[self.chosen_index].roll - 1])
            self.hide_roll_button = NORMAL
        else:
            #roll_label = Label(text=self.virtual_player[self.chosen_index].roll)
            roll_label = Label(image=dice[self.virtual_player[self.chosen_index].roll - 1])
            self.hide_roll_button = DISABLED

        if self.dice_unknown == True:
            roll_label = Label(image=dice_unknown)
        
        roll_label.grid(column=0, row=2)

    def next_color(self):
        if self.chosen_color == "":
            if len(self.real_player) > 0:
                self.chosen_color = self.real_player[0].color
                self.chosen_type = "real"
            else:
                self.chosen_color = self.virtual_player[0].color
                self.chosen_type = "virtual"
        else:
            #Which player has chosen color
            for i in range(len(self.real_player)):
                if self.real_player[i].color == self.chosen_color:
                    index = i
            for i in range(len(self.virtual_player)):
                if self.virtual_player[i].color == self.chosen_color:
                    index = i + 10

            #Next color
            if index < 10:
                if index + 1 < len(self.real_player):
                    #index += 1
                    self.chosen_color = self.real_player[index+1].color
                    self.chosen_type = "real"
                    self.chosen_index = index + 1
                elif len(self.virtual_player) > 0:
                    #index = 10
                    self.chosen_color = self.virtual_player[0].color
                    self.chosen_type = "virtual"
                    self.chosen_index = 0
                else:
                    self.chosen_color = self.real_player[0].color
                    self.chosen_type = "real"
                    self.chosen_index = 0
                    #index = 0
            else:
                if index + 1 < len(self.virtual_player) + 10:
                    #index += 1
                    self.chosen_color = self.virtual_player[index-9].color
                    self.chosen_index = index - 9
                    self.chosen_type = "virtual"
                elif len(self.real_player) > 0:
                    #index = 0
                    self.chosen_color = self.real_player[0].color
                    self.chosen_index = 0
                    self.chosen_type = "real"
                else:
                    #index = 10
                    self.chosen_color = self.virtual_player[0].color
                    self.chosen_index = 0
                    self.chosen_type = "virtual"
            
            #Player ended the game
            if self.chosen_type == "real":
                if self.real_player[self.chosen_index].podium != 0 and self.real_player[self.chosen_index].podium != len(self.used_colors):
                    self.next_color()
            else:
                if self.virtual_player[self.chosen_index].podium != 0 and self.virtual_player[self.chosen_index].podium != len(self.used_colors):
                    self.next_color()

    def add_player(self, color, is_real, nickname, window):
        if len(self.real_player)+len(self.virtual_player) < 4:
            if color in self.colors:
                if color in self.used_colors:
                    print("This color has already been used!")
                    Error_label = Label(window, text="This color has already been used!").grid(row=5, column=0, columnspan=2)
                else:
                    self.used_colors.append(color)
                    if is_real == True:
                        self.real_player.append(Player(color, self.dock_pos, nickname))
                    else:
                        self.virtual_player.append(Virtual_Player(color, self.dock_pos, nickname))
            else:
                Error_label = Label(window, text="Wrong color!").grid(row=5, column=0, columnspan=2)
        else:
            Error_label = Label(window, text="There are already four players!").grid(row=5, column=0, columnspan=2)

        for x in range(len(self.real_player)):
            players_number_label = Label(window, text=f"[{x + 1}]: {self.real_player[x].nickname}, Real, {self.real_player[x].color}")
            players_number_label.grid(row=6+x, column=0, columnspan=2)

        for y in range(len(self.virtual_player)):
            virtual_number_label = Label(window, text=f"[{y+x}]: {self.virtual_player[y].nickname}, Virtual {self.virtual_player[y].color}")
            virtual_number_label.grid(row=6+x+y, column=0, columnspan=2)

    def dice(self):
        roll = random.randint(1, 6)
        if self.chosen_type == "real":
            self.real_player[self.chosen_index].roll = roll
        else:
            self.virtual_player[self.chosen_index].roll = roll
        self.dice_unknown = False
        self.update_dice_img()
        self.hide_select_button = NORMAL
        #self.hide_roll_button = DISABLED
        self.hide_roll_button = NORMAL
        self.side_panel()

    def kill(self):
        for player in self.real_player:
            if player.color != self.real_player[self.chosen_index].color and self.chosen_type == "real":
                for evil_counter in player.counters:
                    for good_counter in self.real_player[self.chosen_index].counters:
                        if evil_counter.position[0] == good_counter.position[0] and evil_counter.position[1] == good_counter.position[1] and evil_counter.color != good_counter.color and evil_counter.position[0] != self.start_pos[evil_counter.color][0] and evil_counter.position[1] != self.start_pos[evil_counter.color][1]:
                                    evil_counter.position[0] = self.dock_pos[evil_counter.color][evil_counter.number-1][0]
                                    evil_counter.position[1] = self.dock_pos[evil_counter.color][evil_counter.number-1][1]
                                    #POINTS
                                    player.points -= 15
                                    self.real_player[self.chosen_index].points += 20
        for player in self.virtual_player:
            if player.color != self.virtual_player[self.chosen_index].color and self.chosen_type == "virtual":
                for evil_counter in player.counters:
                    for good_counter in self.virtual_player[self.chosen_index].counters:
                        if evil_counter.position[0] == good_counter.position[0] and evil_counter.position[1] == good_counter.position[1] and evil_counter.color != good_counter.color and evil_counter.position[0] != self.start_pos[evil_counter.color][0] and evil_counter.position[1] != self.start_pos[evil_counter.color][1]:
                            evil_counter.position[0] = self.dock_pos[evil_counter.color][evil_counter.number-1][0]
                            evil_counter.position[1] = self.dock_pos[evil_counter.color][evil_counter.number-1][1]
                            #POINTS
                            player.points -= 15
                            self.virtual_player[self.chosen_index].points += 20
        self.update_counters_pos()

    def winner(self):
        if self.real_player[self.chosen_index].color in self.winners:
            print("ERROR - Color is in winners!")
        else:
            if self.chosen_type == "real":
                total = 0
                for counter in self.real_player[self.chosen_index].counters:
                    if counter.position[0] == self.end_pos[self.chosen_color][0] and counter.position[1] == self.end_pos[self.chosen_color][1]:
                        total += 1
                if total == 4:
                    self.winners.append(self.real_player[self.chosen_index].color)
                    podium = len(self.winners)     
                    self.real_player[self.chosen_index].finished_the_game = True
                    self.real_player[self.chosen_index].podium = len(self.winners)
                    if len(self.winners) == 1:
                        self.real_player[self.chosen_index].points += 100
                    if len(self.winners) == 2:
                        self.real_player[self.chosen_index].points += 80
                    if len(self.winners) == 3:
                        self.real_player[self.chosen_index].points += 60
                    if len(self.winners) == 4:
                        self.real_player[self.chosen_index].points += 50


            if self.chosen_type == "virtual":
                total = 0
                for counter in self.virtual_player[self.chosen_index].counters:
                    if counter.position[0] == self.end_pos[self.chosen_color][0] and counter.position[1] == self.end_pos[self.chosen_color][1]:
                        total += 1
                if total == 4:
                    self.winners.append(self.virtual_player[self.chosen_index].color)
                    podium = len(self.winners)     
                    self.virtual_player[self.chosen_index].finished_the_game = True
                    self.virtual_player[self.chosen_index].podium = len(self.winners)
                    if len(self.winners) == 1:
                        self.virtual_player[self.chosen_index].points += 100
                    if len(self.winners) == 2:
                        self.virtual_player[self.chosen_index].points += 80
                    if len(self.winners) == 3:
                        self.virtual_player[self.chosen_index].points += 60
                    if len(self.winners) == 4:
                        self.virtual_player[self.chosen_index].points += 50

        if len(self.winners) == len(self.used_colors):
            self.continue_game = False
        else:
            self.continue_game = True

    def select_counter(self, select):
        self.select = select + 1
        if self.chosen_type == "real":
            self.real_player[self.chosen_index].chosen_counter = select
            print(f"SELECTED COUNTER = {select} || TYPE = {self.chosen_type} || ROLL = {self.real_player[self.chosen_index].roll} || POSITION X = {self.real_player[self.chosen_index].counters[self.real_player[self.chosen_index].chosen_counter].position[0]} Y = {self.real_player[self.chosen_index].counters[self.real_player[self.chosen_index].chosen_counter].position[1]}  || COLOR = {self.real_player[self.chosen_index].counters[self.real_player[self.chosen_index].chosen_counter].color}")
            self.move(self.real_player[self.chosen_index].roll, 
                      self.real_player[self.chosen_index].counters[self.real_player[self.chosen_index].chosen_counter].position, 
                      self.real_player[self.chosen_index].counters[self.real_player[self.chosen_index].chosen_counter].color)
        else:
            self.virtual_player[self.chosen_index].virtual_move()
            print(f"SELECTED COUNTER = {self.virtual_player[self.chosen_index].chosen_counter} || TYPE = {self.chosen_type} || ROLL = {self.virtual_player[self.chosen_index].roll} || POSITION X = {self.virtual_player[self.chosen_index].counters[self.virtual_player[self.chosen_index].chosen_counter].position[0]} Y = {self.virtual_player[self.chosen_index].counters[self.virtual_player[self.chosen_index].chosen_counter].position[0]} || COLOR = {self.virtual_player[self.chosen_index].counters[self.virtual_player[self.chosen_index].chosen_counter].color}")
            self.move(self.virtual_player[self.chosen_index].roll, 
                      self.virtual_player[self.chosen_index].counters[self.virtual_player[self.chosen_index].chosen_counter].position, 
                      self.virtual_player[self.chosen_index].counters[self.virtual_player[self.chosen_index].chosen_counter].color)
        

        self.kill()
        self.winner()
        if self.chosen_type == "real":
            if self.real_player[self.chosen_index].roll != 6:
                self.next_color()
        else:
            if self.virtual_player[self.chosen_index].roll != 6:
                self.next_color()
            
        self.dice_unknown = True
        self.control_game()

    def adjust_counter_position(self, counter, select, color):   
        print(f"SELECT = {select}")   
        pad_y = 0
        pad_x = 0  
        if counter.position[0] == 1:
            #pad_y = 0
            #pad_x = 10
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_x)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
        elif counter.position[0] == 2:
            #pad_y = 0
            #pad_x = 10
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
        elif counter.position[0] == 3:
            #pad_y = 0
            #pad_x = 10
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
        elif counter.position[0] == 4:
            #pad_y = 0
            #pad_x = 6
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
        elif counter.position[0] == 5:
            #pad_y = 0
            #pad_x = 0
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
        elif counter.position[0] == 6:
            #pad_y = 0
            #pad_x = 0
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
        elif counter.position[0] == 7:
            #pad_y = 0
            #pad_x = 15
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)   
        elif counter.position[0] == 8:
            #pad_y = 0
            #pad_x = 5
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
        elif counter.position[0] == 9:
            #pad_y = 0
            #pad_x = 10
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
        elif counter.position[0] == 10:
            #pad_y = 0
            #pad_x = 10
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
        elif counter.position[0] == 11:
            #pad_y = 0
            #pad_x = 10
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
        elif counter.position[0] == 12:
            #pad_y = 0
            #pad_x = 10
            if color == "red":
                red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "blue":
                blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "green":
                green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)
            elif color == "yellow":
                yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0], pady = pad_y, padx = pad_y)

    def update_counters_pos(self):
        for x in self.real_player:
            i = 0
            for y in x.counters:
                i += 1
                self.adjust_counter_position(y, i, x.color)
        for x in self.virtual_player:
            i = 0
            for y in x.counters:
                i += 1
                self.adjust_counter_position(y, i, x.color)

    def move(self, roll, position, color):
            stop = 0
            #Counter is in dock
            for pos in self.dock_pos[color]:
                if position == list(pos) and roll == 6:
                    position[0] = self.start_pos[color][0]
                    position[1] = self.start_pos[color][1]
                    if self.chosen_type == "real":
                        self.real_player[self.chosen_index].counters[self.real_player[self.chosen_index].chosen_counter].is_inside = False
                    else:
                        self.virtual_player[self.chosen_index].counters[self.virtual_player[self.chosen_index].chosen_counter].is_inside = False
                    stop = 1
                    break
            while(stop == 0): 
                # ======== MOVE LEFT ======== 
                if roll == 0:
                    break    
                elif roll < 0:
                    Error_Label = Label(text=f"ERROR! - Roll is smaller than 0!").grid(column=1, row = 12, columnspan=11)

                elif (position[0] > 7 and position[1] == 7):
                    if position[0] - roll < 7:
                        roll -= position[0] - 7
                        position[0] = 7

                    else:
                        position[0] -= roll
                        break
                elif (position[0] <= 5 and position[0] > 1 and position[1] == 7):
                    if position[0] - roll < 0:
                        roll -= position[0] - 1
                        position[0] = 1
                        
                    else:
                        position[0] -= roll
                        break
                elif (position[0] > 5 and position[0] <= 7 and position[1] == 11):
                    #YELLOW VICTOR ROAD ENTER
                    if position[0] >= 6 and color == 'yellow':
                        if position[0] == 6 and roll > 4:
                                break
                        elif position[0] == 7 and roll > 5:
                                break
                        elif position[0] == 6 and roll < 5:
                            position[1] -= roll
                            break
                        else:
                            roll -= position[0] - 6
                            position[0] = 6
                            
                    #OTHER SITUATIONS
                    elif position[0] - roll < 5:
                        roll -= position[0] - 5
                        position[0] = 5
                        
                    else:
                        position[0] -= roll
                        break
                #GREEN VICTORY ROAD
                elif (position[0] == 11 and position[1] == 6 and color == 'green'):
                    if roll > 4:
                        break
                    else:
                        position[0] -= roll
                elif position[0] == 7 and position[1] == 6:
                    break
                elif position[1] == 6 and color == "green":
                    if position[0] - 7 < roll:
                        break
                    else:
                        position[0] -= roll
                        break

                # ======== MOVE RIGHT ======== 
                elif (position[0] < 5 and position[1] == 5):
                    if position[0] + roll > 5:
                        roll -= 5 - position[0]
                        position[0] = 5
                    else:
                        position[0] += roll
                        break                    
                elif (position[0] >= 7 and position[0] < 11 and position[1] == 5):
                    if position[0] + roll > 12:
                        roll -= 11 - position[0]
                        position[0] = 11
                    else:
                        position[0] += roll
                        break            
                elif (position[0] >= 5 and position[0] < 7 and position[1] == 1):
                    #BLUE VICTOR ROAD ENTER
                    if position[0] <= 6 and color == 'blue':
                        if position[0] == 6 and roll > 4:
                                break
                        elif position[0] == 5 and roll > 5:
                                break
                        elif position[0] == 6 and roll <= 4:
                            position[1] += roll 
                            break
                        else:
                            roll -= 6 - position[0]
                            position[0] = 6
                    #OTHER SITUATIONS
                    elif position[0] + roll >= 7:
                        roll -= 7 - position[0]
                        position[0] = 7
                    else:
                        position[0] += roll
                        break
                #RED VICTORY ROAD
                elif (position[0] == 1 and position[1] == 6 and color == 'red'):
                    if roll > 4:
                        break
                    else:
                        position[0] += roll
                        break
                elif position[0] == 5 and position[1] == 6:
                    break
                elif position[1] == 6 and position[0] < 5 and color =='red':
                    if 5 - position[0] < roll:
                        break
                    else:
                        position[0] += roll
                        break
                
                # ======== MOVE UP ======== 
                elif (position[0] == 5 and position[1] >= 7):
                    if position[1] - roll <= 7:
                        roll -= position[1] - 7
                        position[1] = 7
                    else:
                        position[1] -= roll
                        break                    
                elif (position[0] == 5 and position[1] <= 5):
                    if position[1] - roll <= 0:
                        roll -= position[1] - 1
                        position[1] = 1
                    else:
                        position[1] -= roll
                        break            
                elif (position[1] >= 5 and position[1] <= 7 and position[0] == 1):
                    #RED VICTORY ROAD ENTER
                    if position[1] >= 6 and color == 'red':
                        if position[1] == 6 and roll > 4:
                                break
                        elif position[1] == 7 and roll > 5:
                                break
                        else:
                            roll -= position[1] - 6
                            position[1] = 6
                    #OTHER SITUATIONS
                    elif position[1] - roll < 5:
                        roll -= position[1] - 5
                        position[1] = 5
                    else:
                        position[1] -= roll
                        break
                #YELLOW VICTORY ROAD
                elif (position[0] == 6 and position[1] == 11 and color == 'yellow'):
                    if roll > 4:
                        break
                    else:
                        position[1] -= roll
                elif position[0] == 6 and position[1] == 7:
                    break
                elif position[0] == 6 and color == "yellow":
                    if position[1] - 7 < roll:
                        break
                    else:
                        position[1] -= roll
                        break

                # ======== MOVE DOWN ======== 
                elif (position[0] == 7 and position[1] <= 5):
                    if position[1] + roll > 5:
                        roll -= 5 - position[1]
                        position[1] = 5
                    else:
                        position[1] += roll
                        break                    
                elif (position[0] == 7 and position[1] >= 7):
                    if position[1] + roll > 11:
                        roll -= 11 - position[1]
                        position[1] = 11
                    else:
                        position[1] += roll
                        break            
                elif (position[1] >= 5 and position[1] <= 7 and position[0] == 11):
                    #GREEN VICTORY ROAD ENTER
                    if position[1] <= 6 and color == 'green':
                        if position[1] == 6 and roll > 4:
                                break
                        elif position[1] == 5 and roll > 5:
                                break
                        else:
                            roll -= 6 - position[1]
                            position[1] = 6
                    #OTHER SITUATIONS
                    elif position[1] + roll > 7:
                        roll -= 7 - position[1]
                        position[1] = 7
                    else:
                        position[1] += roll
                        break
                #BLUE VICTORY ROAD
                elif (position[0] == 6 and position[1] == 11 and color == 'blue'):
                    if roll > 4:
                        break
                    else:
                        position[1] += roll
                elif position[0] == 6 and position[1] == 5:
                    break
                elif position[0] == 6 and color == 'blue':
                    if 5 - position[1] < roll:
                        break
                    else:
                        position[1] += roll
                        break
                else:
                    Error_Label = Label(text=f"ERROR! - Cannot move {color} counter number {self.select_counter}! [{position[0], position[1]}]").grid(column=1, row = 12, columnspan=11)
                    break
                

            if position[0] > 11 or position[0] < 1 or position[1] > 11 or position[1] < 1: #Error Counter out of the board
                Error_Label = Label(text=f"ERROR! - {color} counter {self.real_player[self.chosen_index].chosen_counter}! [{position[0], position[1]}]. Function try to move counter out of the board").grid(column=12, row = 10, columnspan=11)                
            print(f"MOVE => POSITION UPDATE: X = {position[0]} | Y = {position[1]}")
            self.update_counters_pos()

    def side_panel(self):
        counter_number = [("1", 1),
                          ("2", 2),
                          ("3", 3),
                          ("4", 4)]
    
        button_roll = Button(board, text = "Roll", padx=18, command=self.dice, state=self.hide_roll_button)
        self.update_dice_img()

        button_roll.grid(column=0, row=3)
        chosen_color_label = Label(text=f"Chosen color:\n{self.chosen_color}", bg = self.chosen_color).grid(column=0, row =1)

        selected_counter = IntVar()
        selected_counter.set(self.select)
        
        i = 0 
        for text, mode in counter_number:
            Radiobutton(board, text=text, variable= selected_counter, value=mode).grid(column=0, row=5 + i)
            i += 1

        save_button = Button(board, text="Save&Quit", command= self.save_game)
        save_button.grid(column=0, row=10)

        choose_counter_button = Button(board, text="Move Counter", state=self.hide_select_button,command=lambda:self.select_counter(selected_counter.get()-1))
        choose_counter_button.grid(column=0, row=9)

        #Scoreboard
        score_title_label = Label(text="Scoreboard:").grid(row=1, column=12, sticky=S)
        scoreboard= ""
        p_number = 0
        for player in self.real_player:
            p_number += 1
            scoreboard += "[" + str(p_number) + "] " + player.nickname + " - " + player.color + " - " + f"{player.points}p" + f"- {player.podium}"
            if p_number !=4:
                scoreboard += "\n"
        for player in self.virtual_player:
            p_number += 1
            scoreboard += "[" + str(p_number) + "] " + player.nickname + " - " + player.color + " - " + f"{player.points}p" + f"{player.podium}"
            if p_number !=4:
                scoreboard += "\n"
        score_label = Label(text=scoreboard).grid(row=2, column=12, sticky=SW)

        #Counters position
        
        if self.show_counters_pos == True:
            counters_title_label = Label(text="Counters positions:").grid(row=3, column=12, sticky=S)
            p_number = 0
            for player in self.real_player:
                pos_text= ""
                for i in range(4):
                    pos_text += f"[{player.color}][{player.counters[i].number}] -> [{player.counters[i].position[0]}, {player.counters[i].position[1]}]"
                    if i !=3:
                        pos_text += "\n"
                pos_label = Label(text=pos_text, anchor=SW).grid(row=4 + p_number, column=12, sticky=SW)
                p_number += 1

    def new_game_menu(self, prev_window):
        prev_window.destroy()
        prev_window.quit()
        window = Tk()
        window.title("Ludo Board Game - Add Player")
        window.geometry("392x410")
        types = ["Real", "Virtual"]
        types_dict = {"Real":True, "Virtual":False}

        img_logo = ImageTk.PhotoImage(Image.open("logo.png"))
        logo_label = Label(window, image=img_logo).grid(row=0, column = 0, columnspan =2)

        nickname_label = Label(window, text="Nickname: ").grid(row=1, column = 0, sticky=E, padx = 5)
        nickname_entry = Entry(window, width=10)
        nickname_entry.grid(row=1, column=1, sticky=W, padx = 5)
        nickname_entry.insert(0, "Player")

        color = StringVar()
        color.set(self.colors[0])
        color_label = Label(window, text = "Color: ").grid(row=2, column=0, sticky=E, padx = 5)
        choose_color = OptionMenu(window, color, *self.colors)
        choose_color.grid(row=2, column=1, sticky=W, padx = 5)

        type = StringVar()
        type.set(types[0])
        type_label = Label(window, text = "Type: ").grid(row=3, column=0, sticky=E, padx = 5)
        choose_type = OptionMenu(window, type, *types)
        choose_type.grid(row=3, column=1, sticky=W, padx = 5)

        choose_button = Button(window, text="Add Player", command=lambda:self.add_player(color.get().lower(), types_dict[type.get()], nickname_entry.get(), window), padx=20)
        choose_button.grid(row=4, column=0, sticky=E, padx = 5)
        start_button = Button(window, text="Start Game", command=lambda:self.board_init(window), padx=20)
        start_button.grid(row=4, column=1, sticky=W, padx = 5)

        window.mainloop()

    def end_window(self):
        end = Toplevel(board)
        end.title("Ludo Board Game - Winners!")
        global podium_img
        podium_img = ImageTk.PhotoImage(Image.open("podium.png"))
        podium_label = Label(master=end, image=podium_img).grid(row=0, column = 1, columnspan = 3, rowspan = 2)
        for player in self.real_player:
            if player.podium == 1:
                first_label = Label(master=end, text=f"1.{player.nickname}\n{player.points} points").grid(row = 0, column = 2)
            if player.podium == 2:
                second_label = Label(master=end, text=f"2.{player.nickname}\n{player.points} points").grid(row = 0, column = 1)
            if player.podium == 3:
                third_label = Label(master=end, text=f"3.{player.nickname}\n{player.points} points").grid(row = 0, column = 3)
            if player.podium == 4:
                fourth_label = Label(master=end, text=f"4.{player.nickname}\n{player.points} points").grid(row = 3 , column = 2)
        for player in self.virtual_player:
            if player.podium == 1:
                first_label = Label(master=end, text=f"1.{player.nickname}\n{player.points} points").grid(row = 0, column = 2)
            if player.podium == 2:
                second_label = Label(master=end, text=f"2.{player.nickname}\n{player.points} points").grid(row = 0, column = 1)
            if player.podium == 3:
                third_label = Label(master=end, text=f"3.{player.nickname}\n{player.points} points").grid(row = 0, column = 3)
            if player.podium == 4:
                fourth_label = Label(master=end, text=f"4.{player.nickname}\n{player.points} points").grid(row = 3 , column = 2)
        end.mainloop()

    def control_game(self):
        if self.continue_game == True:
            if self.chosen_type == "virtual":
                self.hide_roll_button = DISABLED
                self.hide_select_button = DISABLED
                self.side_panel()
                self.dice()
                board.after(5000, func = self.side_panel())
                board.after(5000, self.select_counter(0))
                self.winner()
            else:
                #self.hide_select_button = DISABLED
                self.hide_select_button = NORMAL
                self.hide_roll_button = NORMAL
                self.side_panel()
        else:
            self.hide_roll_button = DISABLED
            self.hide_select_button = DISABLED
            self.side_panel()
            self.end_window()

    def board_init(self, prev_window):
        if (len(self.real_player) + len(self.virtual_player)) == 0:
            M1 = Label(prev_window, text="There are no players!").grid(row=5, column = 0, columnspan=2)
        else:
            self.start_game = True
            prev_window.destroy()
            prev_window.quit()
            global board
            board = Tk()
            board.title("Ludo Board Game")
            img_board = ImageTk.PhotoImage(Image.open("board/board.png"))
            adjust_label = []
            adjust_block = ImageTk.PhotoImage(Image.open("board/adjust_block.png"))
            
            for i in range(1, 12):
                for j in range(1, 12):
                    adjust_label.append(Label(board, image=adjust_block).grid(row=i, column=j))

            board_label = Label(image=img_board).grid(row=1, column=1, columnspan=11, rowspan=11, pady=0)

            '''
            board.overrideredirect(True)
            board.wm_attributes("-topmost", True)
            board.wm_attributes("-disabled", True)
            board.wm_attributes("-transparentcolor", "purple")
            '''
            global img_red_counter_1
            global img_red_counter_2
            global img_red_counter_3
            global img_red_counter_4
            global red_counter
            red_counter = []

            global img_green_counter_1
            global img_green_counter_2
            global img_green_counter_3
            global img_green_counter_4
            global green_counter
            green_counter = []

            global img_yellow_counter_1
            global img_yellow_counter_2
            global img_yellow_counter_3
            global img_yellow_counter_4
            global yellow_counter
            yellow_counter = []

            global img_blue_counter_1
            global img_blue_counter_2
            global img_blue_counter_3
            global img_blue_counter_4
            global blue_counter
            blue_counter = []

            global img_red_counter_blink
            global img_green_counter_blink
            global img_yellow_counter_blink
            global img_blue_counter_blink

            global dice_one
            global dice_two
            global dice_three
            global dice_four
            global dice_five
            global dice_six
            global dice_unknown
            global dice
            dice = []

            img_red_counter_1 = ImageTk.PhotoImage(Image.open("counters/red_counter/red_counter_1.png"))
            img_red_counter_2 = ImageTk.PhotoImage(Image.open("counters/red_counter/red_counter_2.png"))
            img_red_counter_3 = ImageTk.PhotoImage(Image.open("counters/red_counter/red_counter_3.png"))
            img_red_counter_4 = ImageTk.PhotoImage(Image.open("counters/red_counter/red_counter_4.png"))

            img_green_counter_1 = ImageTk.PhotoImage(Image.open("counters/green_counter/green_counter_1.png"))
            img_green_counter_2 = ImageTk.PhotoImage(Image.open("counters/green_counter/green_counter_2.png"))
            img_green_counter_3 = ImageTk.PhotoImage(Image.open("counters/green_counter/green_counter_3.png"))
            img_green_counter_4 = ImageTk.PhotoImage(Image.open("counters/green_counter/green_counter_4.png"))

            img_yellow_counter_1 = ImageTk.PhotoImage(Image.open("counters/yellow_counter/yellow_counter_1.png"))
            img_yellow_counter_2 = ImageTk.PhotoImage(Image.open("counters/yellow_counter/yellow_counter_2.png"))
            img_yellow_counter_3 = ImageTk.PhotoImage(Image.open("counters/yellow_counter/yellow_counter_3.png"))
            img_yellow_counter_4 = ImageTk.PhotoImage(Image.open("counters/yellow_counter/yellow_counter_4.png"))

            img_blue_counter_1 = ImageTk.PhotoImage(Image.open("counters/blue_counter/blue_counter_1.png"))
            img_blue_counter_2 = ImageTk.PhotoImage(Image.open("counters/blue_counter/blue_counter_2.png"))
            img_blue_counter_3 = ImageTk.PhotoImage(Image.open("counters/blue_counter/blue_counter_3.png"))
            img_blue_counter_4 = ImageTk.PhotoImage(Image.open("counters/blue_counter/blue_counter_4.png"))

            img_red_counter_blink = ImageTk.PhotoImage(Image.open("counters/red_counter_blink.png"))
            img_green_counter_blink = ImageTk.PhotoImage(Image.open("counters/green_counter_blink.png"))
            img_yellow_counter_blink = ImageTk.PhotoImage(Image.open("counters/yellow_counter_blink.png"))
            img_blue_counter_blink = ImageTk.PhotoImage(Image.open("counters/blue_counter_blink.png"))            

            dice_one = ImageTk.PhotoImage(Image.open("dice/dice_one.png"))
            dice_two = ImageTk.PhotoImage(Image.open("dice/dice_two.png"))
            dice_three = ImageTk.PhotoImage(Image.open("dice/dice_three.png"))
            dice_four = ImageTk.PhotoImage(Image.open("dice/dice_four.png"))
            dice_five = ImageTk.PhotoImage(Image.open("dice/dice_five.png"))
            dice_six  = ImageTk.PhotoImage(Image.open("dice/dice_six.png"))       
            dice_unknown  = ImageTk.PhotoImage(Image.open("dice/dice_unknown.png"))       

            dice.append(dice_one)
            dice.append(dice_two)   
            dice.append(dice_three)   
            dice.append(dice_four)   
            dice.append(dice_five)   
            dice.append(dice_six)      


            red_counter.append(Label(image=img_red_counter_1))
            red_counter.append(Label(image=img_red_counter_2))
            red_counter.append(Label(image=img_red_counter_3))
            red_counter.append(Label(image=img_red_counter_4))

            green_counter.append(Label(image=img_green_counter_1))
            green_counter.append(Label(image=img_green_counter_2))
            green_counter.append(Label(image=img_green_counter_3))
            green_counter.append(Label(image=img_green_counter_4))

            yellow_counter.append(Label(image=img_yellow_counter_1))
            yellow_counter.append(Label(image=img_yellow_counter_2))
            yellow_counter.append(Label(image=img_yellow_counter_3))
            yellow_counter.append(Label(image=img_yellow_counter_4))

            blue_counter.append(Label(image=img_blue_counter_1))
            blue_counter.append(Label(image=img_blue_counter_2))
            blue_counter.append(Label(image=img_blue_counter_3))
            blue_counter.append(Label(image=img_blue_counter_4))
        
            self.next_color()
            self.update_counters_pos()
            self.control_game()

            button_quit = Button(board, text = "End", command = board.quit, padx=30).grid(column=0, row = 11)           

            board.mainloop()

    def set_options(self, prev_window, language, show_pos):
        prev_window.destroy()

        if show_pos == self.languages["lan_yes"][self.chosen_language]:
            self.show_counters_pos = True
        if show_pos == self.languages["lan_no"][self.chosen_language]:
            self.show_counters_pos = False
        if language == self.languages["languages"][0]:
            self.chosen_language = 0
        if language == self.languages["languages"][1]:
            self.chosen_language = 1
        
        self.main_menu()

    def back_to_menu(self, prev_window):
        prev_window.destroy()
        self.main_menu()

    def options_menu(self, prev_window):
        prev_window.destroy()
        start = Tk()
        start.title("Ludo Board Game")
        global img_logo
        img_logo = ImageTk.PhotoImage(Image.open("logo.png"))
        logo_label = Label(start, image=img_logo).grid(row=0, column = 0, columnspan=2)

        #Choose Language
        language_label = Label(start, text = "Language:").grid(row=1, column = 0, sticky = E, padx = 5)
        select_language = StringVar()
        select_language.set(self.languages["languages"][self.chosen_language])
        choose_language = OptionMenu(start, select_language, *self.languages["languages"])
        choose_language.grid(row=1, column=1, sticky=W, padx = 5)

        #Show Counters position
        counters_pos_label = Label(start, text = "Show counters positions:").grid(row=2, column = 0, sticky = E, padx = 5)
        select_counters_pos = StringVar()
        if self.show_counters_pos == True:
            select_counters_pos.set(self.languages["lan_yes"][self.chosen_language])
        if self.show_counters_pos == False:
            select_counters_pos.set(self.languages["lan_no"][self.chosen_language])
        show_counters = OptionMenu(start, select_counters_pos, *(self.languages["lan_yes"][self.chosen_language], self.languages["lan_no"][self.chosen_language]))
        show_counters.grid(row=2, column=1, sticky=W, padx = 5)

        save_button = Button(start, text="Save changes", command=lambda:self.set_options(start, select_language.get(), select_counters_pos.get())).grid(row = 5, column=0)
        discard_button = Button(start, text="Discard changes", command=lambda:self.back_to_menu(start)).grid(row=5, column=1)

    def leadership(self, start):
        start.destroy()

    def load_game(self, start):
        return

    def main_menu(self):
        start = Tk()
        start.title("Ludo Board Game")
        load_game_status = DISABLED

        img_logo = ImageTk.PhotoImage(Image.open("logo.png"))
        logo_label = Label(start, image=img_logo).grid(row=0, column = 0)
        new_game_button = Button(start, text="New Game", command = lambda:self.new_game_menu(start), padx = 20).grid(row=1, column=0, pady=5)
        load_game_button = Button(start, text="Load Game", command = lambda:self.load_game(start), state=load_game_status, padx=18).grid(row=2, column=0, pady=5)
        leadership_button = Button(start, text="Leadership Board", command = lambda:self.leadership(start), padx = 2).grid(row=3, column=0, pady=5)
        options_button = Button(start, text="Options", command = lambda:self.options_menu(start), padx = 27).grid(row=4, column=0, pady=5)
        end_button = Button(start, text="End", command = start.quit, padx = 38).grid(row=5, column = 0, pady=5)

        start.mainloop()


game = Ludo() 
game.main_menu()