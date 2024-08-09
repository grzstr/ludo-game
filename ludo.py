import random
from tkinter import *
from manage_database import Database
from player import Player, Virtual_Player
import random
from datetime import datetime
from languages import Languages

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
        self.hide_select_button = DISABLED
        self.select = 1
        self.continue_game = True
        self.dice_unknown = True
        self.chosen_type = ""
        self.chosen_index = 0
        self.show_errors = False
        self.roll = 0

        now = datetime.now()
        self.start_data_time = now.strftime("%d-%m-%Y_%H-%M-%S")
        self.chosen_language = 0
        self.color_types_dict = Languages().color_types_dict
        self.languages = Languages().languages
        
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

        self.database = Database()

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

    def check_nickname(self, nickname):
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

    def add_player(self, color, is_real, nickname):
        if len(self.real_player)+len(self.virtual_player) < 4:
            if color in self.colors:
                if color in self.used_colors:
                    self.error_log(self.languages["used_color"][self.chosen_language], 0, save = False)
                else:
                    nickname = self.check_nickname(nickname)
                    self.used_colors.append(color)
                    if is_real == True:
                        self.real_player.append(Player(color, self.dock_pos, self.end_pos, nickname))
                    else:
                        self.virtual_player.append(Virtual_Player(color, self.dock_pos, self.end_pos, nickname))
            else:
                self.error_log(self.languages["wrong_color"][self.chosen_language], 0, save = False)
        else:
            self.error_log(self.languages["four_players"][self.chosen_language], 0, save = False)

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


    def dice(self):
        self.roll = random.randint(1, 6)
        if self.chosen_type == "real":
            self.real_player[self.chosen_index].roll = self.roll
            self.hide_select_button = NORMAL
        else:
            self.virtual_player[self.chosen_index].roll = self.roll

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
        else:
            if player.roll != 6:
                self.next_color()
            self.dice_unknown = True 

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

        if len(self.winners) + len(self.losers) == len(self.used_colors):
            self.continue_game = False
        else:
            self.continue_game = True

    def load_game(self, start):
        records = self.database.load_game()
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

