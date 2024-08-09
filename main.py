from tkinter import *
from tkinter import  _get_default_root
from tkinter import messagebox
from datetime import datetime
from PIL import ImageTk, Image
from languages import Languages
from ludo import Ludo

#CREATED BY https://github.com/grzstr/ludo-game
class GUI():
    def __init__(self):
        self.game = Ludo()
        self.start_game = False
        self.developer_mode = False
        self.default_virtual_speed = 1

        #LANGUAGES DICTIONARIES
        self.color_types_dict = Languages().color_types_dict
        self.languages = Languages().languages

        self.hide_roll_button = NORMAL
        self.hide_radio_buttons = NORMAL
        self.hide_give_up_button = NORMAL
        self.show_counters_pos = False
        self.show_board_pos = False
        
        self.window = Tk()
        self.window.title(self.languages["title"][self.game.chosen_language])
        self.window.protocol("WM_DELETE_WINDOW", lambda:self.close_window(self.window))
        self.load_menu_images()
        self.main_menu()
        self.window.mainloop()

    def load_menu_images(self):
        global img_logo
        img_logo = ImageTk.PhotoImage(Image.open("logo.png"))

    def load_board_images(self):
        global img_red_counter_1
        global img_red_counter_2
        global img_red_counter_3
        global img_red_counter_4

        global img_green_counter_1
        global img_green_counter_2
        global img_green_counter_3
        global img_green_counter_4

        global img_yellow_counter_1
        global img_yellow_counter_2
        global img_yellow_counter_3
        global img_yellow_counter_4

        global img_blue_counter_1
        global img_blue_counter_2
        global img_blue_counter_3
        global img_blue_counter_4

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

        global dice
        dice = []

        dice.append(dice_one)
        dice.append(dice_two)   
        dice.append(dice_three)   
        dice.append(dice_four)   
        dice.append(dice_five)   
        dice.append(dice_six)      

        global img_board
        global adjust_block

        if self.show_board_pos == True:
            img_board = ImageTk.PhotoImage(Image.open("board/board_pos.png"))
        else:
            img_board = ImageTk.PhotoImage(Image.open("board/board.png"))
        
        adjust_block = ImageTk.PhotoImage(Image.open("board/adjust_block.png"))

    def add_player(self, color, is_real, nickname):
        self.game.add_player(color, is_real, nickname)

        for x in range(len(self.game.real_player)):
            players_number_label = Label(self.window, text=f"[{len(self.game.real_player)+len(self.game.virtual_player)}]: {self.game.real_player[x].nickname}, {self.languages['types'][self.game.chosen_language][0]}, {self.languages[self.game.real_player[x].color][self.game.chosen_language]}")
            players_number_label.grid(row=7+len(self.game.real_player)+len(self.game.virtual_player), column=0, columnspan=2)

        for y in range(len(self.game.virtual_player)):
            virtual_number_label = Label(self.window, text=f"[{len(self.game.real_player)+len(self.game.virtual_player)}]: {self.game.virtual_player[y].nickname}, {self.languages['types'][self.game.chosen_language][1]} {self.languages[self.game.virtual_player[y].color][self.game.chosen_language]}")
            virtual_number_label.grid(row=7+len(self.game.real_player)+len(self.game.virtual_player), column=0, columnspan=2)

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
        for x in self.game.real_player:
            if self.game.chosen_color != x.color:
                i = 0
                for y in x.counters:
                    i += 1
                    self.adjust_counter_position(y, i, x.color)
            else:
                current_player = x
        for x in self.game.virtual_player:
            if self.game.chosen_color != x.color:
                i = 0
                for y in x.counters:
                    i += 1
                    self.adjust_counter_position(y, i, x.color)
            else:
                current_player = x
        
        if self.game.chosen_color != "":
            i = 0
            for y in current_player.counters:
                i += 1
                self.adjust_counter_position(y, i, current_player.color)     

    def update_dice_img(self):
        if self.game.chosen_type == "real":
            roll = self.game.real_player[self.game.chosen_index].roll - 1
            if self.developer_mode == False:
                self.hide_roll_button = DISABLED
            else:
                self.hide_roll_button = NORMAL
        else:
            roll = self.game.virtual_player[self.game.chosen_index].roll - 1
            self.hide_roll_button = DISABLED
        
        if self.game.dice_unknown == True:
            roll_label =Label(image=dice_unknown)
        else:
            roll_label = Label(image=dice[roll])
        roll_label.grid(column=0, row=2)

    def tksleep(self, t):
        ms = int(t*1000)
        root = _get_default_root('sleep')
        var = IntVar(root)
        root.after(ms, var.set, 1)
        root.wait_variable(var)

    def dice(self):
        self.game.dice()
        self.game.dice_unknown = False
        self.update_dice_img()
      
        if self.game.chosen_type == "real":
            self.board_init()

    def side_panel_scoreboard(self):
        score_title_label = Label(text=self.languages["scoreboard"][self.game.chosen_language] + ":").grid(row=1, column=12, sticky=S)
        scoreboard= ""
        p_number = 0
        for player in self.game.real_player:
            p_number += 1
            scoreboard += "[" + str(p_number) + "] " + player.nickname + " - " + self.languages[player.color][self.game.chosen_language] + " - " + f"{player.points}p"
            if player.podium == 1:
                scoreboard += f"- " + self.languages["1st"][self.game.chosen_language]
            if player.podium == 2:
                scoreboard += f"- " + self.languages["2nd"][self.game.chosen_language]
            if player.podium == 3:
                scoreboard += f"- " + self.languages["3rd"][self.game.chosen_language]
            if player.podium == 4:
                scoreboard += f"- " + self.languages["4th"][self.game.chosen_language]
            if p_number !=4:
                scoreboard += "\n"
        for player in self.game.virtual_player:
            p_number += 1
            scoreboard += "[" + str(p_number) + "] " + player.nickname + " - " + self.languages[player.color][self.game.chosen_language] + " - " + f"{player.points}p"
            if player.podium == 1:
                scoreboard += f"- " + self.languages["1st"][self.game.chosen_language]
            if player.podium == 2:
                scoreboard += f"- " + self.languages["2nd"][self.game.chosen_language]
            if player.podium == 3:
                scoreboard += f"- " + self.languages["3rd"][self.game.chosen_language]
            if player.podium == 4:
                scoreboard += f"- " + self.languages["4th"][self.game.chosen_language]           
            if p_number !=4:
                scoreboard += "\n"
        score_label = Label(text=scoreboard, anchor=SW).grid(row=2, column=12, sticky=SW)

    def side_panel_counters_position(self):
        if self.show_counters_pos == True:
            counters_title_label = Label(text= self.languages["counter_position"][self.game.chosen_language] + ":").grid(row=3, column=12, sticky=S)
            p_number = 0
            for player in self.game.real_player:
                pos_text= ""
                for i in range(4):
                    pos_text += f"[{self.languages[player.color][self.game.chosen_language]}][{player.counters[i].number}] -> [{player.counters[i].position[0]}, {player.counters[i].position[1]}]"
                    if i !=3:
                        pos_text += "\n"
                pos_label = Label(text=pos_text, anchor=SW).grid(row=4 + p_number, column=12, sticky=SW)
                p_number += 1
            for player in self.game.virtual_player:
                pos_text= ""
                for i in range(4):
                    pos_text += f"[{self.languages[player.color][self.game.chosen_language]}][{player.counters[i].number}] -> [{player.counters[i].position[0]}, {player.counters[i].position[1]}]"
                    if i !=3:
                        pos_text += "\n"
                pos_label = Label(text=pos_text, anchor=SW).grid(row=4 + p_number, column=12, sticky=SW)
                p_number += 1

    def side_panel(self):
        counter_number = [("1", 1),
                          ("2", 2),
                          ("3", 3),
                          ("4", 4)]
    
        try:
            button_roll = Button(self.window, text = self.languages["roll"][self.game.chosen_language], padx=18, command=self.dice, state=self.hide_roll_button)
            self.update_dice_img()

            button_roll.grid(column=0, row=3)
            chosen_color_label = Label(text= self.languages["chosen_color"][self.game.chosen_language] + f":\n{self.languages[self.game.chosen_color][self.game.chosen_language]}", bg = self.game.chosen_color).grid(column=0, row =1)

            give_up_button = Button(self.window, text=self.languages["give_up"][self.game.chosen_language], padx=18, command=self.give_up, state=self.hide_give_up_button).grid(column=0, row=4)

            selected_counter = IntVar()
            selected_counter.set(self.game.select)
            
            i = 0 
            for text, mode in counter_number:
                Radiobutton(self.window, text=text, variable= selected_counter, value=mode, state=self.hide_radio_buttons).grid(column=0, row=5 + i)
                i += 1

            save_button = Button(self.window, text=self.languages["save_game"][self.game.chosen_language], command=self.save_popup)
            save_button.grid(column=0, row=10)

            choose_counter_button = Button(self.window, text=self.languages["move_counter"][self.game.chosen_language], state=self.game.hide_select_button,command=lambda:self.select_counter(selected_counter.get()-1))
            choose_counter_button.grid(column=0, row=9)

            self.side_panel_scoreboard()
            self.side_panel_counters_position()
        except:
            pass


    def new_game_menu(self):
        self.destroy_widgets(self.window)
        self.window.title(self.languages["title"][self.game.chosen_language])
        self.window.geometry("392x450")
        self.window.protocol("WM_DELETE_WINDOW", lambda:self.close_window(self.window))
        self.load_board_images()
        types_dict = {"real":True, "virtual":False}

        logo_label = Label(self.window, image=img_logo).grid(row=0, column = 0, columnspan =2)

        nickname_label = Label(self.window, text= self.languages["nickname"][self.game.chosen_language] + ": ").grid(row=1, column = 0, sticky=E, padx = 5)
        nickname_entry = Entry(self.window, width=10)
        nickname_entry.grid(row=1, column=1, sticky=W, padx = 5)
        nickname_entry.insert(0, self.languages["player"][self.game.chosen_language])

        color = StringVar()
        color.set(self.languages["colors"][self.game.chosen_language][0])
        color_label = Label(self.window, text = self.languages["color"][self.game.chosen_language] + ": ").grid(row=2, column=0, sticky=E, padx = 5)
        choose_color = OptionMenu(self.window, color, *self.languages["colors"][self.game.chosen_language])
        choose_color.grid(row=2, column=1, sticky=W, padx = 5)

        type = StringVar()
        type.set(self.languages["types"][self.game.chosen_language][0])
        type_label = Label(self.window, text = self.languages["type"][self.game.chosen_language] + ": ").grid(row=3, column=0, sticky=E, padx = 5)
        choose_type = OptionMenu(self.window, type, *self.languages["types"][self.game.chosen_language])
        choose_type.grid(row=3, column=1, sticky=W, padx = 5)

        choose_button = Button(self.window, text=self.languages["add_player"][self.game.chosen_language], command=lambda:self.add_player(self.color_types_dict[color.get()], types_dict[self.color_types_dict[type.get()]], nickname_entry.get()), padx=20)
        choose_button.grid(row=4, column=0, sticky=E, padx = 5)
        start_button = Button(self.window, text=self.languages["start_game"][self.game.chosen_language], command=lambda:self.board_init(), padx=20)
        start_button.grid(row=4, column=1, sticky=W, padx = 5)

        back_button = Button(self.window, text=self.languages["back"][self.game.chosen_language], command=lambda:self.main_menu(), padx = 20)
        back_button.grid(row=5, column=0, columnspan = 2, padx = 5, pady = 5)

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
        end = Toplevel(self.window)
        end.title(self.languages["title"][self.game.chosen_language])
        global podium_img
        podium_img = ImageTk.PhotoImage(Image.open("podium.png"))
        podium_label = Label(master=end, image=podium_img).grid(row=0, column = 1, columnspan = 3, rowspan = 2)

        #Add winners to leaders list
        self.game.database.save_leaders(self.game.real_player, self.game.virtual_player)

        #Display winners 
        for player in self.game.real_player:
            self.display_podium(end, player)
        for player in self.game.virtual_player:
            self.display_podium(end, player)

        #Delete saved game
        self.game.database.delete_saved_game()

        end.mainloop()

    def disable_event(self):
        pass

    def close_window(self, prev_window):
        self.yes_now_popup(self.languages["popup_end"][self.game.chosen_language])
        if response == 1:
            prev_window.destroy()
            prev_window.quit()

    def save_popup(self):
        self.yes_now_popup(self.languages["popup_save"][self.game.chosen_language])
        if response == 1:
            self.game.database.save_game(self.game.real_player, self.game.virtual_player)

    def give_up(self):
        self.game.give_up()
        self.update_counters_pos()
        self.game.next_color()
        self.control_game()

    def select_counter(self, select):
        self.game.select_counter(select)
        self.update_counters_pos()
        if self.game.chosen_type == "real":
            self.side_panel()
            self.control_game()

    def control_game(self):
        if self.game.continue_game == True:
            while(1):
                if self.game.chosen_type == "virtual":
                    self.hide_roll_button = DISABLED
                    self.game.hide_select_button = DISABLED
                    self.hide_radio_buttons = DISABLED
                    self.hide_give_up_button = DISABLED
                    self.side_panel()
                    self.dice()
                    self.tksleep(self.default_virtual_speed)
                    self.select_counter(0)
                    if self.game.chosen_type == "virtual":
                        self.side_panel()
                    self.tksleep(self.default_virtual_speed)
                    if self.game.continue_game == False:
                        self.control_game()
                else:
                    self.hide_roll_button = NORMAL
                    self.hide_give_up_button = NORMAL
                    self.hide_radio_buttons = NORMAL
                    self.side_panel()
                    break
        else:
            self.hide_roll_button = DISABLED
            self.game.hide_select_button = DISABLED
            self.hide_radio_buttons = DISABLED
            self.hide_give_up_button = DISABLED
            self.side_panel()
            self.end_window()

    def show_board(self):
        self.destroy_widgets(self.window)
        self.window.title(self.languages["title"][self.game.chosen_language])
        self.window.geometry("1080x800")
        self.window.protocol("WM_DELETE_WINDOW", lambda:self.close_window(self.window))
        adjust_label = []
        for i in range(1, 12):
            for j in range(1, 12):
                adjust_label.append(Label(self.window, image=adjust_block).grid(row=i, column=j))

        board_label = Label(image=img_board).grid(row=1, column=1, columnspan=11, rowspan=11, pady=0)

        global red_counter
        global green_counter
        global yellow_counter
        global blue_counter

        red_counter = []
        green_counter = []
        yellow_counter = []
        blue_counter = []

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

        self.update_counters_pos()

    def board_init(self):
        if (len(self.game.real_player) + len(self.game.virtual_player)) == 0:
            Error_label = Label(self.window, text=self.languages["no_players"][self.game.chosen_language]).grid(row=5, column = 0, columnspan=2)
        else:
            self.start_game = True
            self.show_board()

            self.game.next_color()
            self.update_counters_pos()
            self.control_game()

            button_quit = Button(self.window, text = self.languages["end"][self.game.chosen_language], command = lambda:self.close_window(self.window), padx=30).grid(column=0, row = 11)           

    def yes_now_popup(self, message):
        global response
        response = messagebox.askyesno(self.languages["title"][self.game.chosen_language], message)     

    def set_options(self, language, show_pos, show_board_pos, show_dev_mode, show_errors, virtual_speed):

        self.yes_now_popup(self.languages["popup_options"][self.game.chosen_language])
        self.destroy_widgets(self.window)

        if response == 1:
            self.default_virtual_speed = virtual_speed

            if show_errors == self.languages["lan_yes"][self.game.chosen_language]:
                self.game.show_errors = True
            if show_errors == self.languages["lan_no"][self.game.chosen_language]:
                self.game.show_errors = False

            if show_dev_mode == self.languages["lan_yes"][self.game.chosen_language]:
                self.developer_mode = True
            if show_dev_mode == self.languages["lan_no"][self.game.chosen_language]:
                self.developer_mode = False

            if show_board_pos == self.languages["lan_yes"][self.game.chosen_language]:
                self.show_board_pos = True
            if show_board_pos == self.languages["lan_no"][self.game.chosen_language]:
                self.show_board_pos = False

            if show_pos == self.languages["lan_yes"][self.game.chosen_language]:
                self.show_counters_pos = True
            if show_pos == self.languages["lan_no"][self.game.chosen_language]:
                self.show_counters_pos = False

            if language == self.color_types_dict["languages"][0][0]:
                self.game.chosen_language = 0
            if language == self.color_types_dict["languages"][0][1]:
                self.game.chosen_language = 1
        
        self.main_menu()

    def back_to_menu(self, prev_window):
        prev_window.destroy()
        self.main_menu()

    def destroy_widgets(self, window):
        try:
            for widget in window.winfo_children():
                widget.destroy()
        except:
            pass

    def options_menu(self):
        self.destroy_widgets(self.window)
        self.window.title(self.languages["title"][self.game.chosen_language])
        self.window.protocol("WM_DELETE_WINDOW", lambda:self.close_window(self.window))
        logo_label = Label(self.window, image=img_logo).grid(row=0, column = 0, columnspan=2)

        #Choose Language
        language_label = Label(self.window, text = self.languages["language"][self.game.chosen_language] + ":").grid(row=1, column = 0, sticky = E, padx = 5)
        select_language = StringVar()
        select_language.set(self.color_types_dict["languages"][self.game.chosen_language][self.game.chosen_language])
        choose_language = OptionMenu(self.window, select_language, *self.color_types_dict["languages"][self.game.chosen_language])
        choose_language.grid(row=1, column=1, sticky=W, padx = 5)

        #Show Counters position
        counters_pos_label = Label(self.window, text = self.languages["show_counters_pos"][self.game.chosen_language] + ":").grid(row=2, column = 0, sticky = E, padx = 5)
        select_counters_pos = StringVar()
        if self.show_counters_pos == True:
            select_counters_pos.set(self.languages["lan_yes"][self.game.chosen_language])
        if self.show_counters_pos == False:
            select_counters_pos.set(self.languages["lan_no"][self.game.chosen_language])
        show_counters = OptionMenu(self.window, select_counters_pos, *(self.languages["lan_yes"][self.game.chosen_language], self.languages["lan_no"][self.game.chosen_language]))
        show_counters.grid(row=2, column=1, sticky=W, padx = 5)

        #Load board with boxes coordinates
        board_pos_label = Label(self.window, text = self.languages["show_board_pos"][self.game.chosen_language] + ":").grid(row=3, column = 0, sticky = E, padx = 5)
        select_board_pos = StringVar()
        if self.show_board_pos == True:
            select_board_pos.set(self.languages["lan_yes"][self.game.chosen_language])
        if self.show_board_pos == False:
            select_board_pos.set(self.languages["lan_no"][self.game.chosen_language])
        show_board = OptionMenu(self.window, select_board_pos, *(self.languages["lan_yes"][self.game.chosen_language], self.languages["lan_no"][self.game.chosen_language]))
        show_board.grid(row=3, column=1, sticky=W, padx = 5)

         #Developer mode
        dev_mode_label = Label(self.window, text = self.languages["show_dev_mode"][self.game.chosen_language] + ":").grid(row=4, column = 0, sticky = E, padx = 5)
        select_dev_mode = StringVar()
        if self.developer_mode == True:
            select_dev_mode.set(self.languages["lan_yes"][self.game.chosen_language])
        if self.developer_mode == False:
            select_dev_mode.set(self.languages["lan_no"][self.game.chosen_language])
        show_dev_mode = OptionMenu(self.window, select_dev_mode, *(self.languages["lan_yes"][self.game.chosen_language], self.languages["lan_no"][self.game.chosen_language]))
        show_dev_mode.grid(row=4, column=1, sticky=W, padx = 5)
 
          #Show Errors
        show_errors_label = Label(self.window, text = self.languages["show_errors"][self.game.chosen_language] + ":").grid(row=5, column = 0, sticky = E, padx = 5)
        select_show_errors = StringVar()
        if self.game.show_errors == True:
            select_show_errors.set(self.languages["lan_yes"][self.game.chosen_language])
        if self.game.show_errors == False:
            select_show_errors.set(self.languages["lan_no"][self.game.chosen_language])
        show_errors = OptionMenu(self.window, select_show_errors, *(self.languages["lan_yes"][self.game.chosen_language], self.languages["lan_no"][self.game.chosen_language]))
        show_errors.grid(row=5, column=1, sticky=W, padx = 5)

          #Virtual player speed
        virtual_speed_label = Label(self.window, text = self.languages["virtual_speed"][self.game.chosen_language] + ":").grid(row=6, column = 0, sticky = E, padx = 5)
        virtual_speed = IntVar()
        virtual_speed.set(self.default_virtual_speed)
        virtual_option = OptionMenu(self.window, virtual_speed, *(0.25,0.5,1,2))
        virtual_option.grid(row=6, column=1, sticky=W, padx = 5)

        save_button = Button(self.window, text=self.languages["save"][self.game.chosen_language], command=lambda:self.set_options(select_language.get(), select_counters_pos.get(), select_board_pos.get(), select_dev_mode.get(), select_show_errors.get(), virtual_speed.get()), padx = 20).grid(row = 10, column=0, pady = 5)
        discard_button = Button(self.window, text=self.languages["discard"][self.game.chosen_language], command=lambda:self.main_menu(), padx = 20).grid(row=10, column=1, pady = 5)

    def delete_leaders(self):
        self.yes_now_popup(self.languages["popup_leaders"][self.game.chosen_language])
        if response == 1:
            self.game.database.delete_leaders()
        self.main_menu()

    def leadership(self):
        self.destroy_widgets(self.window)
        self.window.title(self.languages["title"][self.game.chosen_language])
        self.window.protocol("WM_DELETE_WINDOW", lambda:self.close_window(self.window))
        logo_label = Label(self.window, image=img_logo).grid(row=0, column = 0, columnspan=2)

        try:

            score_label = Label(self.window, text=self.languages["scoreboard"][self.game.chosen_language]).grid(row=1, column=0, columnspan =2)

            list_of_players = self.game.database.leadership(self.game.chosen_language)

            score_list_label = Label(self.window, text=list_of_players).grid(row=2,column=0, columnspan=2)

           
            delete_btn = Button(self.window, text=self.languages["delete_records"][self.game.chosen_language], command = lambda:self.delete_leaders()).grid(row=3, column=1, pady=5)
            back_btn = Button(self.window, text=self.languages["back"][self.game.chosen_language], command = lambda:self.main_menu()).grid(row=3, column=0, pady=5)
        except:
            no_data_label = Label(self.window, text = self.languages["no_leaders"][self.game.chosen_language]).grid(row = 1, column=0, columnspan =2)
            back_btn = Button(self.window, text=self.languages["back"][self.game.chosen_language], command = lambda:self.main_menu(), padx = 20).grid(row=3, column=0, columnspan=2, pady=5)

    def load_game(self):
        self.game.load_game()
        self.load_board_images()
        self.board_init()      

    def main_menu(self):
        self.destroy_widgets(self.window)
        try:
            self.game.database.check_saved_games()
            load_game_status = NORMAL
        except:
            load_game_status = DISABLED

        try:
            logo_label = Label(self.window, image=img_logo).grid(row=0, column = 0)
            new_game_button = Button(self.window, text=self.languages["new_game"][self.game.chosen_language], command = lambda:self.new_game_menu(), padx = 20).grid(row=1, column=0, pady=5)
            load_game_button = Button(self.window, text=self.languages["load_game"][self.game.chosen_language], command = lambda:self.game.load_game(), state=load_game_status, padx=18).grid(row=2, column=0, pady=5)
            leadership_button = Button(self.window, text=self.languages["scoreboard"][self.game.chosen_language], command = lambda:self.leadership(), padx = 2).grid(row=3, column=0, pady=5)
            options_button = Button(self.window, text=self.languages["options"][self.game.chosen_language], command = lambda:self.options_menu(), padx = 27).grid(row=4, column=0, pady=5)
            end_button = Button(self.window, text=self.languages["end"][self.game.chosen_language], command = lambda:self.close_window(self.window), padx = 38).grid(row=5, column = 0, pady=5)
        except:
            pass


ludo = GUI() 
ludo.main_menu()