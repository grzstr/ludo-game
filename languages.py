
#CREATED BY https://github.com/grzstr/ludo-game

class Languages():
    def __init__(self):
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