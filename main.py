from tkinter import *
from tkinter import  _get_default_root
from tkinter import messagebox
from datetime import datetime
import time
import random
from PIL import ImageTk, Image
import sqlite3

#CREATED BY https://github.com/grzstr/ludo-game

class Counter:
    def __init__(self, color, number, dock_pos):
        self.color = color
        self.position = []
        self.number = number
        self.is_inside = True
        self.dock_pos = dock_pos
        self.position = list(self.dock_pos[color][number-1])
        
    def set_dock_pos(self):
        self.position = list(self.dock_pos[self.color][self.number-1])

class Player:
    def __init__(self, color, dock_pos, end_pos, nickname = "Player"):
        self.counter_number = 4
        self.counters = []
        self.chosen_counter = 1
        self.color = color
        self.finished_the_game = False
        self.podium = 0
        self.in_dock = 4
        self.dock_pos = dock_pos
        self.end_pos = end_pos
        self.points = 100
        self.nickname = nickname
        self.roll = random.randint(1, 6)

        for i in range(1, 5):
            self.counters.append(Counter(color, i, self.dock_pos))

class Virtual_Player(Player):
    def virtual_move(self):
        ok_counter = False
        if self.in_dock > 0 and self.roll == 6: # Counter is in dock
            for i in range(4):
                if self.counters[i].is_inside == True:
                    self.chosen_counter = i
                    ok_counter = True
                    break
        elif self.in_dock < 4:
             for i in range(4):
                if self.counters[i].is_inside == False and self.end_pos[self.color][0] != self.counters[i].position[0] and self.end_pos[self.color][1] != self.counters[i].position[1]:
                    self.chosen_counter = i
                    ok_counter = True
                    break    
                elif self.color == "red" and self.counters[i].position[0] >= 1 and self.counters[i].position[0] <= 5 and self.counters[i].position[0] == 6: 
                    if self.counters[i].position[0] + self.roll <= 5:
                        self.chosen_counter = i
                        ok_counter = True
                        break
                elif self.color == "yellow" and self.counters[i].position[0] == 6 and self.counters[i].position[1] >= 7 and self.counters[i].position[1] <= 11:
                    if self.counters[i].position[1] - self.roll >= 7:
                        self.chosen_counter = i
                        ok_counter = True
                        break
                elif self.color == "blue" and self.counters[i].position[0] == 6 and self.counters[i].position[1] <= 5 and self.counters[i].position[1] >= 1:
                    if self.counters[i].position[1] + self.roll <= 5:
                        self.chosen_counter = i
                        ok_counter = True
                        break
                elif self.color == "green" and self.counters[i].position[1] == 6 and self.counters[i].position[0] >= 7 and self.counters[i].position[1] <= 11:
                    if self.counters[i].position[0] - self.roll >= 7:
                        self.chosen_counter = i
                        ok_counter = True
                        break
        else:
            self.chosen_counter = random.randint(0, 3)
            ok_counter = True

        if ok_counter == False:
            rand = random.randint(0, 3)
            while(1):
                end = 0
                for i in range(4):
                    if self.counters[i].position[1] == self.end_pos[self.color][1] and self.counters[i].position[0] == self.end_pos[self.color][0]:
                        end += 1    
                if end == 4:
                    break
                if self.counters[rand].position[1] == self.end_pos[self.color][1] and self.counters[rand].position[0] == self.end_pos[self.color][0]:
                    rand = random.randint(0, 3)
                else:
                    break
            self.chosen_counter = rand


class Ludo:
    def __init__(self):
        self.virtual_player = []
        self.colors = ["red", "yellow", "blue", "green"]
        self.used_colors = []
        self.used_nicknames = []
        self.winners = []
        self.losers = []
        self.real_player = []
        self.chosen_color = ""
        self.select = 1
        self.continue_game = True
        self.hide_roll_button = NORMAL
        self.hide_select_button = DISABLED
        self.hide_radio_buttons = NORMAL
        self.hide_give_up_button = NORMAL
        self.dice_unknown = True
        self.start_game = False
        self.chosen_type = ""
        self.chosen_index = 0
        self.chosen_language = 0
        self.show_counters_pos = False
        self.show_board_pos = False
        self.show_errors = False
        self.developer_mode = False
        self.default_virtual_speed = 1
        now = datetime.now()
        self.start_data_time = now.strftime("%d-%m-%Y_%H-%M-%S")
        
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

        #LANGUAGES DICTIONARIES

        self.color_types_dict = {"Real": "real",
                                "Virtual": "virtual",
                                "Red": "red",
                                "Blue": "blue",
                                "Green": "green",
                                "Yellow": "yellow",
                                "languages": (("English", "Polish"), ("Angielski", "Polski")),
                                
                                #POLISH
                                "Rzeczywisty": "real",
                                "Wirtualny": "virtual",
                                "Czerwony": "red",
                                "Niebieski": "blue",
                                "Zielony": "green",
                                "Żółty": "yellow",}

        self.languages = {  "title": ("Ludo Board Game", 'Gra planszowa "Chińczyk"'),
                            "lan_yes": ("Yes", "Tak"),
                            "lan_no": ("No", "Nie"), 

                            #COLORS TYPES
                            "colors": (("Red", "Blue", "Green", "Yellow"),("Czerwony", "Niebieski", "Zielony", "Żółty")),
                            "types": (("Real", "Virtual"), ("Rzeczywisty", "Wirtualny")),

                            "red": ("Red", "Czerwony"),
                            "green": ("Green", "Zielony"),
                            "blue": ("Blue", "Niebieski"),
                            "yellow": ("Yellow", "Żółty"),

                            "english": ("English", "Angielski"),
                            "polish": ("Polish", "Polski"),

                            "real": ("Real", "Rzeczywisty"),
                            "virtual": ("Virtual", "Wirtualny"),

                            0: ("English", "Angielski"),
                            1: ("Polish", "Polski"),

                            #MAIN MENU
                            "new_game": ("New game", "Nowa gra"),
                            "load_game": ("Continue game", "Kontynuuj grę"),
                            "victory": ("Victory board", "Tablica zwycięstw"),
                            "options": ("Options", "Opcje"),
                            "end": ("End", "Zakończ"),

                            #NEW GAME MENU
                            "color": ("Color", "Kolor"),
                            "nickname": ("Nickname", "Nazwa"),
                            "player": ("Player", "Gracz"),
                            "type": ("Type", "Typ"),
                            "add_player": ("Add Player", "Dodaj gracza"),
                            "start_game": ("Start game", "Rozpocznij grę"),

                            #BOARD INIT
                            "roll": ("Roll", "Rzuć kostką"),
                            "give_up": ("Give up", "Poddaj się"),
                            "chosen_color": ("Chosen color", "Wybrany kolor"),
                            "save_game": ("Save game", "Zapisz grę"),
                            "move_counter": ("Move counter", "Rusz pionkiem"),
                            "scoreboard": ("Scoreboard", "Tablica wyników"),
                            "counter_position": ("Counters positions", "Pozycje pionków"),

                            #OPTIONS MENU
                            "language": ("Language", "Język"),
                            "show_counters_pos": ("Show tokens positions", "Pokaż pozycję pionków"),
                            "show_board_pos": ("Load board with boxes coordinates", "Wczytaj planszę z koordynatami pól"),
                            "show_dev_mode": ("Developer mode", "Tryb developerski"),
                            "show_errors": ("Show error messages", "Wyświetl komunikaty o błędach"),
                            "save": ("Save changes", "Zapisz zmiany"),
                            "discard": ("Discard changes", "Niezapisuj zmian"),
                            "virtual_speed": ("Speed of virtual players", "Prędkość wirtualnych graczy"),

                            "back": ("Back", "Powrót"),
                            "points": ("points", "punktów"),
                            
                            #WINNERS
                            "1st": ("1st PLACE!", "PIERWSZE MIEJSCE!"),
                            "2nd": ("2nd PLACE!", "DRUGIE MIEJSCE!"),
                            "3rd": ("3rd PLACE!", "TRZECIE MIEJSCE!"),
                            "4th": ("4th PLACE!", "CZWARTE MIEJSCE!"),

                            "delete_records": ("Delete data", "Usuń dane"),

                            #ERROR MESSAGES
                            "no_players": ("There are no players!", "Brak graczy!"),
                            "no_leaders": ("There are no data to display!", "Brak danych do wyświetlenia!"),
                            "wrong_color": ("Wrong color!", "Zły kolor!"),
                            "used_color": ("This color has already been used!", "Ten kolor już został wykorzystany!"),
                            "used_name": ("This nickname has already been used!","Ta nazwa już została wykorzystana!"),
                            "four_players": ("There are already four players!", "Jest już czterech graczy!"),
                            "roll_smaller_0": ("ERROR! - Roll is smaller than 0!", "BŁĄD! - Wyrzucono liczbę mniejszą niż 0"),
                            "color_in_winners": ("ERROR! - Color is in winners!", "BŁĄD! - Ten kolor już zakończył grę"),
                            "color_in_losers": ("ERROR! - Color is in losers!", "BŁĄD! - Ten kolor już poddał grę"),    

                            #POPUP MESSAGES
                            "popup_options": ("Are you sure?", "Czy chcesz zachować zmiany?"),
                            "popup_leaders": ("Do you want to delete data?", "Czy chcesz usunąć dane?"),
                            "popup_end": ("Do you want to quit the game?", "Czy chcesz zakończyć grę?"),
                            "popup_save": ("Do you want to save the game?", "Czy chcesz zapisać grę?"),

                            #CANNOT MOVE COUNTER NUMBER
                            "cannot_move_0": ("ERROR! - Cannot move", "Błąd nie można ruszyć"),
                            "cannot_move_1": ("counter number", "pionka numer"),
                            "kill_1": ("Token", "Pionek"), 
                            "kill_2": ("was beaten by the", "został zbity przez pionek")

                            }

    def error_log(self, error_text, which_window = 1, save = True):
        if which_window == 0: #ADD PLAYER WINDOW
           Error_Label = Label(text=error_text).grid(column=0, row = 6, columnspan= 2)         
        if which_window == 1:  # BOARD WINDOW
            if self.show_errors == True:
                Error_Label = Label(text=error_text).grid(column=12, row = 10)        
        if which_window == 3:  # BOARD WINDOW KILL
            Error_Label = Label(text=error_text).grid(column=12, row = 10) 
        if save == True:         
            date = datetime.now()
            file = open("error_log_" + self.start_data_time + ".txt", "a")
            file.write(date.strftime("%d/%m/%T %H:%M:%S")  + " - " + error_text + "\n")
            file.close()

    def tksleep(self, t):
        ms = int(t*1000)
        root = _get_default_root('sleep')
        var = IntVar(root)
        root.after(ms, var.set, 1)
        root.wait_variable(var)

    def add_leader(self, leaders, player, type):
        c = leaders.cursor()
        c.execute("SELECT * FROM players WHERE nickname = ?", [player.nickname])
        result = c.fetchone()
        if result == None:
            c.execute("""INSERT INTO players VALUES (
                :nickname, 
                :type,
                :points
                )""", 
                    {
                        "nickname": player.nickname, 
                        "type": type, 
                        "points": player.points
                    }
                    )       
        else:
            if int(result[2]) < player.points:
                c.execute("UPDATE players SET points = ? WHERE nickname = ?", (player.points, player.nickname))


        leaders.commit()

    def save_leaders(self):
        leaders = sqlite3.connect('leaders.db')
        c = leaders.cursor()
        c.execute("""CREATE TABLE if not exists players (
                nickname text,
                type text,
                points integer
                )""")    
        
        for player in self.real_player:
            self.add_leader(leaders, player, "real")
        for player in self.virtual_player:
            self.add_leader(leaders, player, "virtual")
        c.close()

    def add_player_to_save(self, save, player, type):
        c = save.cursor()
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
                    "counter_1_pos_x": player.counters[0].position[0], 
                    "counter_1_pos_y": player.counters[0].position[1], 
                    "counter_2_pos_x": player.counters[1].position[0],
                    "counter_2_pos_y": player.counters[1].position[1],
                    "counter_3_pos_x": player.counters[2].position[0],
                    "counter_3_pos_y": player.counters[2].position[1],
                    "counter_4_pos_x": player.counters[3].position[0],
                    "counter_4_pos_y": player.counters[3].position[1]
                }
                )       
        save.commit()

    def save_game(self):
        save = sqlite3.connect('saved_game.db')
        c = save.cursor()
        c.execute("drop table if exists players")
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
            self.add_player_to_save(save, player, "real")
        for player in self.virtual_player:
            self.add_player_to_save(save, player, "virtual")
        save.close()

    def update_dice_img(self):
        if self.chosen_type == "real":
            roll = self.real_player[self.chosen_index].roll - 1
            if self.developer_mode == False:
                self.hide_roll_button = DISABLED
            else:
                self.hide_roll_button = NORMAL
        else:
            roll = self.virtual_player[self.chosen_index].roll - 1
            self.hide_roll_button = DISABLED
        
        if self.dice_unknown == True:
            roll_label =Label(image=dice_unknown)
        else:
            roll_label = Label(image=dice[roll])
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
                #if self.real_player[self.chosen_index].podium != 0 and self.real_player[self.chosen_index].podium != len(self.used_colors):
                if self.real_player[self.chosen_index].podium != 0 and (len(self.winners) + len(self.losers)) != len(self.used_colors):
                    self.next_color()
            else:
                #if self.virtual_player[self.chosen_index].podium != 0 and self.virtual_player[self.chosen_index].podium != len(self.used_colors):
                if self.virtual_player[self.chosen_index].podium != 0 and (len(self.winners) + len(self.losers)) != len(self.used_colors):
                    self.next_color()

    def check_nickname(self, nickname, window):
        i = 0
        new_nickname = nickname
        while(1):
            i += 1
            if new_nickname in self.used_nicknames:
                new_nickname = nickname
                new_nickname += " " + str(i)
                self.error_log(self.languages["used_name"][self.chosen_language], save = False)
            else:
                nickname = new_nickname
                self.used_nicknames.append(nickname)
                break
        return nickname

    def add_player(self, color, is_real, nickname, window):
        if len(self.real_player)+len(self.virtual_player) < 4:
            if color in self.colors:
                if color in self.used_colors:
                    self.error_log(self.languages["used_color"][self.chosen_language], 0, save = False)
                else:
                    nickname = self.check_nickname(nickname, window)
                    self.used_colors.append(color)
                    if is_real == True:
                        self.real_player.append(Player(color, self.dock_pos, self.end_pos, nickname))
                    else:
                        self.virtual_player.append(Virtual_Player(color, self.dock_pos, self.end_pos, nickname))
            else:
                self.error_log(self.languages["wrong_color"][self.chosen_language], 0, save = False)
        else:
            self.error_log(self.languages["four_players"][self.chosen_language], 0, save = False)

        for x in range(len(self.real_player)):
            players_number_label = Label(window, text=f"[{len(self.real_player)+len(self.virtual_player)}]: {self.real_player[x].nickname}, {self.languages['types'][self.chosen_language][0]}, {self.languages[self.real_player[x].color][self.chosen_language]}")
            players_number_label.grid(row=7+len(self.real_player)+len(self.virtual_player), column=0, columnspan=2)

        for y in range(len(self.virtual_player)):
            virtual_number_label = Label(window, text=f"[{len(self.real_player)+len(self.virtual_player)}]: {self.virtual_player[y].nickname}, {self.languages['types'][self.chosen_language][1]} {self.languages[self.virtual_player[y].color][self.chosen_language]}")
            virtual_number_label.grid(row=7+len(self.real_player)+len(self.virtual_player), column=0, columnspan=2)

    def dice(self):
        roll = random.randint(1, 6)
        if self.chosen_type == "real":
            self.real_player[self.chosen_index].roll = roll
            self.hide_select_button = NORMAL
        else:
            self.virtual_player[self.chosen_index].roll = roll
        self.dice_unknown = False
        self.update_dice_img()
      
        if self.chosen_type == "real":
            self.side_panel()

    def kill_check_player(self, player, second_player):
        if player.color != second_player.color:
            for evil_counter in player.counters:
                for good_counter in second_player.counters:
                    if evil_counter.position[0] == good_counter.position[0] and evil_counter.position[1] == good_counter.position[1] and evil_counter.color != good_counter.color and evil_counter.position[0] != self.start_pos[evil_counter.color][0] and evil_counter.position[1] != self.start_pos[evil_counter.color][1]:
                        evil_counter.position[0] = self.dock_pos[evil_counter.color][evil_counter.number-1][0]
                        evil_counter.position[1] = self.dock_pos[evil_counter.color][evil_counter.number-1][1]
                        #POINTS
                        player.points -= 15
                        second_player.points += 20
                        player.in_dock += 1
                        #self.error_log(self.languages["kill_1"][self.chosen_language] + " " + self.languages[player.color][self.chosen_language] + " " + self.languages["kill_2"][self.chosen_language] + " " + self.languages[second_player.color][self.chosen_language], 3, save = False)
        return player

    def kill(self):
        if self.chosen_type == "real":
            second_player = self.real_player[self.chosen_index]
        else:    
            second_player = self.virtual_player[self.chosen_index]
        for player in self.real_player:
            player = self.kill_check_player(player, second_player)
        for player in self.virtual_player:
            player = self.kill_check_player(player, second_player)

        self.update_counters_pos()

    def winner(self):
        if self.chosen_type == "real":
            player = self.real_player[self.chosen_index]
        else:
            player = self.virtual_player[self.chosen_index]
        
        if player.color in self.winners:
            self.error_log(self.languages["color_in_winners"][self.chosen_language])
        elif player.color in self.losers:
            self.error_log(self.languages["color_in_losers"][self.chosen_language])
        else:
            total = 0
            for counter in player.counters:
                if counter.position[0] == self.end_pos[self.chosen_color][0] and counter.position[1] == self.end_pos[self.chosen_color][1]:
                    total += 1
            if total == 4:
                self.winners.append(player.color)
                podium = len(self.winners)     
                player.finished_the_game = True
                player.podium = len(self.winners)
                if len(self.winners) == 1:
                    player.points += 100
                if len(self.winners) == 2:
                    player.points += 80
                if len(self.winners) == 3:
                    player.points += 60
                if len(self.winners) == 4:
                    player.points += 50

        if (len(self.winners) + len(self.losers)) == len(self.used_colors):
            self.continue_game = False
        else:
            self.continue_game = True

    def select_counter(self, select):
        if self.chosen_type == "real":
            self.select = select + 1
            self.real_player[self.chosen_index].chosen_counter = select
            player = self.real_player[self.chosen_index]
        else:
            self.virtual_player[self.chosen_index].virtual_move()
            self.select = self.virtual_player[self.chosen_index].chosen_counter
            player = self.virtual_player[self.chosen_index]
        
        self.check_dock(player.roll, 
                        player.counters[player.chosen_counter].position, 
                        player.counters[player.chosen_counter].color)
        self.kill()
        self.winner()

        if self.chosen_type == "real":
            if player.roll != 6:
                self.next_color()
            self.dice_unknown = True
            self.side_panel()
            self.control_game()
        else:
            if player.roll != 6:
                self.next_color()
            self.dice_unknown = True

    def adjust_counter_position(self, counter, select, color):   
        if color == "red":
            red_counter[select - 1].grid(row=counter.position[1], column=counter.position[0])
        elif color == "blue":
            blue_counter[select - 1].grid(row=counter.position[1], column=counter.position[0])
        elif color == "green":
            green_counter[select - 1].grid(row=counter.position[1], column=counter.position[0])
        elif color == "yellow":
            yellow_counter[select - 1].grid(row=counter.position[1], column=counter.position[0])

    def update_counters_pos(self):
        for x in self.real_player:
            if self.chosen_color != x.color:
                i = 0
                for y in x.counters:
                    i += 1
                    self.adjust_counter_position(y, i, x.color)
            else:
                current_player = x
        for x in self.virtual_player:
            if self.chosen_color != x.color:
                i = 0
                for y in x.counters:
                    i += 1
                    self.adjust_counter_position(y, i, x.color)
            else:
                current_player = x
        
        if self.chosen_color != "":
            i = 0
            for y in current_player.counters:
                i += 1
                self.adjust_counter_position(y, i, current_player.color)      

    def move(self, roll, position, color, old_position):
        while(1):
            if roll > 0:
                # ======== MOVE LEFT ======== 
                if (position[0] > 7 and position[1] == 7):
                    if position[0] - roll < 7:
                        roll -= position[0] - 7
                        position[0] = 7
                    else:
                        position[0] -= roll
                        break
                elif (position[0] <= 5 and position[0] > 1 and position[1] == 7):
                    if position[0] - roll <= 0:
                        roll -= position[0] - 1
                        position[0] = 1         
                    else:
                        position[0] -= roll
                        break
                elif (position[0] > 5 and position[0] <= 7 and position[1] == 11):
                    #YELLOW VICTOR ROAD ENTER
                    if position[0] >= 6 and color == 'yellow':
                        if position[0] == 6 and roll < 5:
                            position[1] -= roll
                            break
                        elif (position[0] == 6 and roll <= 4) or (position[0] == 7 and roll <= 5):
                            roll -= position[0] - 6
                            position[0] = 6  
                        else:
                            break                    
                    #OTHER SITUATIONS
                    elif position[0] - roll < 5:
                        roll -= position[0] - 5
                        position[0] = 5                
                    else:
                        position[0] -= roll
                        break
                #GREEN VICTORY ROAD
                elif (position[0] == 11 and position[1] == 6 and color == 'green'):
                    if roll <= 4:
                        position[0] -= roll
                    else:
                        break
                elif position[1] == 6 and color == "green" and  position[0] != 7 and position[0] > 7 and position[0] <= 11:
                    if position[0] - 7 >= roll:
                        position[0] -= roll
                        break
                    else:
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
                    if position[0] + roll >= 12:
                        roll -= 11 - position[0]
                        position[0] = 11
                    else:
                        position[0] += roll        
                        break
                elif (position[0] >= 5 and position[0] < 7 and position[1] == 1):
                    #BLUE VICTOR ROAD ENTER
                    if position[0] <= 6 and color == 'blue':
                        if position[0] == 6 and roll <= 4:
                            position[1] += roll 
                            break
                        elif (position[0] == 6 and roll <= 4) or (position[0] == 5 and roll <= 5):
                            roll -= 6 - position[0]
                            position[0] = 6
                        else:
                            break
                    #OTHER SITUATIONS
                    elif position[0] + roll >= 7:
                        roll -= 7 - position[0]
                        position[0] = 7
                    else:
                        position[0] += roll
                        break
                #RED VICTORY ROAD
                elif (position[0] == 1 and position[1] == 6 and color == 'red'):
                    if roll <= 4:
                        position[0] += roll
                        break
                    else:
                        break
                elif position[1] == 6 and position[0] < 5 and color =='red':
                    if 5 - position[0] >= roll:
                        position[0] += roll
                        break
                    else:
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
                        if (position[1] != 6 and roll <= 4) or (position[1] != 7 and roll <= 5):
                            roll -= position[1] - 6
                            position[1] = 6
                        else:
                            break
                    #OTHER SITUATIONS
                    elif position[1] - roll < 5:
                        roll -= position[1] - 5
                        position[1] = 5
                    else:
                        position[1] -= roll
                        break
                #YELLOW VICTORY ROAD
                elif (position[0] == 6 and position[1] == 11 and color == 'yellow'):
                    if roll <= 4:
                        position[1] -= roll
                    else:
                        break
                elif position[0] == 6 and color == "yellow":
                    if position[1] - 7 >= roll:
                        position[1] -= roll
                        break
                    else:
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
                        if (position[1] != 6 and roll <= 4) or (position[1] != 5 and roll <= 5):
                            roll -= 6 - position[1]
                            position[1] = 6
                        else:
                            break
                    #OTHER SITUATIONS
                    elif position[1] + roll > 7:
                        roll -= 7 - position[1]
                        position[1] = 7
                    else:
                        position[1] += roll
                        break
                #BLUE VICTORY ROAD
                elif (position[0] == 6 and position[1] == 11 and color == 'blue'):
                    if roll <= 4:
                        position[1] += roll
                    else:
                        break
                elif position[0] == 6 and color == 'blue':
                    if 5 - position[1] >= roll:
                        position[1] += roll
                        break
                    else:
                        break
                else:
                    self.error_log(self.languages["cannot_move_0"][self.chosen_language] + " " + self.languages[color][self.chosen_language].lower() + " " + self.languages["cannot_move_1"][self.chosen_language] + "[" + str(position[0]) + " " + str(position[1]) + "]")
                    break
            else:
                #Roll is smaller than 0
                #self.error_log(self.languages["roll_smaller_0"][self.chosen_language])
                break

            if position[0] > 11 or position[0] < 1 or position[1] > 11 or position[1] < 1: #Error Counter out of the board
                if self.chosen_type == "real":
                    player = self.real_player
                else:
                    player = self.virtual_player
                self.error_log(f"ERROR! - {color} counter {player[self.chosen_index].chosen_counter}! [{position[0], position[1]}]. || OLD POSITION [{old_position[0]}][{old_position[1]}] || ROLL = {roll} || Function try to move counter out of the board")

    def check_dock(self, roll, position, color):
            old_position = []
            old_position.append(position[0])
            old_position.append(position[1])
            move_further = 0
            #Counter is in dock
            for pos in self.dock_pos[color]:
                if position == list(pos):
                    if roll == 6:
                        position[0] = self.start_pos[color][0]
                        position[1] = self.start_pos[color][1]
                        if self.chosen_type == "real":
                            self.real_player[self.chosen_index].counters[self.real_player[self.chosen_index].chosen_counter].is_inside = False
                            self.real_player[self.chosen_index].in_dock -= 1
                        else:
                            self.virtual_player[self.chosen_index].counters[self.virtual_player[self.chosen_index].chosen_counter].is_inside = False
                            self.virtual_player[self.chosen_index].in_dock -= 1
                        move_further = 1
                        break
                    else:
                        move_further = 1
                        break
            if move_further == 0:
                self.move(roll, position, color, old_position)
            self.update_counters_pos()

    def give_up(self):
        if self.chosen_type == "real":
            player = self.real_player[self.chosen_index]
        else:
            player = self.virtual_player[self.chosen_index]
        
        if player.color in self.winners:
            self.error_log(self.languages["color_in_winners"][self.chosen_language])
        elif player.color in self.losers:
            self.error_log(self.languages["color_in_losers"][self.chosen_language])
        else:
            self.losers.append(player.color)
            player.podium = len(self.used_colors) - len(self.losers) + 1
            for counter in player.counters:
                counter.set_dock_pos()
            self.update_counters_pos()
            self.next_color()

        if len(self.winners) + len(self.losers) == len(self.used_colors):
            self.continue_game = False
        else:
            self.continue_game = True
        self.control_game()

    def side_panel(self):
        counter_number = [("1", 1),
                          ("2", 2),
                          ("3", 3),
                          ("4", 4)]
    
        button_roll = Button(board, text = self.languages["roll"][self.chosen_language], padx=18, command=self.dice, state=self.hide_roll_button)
        self.update_dice_img()

        button_roll.grid(column=0, row=3)
        chosen_color_label = Label(text= self.languages["chosen_color"][self.chosen_language] + f":\n{self.languages[self.chosen_color][self.chosen_language]}", bg = self.chosen_color).grid(column=0, row =1)

        give_up_button = Button(board, text=self.languages["give_up"][self.chosen_language], padx=18, command=self.give_up, state=self.hide_give_up_button).grid(column=0, row=4)

        selected_counter = IntVar()
        selected_counter.set(self.select)
        
        i = 0 
        for text, mode in counter_number:
            Radiobutton(board, text=text, variable= selected_counter, value=mode, state=self.hide_radio_buttons).grid(column=0, row=5 + i)
            i += 1

        save_button = Button(board, text=self.languages["save_game"][self.chosen_language], command=self.save_popup)
        save_button.grid(column=0, row=10)

        choose_counter_button = Button(board, text=self.languages["move_counter"][self.chosen_language], state=self.hide_select_button,command=lambda:self.select_counter(selected_counter.get()-1))
        choose_counter_button.grid(column=0, row=9)

        #Scoreboard
        score_title_label = Label(text=self.languages["scoreboard"][self.chosen_language] + ":").grid(row=1, column=12, sticky=S)
        scoreboard= ""
        p_number = 0
        for player in self.real_player:
            p_number += 1
            scoreboard += "[" + str(p_number) + "] " + player.nickname + " - " + self.languages[player.color][self.chosen_language] + " - " + f"{player.points}p"
            if player.podium == 1:
                scoreboard += f"- " + self.languages["1st"][self.chosen_language]
            if player.podium == 2:
                scoreboard += f"- " + self.languages["2nd"][self.chosen_language]
            if player.podium == 3:
                scoreboard += f"- " + self.languages["3rd"][self.chosen_language]
            if player.podium == 4:
                scoreboard += f"- " + self.languages["4th"][self.chosen_language]
            if p_number !=4:
                scoreboard += "\n"
        for player in self.virtual_player:
            p_number += 1
            scoreboard += "[" + str(p_number) + "] " + player.nickname + " - " + self.languages[player.color][self.chosen_language] + " - " + f"{player.points}p"
            if player.podium == 1:
                scoreboard += f"- " + self.languages["1st"][self.chosen_language]
            if player.podium == 2:
                scoreboard += f"- " + self.languages["2nd"][self.chosen_language]
            if player.podium == 3:
                scoreboard += f"- " + self.languages["3rd"][self.chosen_language]
            if player.podium == 4:
                scoreboard += f"- " + self.languages["4th"][self.chosen_language]           
            if p_number !=4:
                scoreboard += "\n"
        score_label = Label(text=scoreboard, anchor=SW).grid(row=2, column=12, sticky=SW)

        #Counters position
        
        if self.show_counters_pos == True:
            counters_title_label = Label(text= self.languages["counter_position"][self.chosen_language] + ":").grid(row=3, column=12, sticky=S)
            p_number = 0
            for player in self.real_player:
                pos_text= ""
                for i in range(4):
                    pos_text += f"[{self.languages[player.color][self.chosen_language]}][{player.counters[i].number}] -> [{player.counters[i].position[0]}, {player.counters[i].position[1]}]"
                    if i !=3:
                        pos_text += "\n"
                pos_label = Label(text=pos_text, anchor=SW).grid(row=4 + p_number, column=12, sticky=SW)
                p_number += 1
            for player in self.virtual_player:
                pos_text= ""
                for i in range(4):
                    pos_text += f"[{self.languages[player.color][self.chosen_language]}][{player.counters[i].number}] -> [{player.counters[i].position[0]}, {player.counters[i].position[1]}]"
                    if i !=3:
                        pos_text += "\n"
                pos_label = Label(text=pos_text, anchor=SW).grid(row=4 + p_number, column=12, sticky=SW)
                p_number += 1

    def new_game_menu(self, prev_window):
        prev_window.destroy()
        prev_window.quit()
        window = Tk()
        window.title(self.languages["title"][self.chosen_language])
        window.geometry("392x450")
        window.protocol("WM_DELETE_WINDOW", lambda:self.close_window(window))
        types_dict = {"real":True, "virtual":False}

        img_logo = ImageTk.PhotoImage(Image.open("logo.png"))
        logo_label = Label(window, image=img_logo).grid(row=0, column = 0, columnspan =2)

        nickname_label = Label(window, text= self.languages["nickname"][self.chosen_language] + ": ").grid(row=1, column = 0, sticky=E, padx = 5)
        nickname_entry = Entry(window, width=10)
        nickname_entry.grid(row=1, column=1, sticky=W, padx = 5)
        nickname_entry.insert(0, self.languages["player"][self.chosen_language])

        color = StringVar()
        color.set(self.languages["colors"][self.chosen_language][0])
        color_label = Label(window, text = self.languages["color"][self.chosen_language] + ": ").grid(row=2, column=0, sticky=E, padx = 5)
        choose_color = OptionMenu(window, color, *self.languages["colors"][self.chosen_language])
        choose_color.grid(row=2, column=1, sticky=W, padx = 5)

        type = StringVar()
        type.set(self.languages["types"][self.chosen_language][0])
        type_label = Label(window, text = self.languages["type"][self.chosen_language] + ": ").grid(row=3, column=0, sticky=E, padx = 5)
        choose_type = OptionMenu(window, type, *self.languages["types"][self.chosen_language])
        choose_type.grid(row=3, column=1, sticky=W, padx = 5)

        choose_button = Button(window, text=self.languages["add_player"][self.chosen_language], command=lambda:self.add_player(self.color_types_dict[color.get()], types_dict[self.color_types_dict[type.get()]], nickname_entry.get(), window), padx=20)
        choose_button.grid(row=4, column=0, sticky=E, padx = 5)
        start_button = Button(window, text=self.languages["start_game"][self.chosen_language], command=lambda:self.board_init(window), padx=20)
        start_button.grid(row=4, column=1, sticky=W, padx = 5)

        back_button = Button(window, text=self.languages["back"][self.chosen_language], command=lambda:self.back_to_menu(window), padx = 20)
        back_button.grid(row=5, column=0, columnspan = 2, padx = 5, pady = 5)

        window.mainloop()

    def display_podium(self, end, player):
        if player.podium == 1:
            first_label = Label(master=end, text=f"1.{player.nickname}\n{player.points} points").grid(row = 0, column = 2)
        if player.podium == 2:
            second_label = Label(master=end, text=f"2.{player.nickname}\n{player.points} points").grid(row = 0, column = 1)
        if player.podium == 3:
            third_label = Label(master=end, text=f"3.{player.nickname}\n{player.points} points").grid(row = 0, column = 3)
        if player.podium == 4:
            fourth_label = Label(master=end, text=f"4.{player.nickname}\n{player.points} points").grid(row = 3 , column = 2)

    def end_window(self):
        end = Toplevel(board)
        end.title(self.languages["title"][self.chosen_language])
        global podium_img
        podium_img = ImageTk.PhotoImage(Image.open("podium.png"))
        podium_label = Label(master=end, image=podium_img).grid(row=0, column = 1, columnspan = 3, rowspan = 2)

        #Add winners to leaders list
        self.save_leaders()

        #Display winners 
        for player in self.real_player:
            self.display_podium(end, player)
        for player in self.virtual_player:
            self.display_podium(end, player)

        #Delete saved game
        save = sqlite3.connect('saved_game.db')
        c = save.cursor()
        c.execute("drop table if exists players")
        save.close()

        end.mainloop()

    def disable_event(self):
        pass

    def close_window(self, prev_window):
        self.yes_now_popup(self.languages["popup_end"][self.chosen_language])
        if response == 1:
            prev_window.destroy()
            prev_window.quit()

    def save_popup(self):
        self.yes_now_popup(self.languages["popup_save"][self.chosen_language])
        if response == 1:
            self.save_game()

    def control_game(self):
        if self.continue_game == True:
            while(1):
                if self.chosen_type == "virtual":
                    self.hide_roll_button = DISABLED
                    self.hide_select_button = DISABLED
                    self.hide_radio_buttons = DISABLED
                    self.hide_give_up_button = DISABLED
                    self.side_panel()
                    self.dice()
                    self.tksleep(self.default_virtual_speed)
                    self.select_counter(0)
                    if self.chosen_type == "virtual":
                        self.side_panel()
                    self.tksleep(self.default_virtual_speed)
                    if self.continue_game == False:
                        self.control_game()
                else:
                    self.hide_roll_button = NORMAL
                    self.hide_give_up_button = NORMAL
                    self.hide_radio_buttons = NORMAL
                    self.side_panel()
                    break
        else:
            self.hide_roll_button = DISABLED
            self.hide_select_button = DISABLED
            self.hide_radio_buttons = DISABLED
            self.hide_give_up_button = DISABLED
            self.side_panel()
            self.end_window()

    def board_init(self, prev_window):
        if (len(self.real_player) + len(self.virtual_player)) == 0:
            Error_label = Label(prev_window, text=self.languages["no_players"][self.chosen_language]).grid(row=5, column = 0, columnspan=2)
        else:
            self.start_game = True
            prev_window.destroy()
            prev_window.quit()
            global board
            board = Tk()
            board.title(self.languages["title"][self.chosen_language])
            board.protocol("WM_DELETE_WINDOW", lambda:self.close_window(board))
            if self.show_board_pos == True:
                img_board = ImageTk.PhotoImage(Image.open("board/board_pos.png"))
            else:
                img_board = ImageTk.PhotoImage(Image.open("board/board.png"))
            adjust_label = []
            adjust_block = ImageTk.PhotoImage(Image.open("board/adjust_block.png"))
            
            for i in range(1, 12):
                for j in range(1, 12):
                    adjust_label.append(Label(board, image=adjust_block).grid(row=i, column=j))

            board_label = Label(image=img_board).grid(row=1, column=1, columnspan=11, rowspan=11, pady=0)


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

            button_quit = Button(board, text = self.languages["end"][self.chosen_language], command = lambda:self.close_window(board), padx=30).grid(column=0, row = 11)           

            board.mainloop()

    def yes_now_popup(self, message):
        global response
        response = messagebox.askyesno(self.languages["title"][self.chosen_language], message)     

    def set_options(self, prev_window, language, show_pos, show_board_pos, show_dev_mode, show_errors, virtual_speed):

        self.yes_now_popup(self.languages["popup_options"][self.chosen_language])
        prev_window.destroy()

        if response == 1:
            self.default_virtual_speed = virtual_speed

            if show_errors == self.languages["lan_yes"][self.chosen_language]:
                self.show_errors = True
            if show_errors == self.languages["lan_no"][self.chosen_language]:
                self.show_errors = False

            if show_dev_mode == self.languages["lan_yes"][self.chosen_language]:
                self.developer_mode = True
            if show_dev_mode == self.languages["lan_no"][self.chosen_language]:
                self.developer_mode = False

            if show_board_pos == self.languages["lan_yes"][self.chosen_language]:
                self.show_board_pos = True
            if show_board_pos == self.languages["lan_no"][self.chosen_language]:
                self.show_board_pos = False

            if show_pos == self.languages["lan_yes"][self.chosen_language]:
                self.show_counters_pos = True
            if show_pos == self.languages["lan_no"][self.chosen_language]:
                self.show_counters_pos = False

            if language == self.color_types_dict["languages"][0][0]:
                self.chosen_language = 0
            if language == self.color_types_dict["languages"][0][1]:
                self.chosen_language = 1
        
        self.main_menu()

    def back_to_menu(self, prev_window):
        prev_window.destroy()
        self.main_menu()

    def options_menu(self, prev_window):
        prev_window.destroy()
        start = Tk()
        start.title(self.languages["title"][self.chosen_language])
        start.protocol("WM_DELETE_WINDOW", lambda:self.close_window(start))
        global img_logo
        img_logo = ImageTk.PhotoImage(Image.open("logo.png"))
        logo_label = Label(start, image=img_logo).grid(row=0, column = 0, columnspan=2)

        #Choose Language
        language_label = Label(start, text = self.languages["language"][self.chosen_language] + ":").grid(row=1, column = 0, sticky = E, padx = 5)
        select_language = StringVar()
        select_language.set(self.color_types_dict["languages"][self.chosen_language][self.chosen_language])
        choose_language = OptionMenu(start, select_language, *self.color_types_dict["languages"][self.chosen_language])
        choose_language.grid(row=1, column=1, sticky=W, padx = 5)

        #Show Counters position
        counters_pos_label = Label(start, text = self.languages["show_counters_pos"][self.chosen_language] + ":").grid(row=2, column = 0, sticky = E, padx = 5)
        select_counters_pos = StringVar()
        if self.show_counters_pos == True:
            select_counters_pos.set(self.languages["lan_yes"][self.chosen_language])
        if self.show_counters_pos == False:
            select_counters_pos.set(self.languages["lan_no"][self.chosen_language])
        show_counters = OptionMenu(start, select_counters_pos, *(self.languages["lan_yes"][self.chosen_language], self.languages["lan_no"][self.chosen_language]))
        show_counters.grid(row=2, column=1, sticky=W, padx = 5)

        #Load board with boxes coordinates
        board_pos_label = Label(start, text = self.languages["show_board_pos"][self.chosen_language] + ":").grid(row=3, column = 0, sticky = E, padx = 5)
        select_board_pos = StringVar()
        if self.show_board_pos == True:
            select_board_pos.set(self.languages["lan_yes"][self.chosen_language])
        if self.show_board_pos == False:
            select_board_pos.set(self.languages["lan_no"][self.chosen_language])
        show_board = OptionMenu(start, select_board_pos, *(self.languages["lan_yes"][self.chosen_language], self.languages["lan_no"][self.chosen_language]))
        show_board.grid(row=3, column=1, sticky=W, padx = 5)

         #Developer mode
        dev_mode_label = Label(start, text = self.languages["show_dev_mode"][self.chosen_language] + ":").grid(row=4, column = 0, sticky = E, padx = 5)
        select_dev_mode = StringVar()
        if self.developer_mode == True:
            select_dev_mode.set(self.languages["lan_yes"][self.chosen_language])
        if self.developer_mode == False:
            select_dev_mode.set(self.languages["lan_no"][self.chosen_language])
        show_dev_mode = OptionMenu(start, select_dev_mode, *(self.languages["lan_yes"][self.chosen_language], self.languages["lan_no"][self.chosen_language]))
        show_dev_mode.grid(row=4, column=1, sticky=W, padx = 5)
 
          #Show Errors
        show_errors_label = Label(start, text = self.languages["show_errors"][self.chosen_language] + ":").grid(row=5, column = 0, sticky = E, padx = 5)
        select_show_errors = StringVar()
        if self.show_errors == True:
            select_show_errors.set(self.languages["lan_yes"][self.chosen_language])
        if self.show_errors == False:
            select_show_errors.set(self.languages["lan_no"][self.chosen_language])
        show_errors = OptionMenu(start, select_show_errors, *(self.languages["lan_yes"][self.chosen_language], self.languages["lan_no"][self.chosen_language]))
        show_errors.grid(row=5, column=1, sticky=W, padx = 5)

          #Virtual player speed
        virtual_speed_label = Label(start, text = self.languages["virtual_speed"][self.chosen_language] + ":").grid(row=6, column = 0, sticky = E, padx = 5)
        virtual_speed = IntVar()
        virtual_speed.set(self.default_virtual_speed)
        virtual_option = OptionMenu(start, virtual_speed, *(0.25,0.5,1,2))
        virtual_option.grid(row=6, column=1, sticky=W, padx = 5)

        save_button = Button(start, text=self.languages["save"][self.chosen_language], command=lambda:self.set_options(start, select_language.get(), select_counters_pos.get(), select_board_pos.get(), select_dev_mode.get(), select_show_errors.get(), virtual_speed.get()), padx = 20).grid(row = 10, column=0, pady = 5)
        discard_button = Button(start, text=self.languages["discard"][self.chosen_language], command=lambda:self.back_to_menu(start), padx = 20).grid(row=10, column=1, pady = 5)

    def delete_leaders(self, prev_window):
        self.yes_now_popup(self.languages["popup_leaders"][self.chosen_language])
        if response == 1:
            leaders = sqlite3.connect('leaders.db')
            c = leaders.cursor()
            c.execute("drop table if exists players")
            c.close()
            leaders.close()
        self.back_to_menu(prev_window)

    def leadership(self, prev_window):
        prev_window.destroy()
        start = Tk()
        start.title(self.languages["title"][self.chosen_language])
        start.protocol("WM_DELETE_WINDOW", lambda:self.close_window(start))
        global img_logo
        img_logo = ImageTk.PhotoImage(Image.open("logo.png"))
        logo_label = Label(start, image=img_logo).grid(row=0, column = 0, columnspan=2)

        try:
            conn = sqlite3.connect('leaders.db')
            c = conn.cursor()
            c.execute("SELECT *, oid FROM players")
            records = c.fetchall()
            score_label = Label(start, text=self.languages["scoreboard"][self.chosen_language]).grid(row=1, column=0, columnspan =2)

            #Creating new list where player with the biggest score are on top
            new_records = []
            while(1):
                if len(new_records) == len(records):
                    break
                else:
                    for j in range(len(records)):
                        best_record = j
                        if records[j] in new_records:
                            print()
                        else:
                            for i in range(len(records)):
                                if records[i] in new_records:
                                    print()
                                else:
                                    if int(records[i][2]) >= int(records[best_record][2]):
                                        best_record = i            
                            new_records.append(records[best_record])
                
            #Display list 
            list_of_players = ""
            i = 0
            for player in new_records:
                i += 1
                list_of_players += f"[{i}] {player[0]} - {self.languages[player[1]][self.chosen_language].lower()} => {player[2]} {self.languages['points'][self.chosen_language]}.\n"
            score_list_label = Label(start, text=list_of_players).grid(row=2,column=0, columnspan=2)

            c.close()
            delete_btn = Button(start, text=self.languages["delete_records"][self.chosen_language], command = lambda:self.delete_leaders(start)).grid(row=3, column=1, pady=5)
            back_btn = Button(start, text=self.languages["back"][self.chosen_language], command = lambda:self.back_to_menu(start)).grid(row=3, column=0, pady=5)
        except:
            no_data_label = Label(start, text = self.languages["no_leaders"][self.chosen_language]).grid(row = 1, column=0, columnspan =2)
            back_btn = Button(start, text=self.languages["back"][self.chosen_language], command = lambda:self.back_to_menu(start), padx = 20).grid(row=3, column=0, columnspan=2, pady=5)



        start.mainloop()

    def load_game(self, start):
        conn = sqlite3.connect('saved_game.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM players")
        records = c.fetchall()
        for player in records:
            if player[2] == 'real':
                is_real = True
                players_number = len(self.real_player)
            else:
                is_real = False
                players_number = len(self.virtual_player)

            self.add_player(player[1], is_real, player[0], start)

            if is_real == True:
                load_player = self.real_player[players_number]
            else:
                load_player = self.virtual_player[players_number]

            load_player.points = player[3]
            load_player.podium = player[4]
            load_player.counters[0].position[0] = player[5]
            load_player.counters[0].position[1] = player[6]
            load_player.counters[1].position[0] = player[7]
            load_player.counters[1].position[1] = player[8]
            load_player.counters[2].position[0] = player[9]
            load_player.counters[2].position[1] = player[10]
            load_player.counters[3].position[0] = player[11]
            load_player.counters[3].position[1] = player[12]

        conn.close()
        self.board_init(start)        

    def main_menu(self):
        start = Tk()
        start.title(self.languages["title"][self.chosen_language])
        start.protocol("WM_DELETE_WINDOW", lambda:self.close_window(start))

        try:
            conn = sqlite3.connect('saved_game.db')
            c = conn.cursor()
            c.execute("SELECT *, oid FROM players")
            c.close()
            load_game_status = NORMAL
        except:
            load_game_status = DISABLED

        img_logo = ImageTk.PhotoImage(Image.open("logo.png"))
        logo_label = Label(start, image=img_logo).grid(row=0, column = 0)
        new_game_button = Button(start, text=self.languages["new_game"][self.chosen_language], command = lambda:self.new_game_menu(start), padx = 20).grid(row=1, column=0, pady=5)
        load_game_button = Button(start, text=self.languages["load_game"][self.chosen_language], command = lambda:self.load_game(start), state=load_game_status, padx=18).grid(row=2, column=0, pady=5)
        leadership_button = Button(start, text=self.languages["scoreboard"][self.chosen_language], command = lambda:self.leadership(start), padx = 2).grid(row=3, column=0, pady=5)
        options_button = Button(start, text=self.languages["options"][self.chosen_language], command = lambda:self.options_menu(start), padx = 27).grid(row=4, column=0, pady=5)
        end_button = Button(start, text=self.languages["end"][self.chosen_language], command = lambda:self.close_window(start), padx = 38).grid(row=5, column = 0, pady=5)

        start.mainloop()

game = Ludo() 
game.main_menu()