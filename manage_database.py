import sqlite3
from languages import Languages

class Database():
    def __init__(self):
        self.leaders_base = 'leaders.db'
        self.save_base = 'saved_game.db'
        self.languages = Languages().languages


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

    def save_leaders(self, real_player, virtual_player):
        leaders = sqlite3.connect(self.leaders_base)
        c = leaders.cursor()
        c.execute("""CREATE TABLE if not exists players (
                nickname text,
                type text,
                points integer
                )""")    
        
        for player in real_player:
            self.add_leader(leaders, player, "real")
        for player in virtual_player:
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

    def save_game(self, real_player, virtual_player):
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
        
        for player in real_player:
            self.add_player_to_save(save, player, "real")
        for player in virtual_player:
            self.add_player_to_save(save, player, "virtual")
        save.close()

    def delete_saved_game(self):
        save = sqlite3.connect(self.save_base)
        c = save.cursor()
        c.execute("drop table if exists players")
        save.close()

    def delete_leaders(self):
        leaders = sqlite3.connect(self.leaders_base)
        c = leaders.cursor()
        c.execute("drop table if exists players")
        c.close()
        leaders.close()

    def leadership(self, chosen_language):
        conn = sqlite3.connect(self.leaders_base)
        c = conn.cursor()
        c.execute("SELECT *, oid FROM players")
        records = c.fetchall()

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
            list_of_players += f"[{i}] {player[0]} - {self.languages[player[1]][chosen_language].lower()} => {player[2]} {self.languages['points'][chosen_language]}.\n"
        c.close()  

        return list_of_players
    
    def load_game(self):
        conn = sqlite3.connect(self.save_base)
        c = conn.cursor()
        c.execute("SELECT *, oid FROM players")
        records = c.fetchall()
        conn.close()
        return records
    
    def check_saved_games(self):
        conn = sqlite3.connect(self.save_base)
        c = conn.cursor()
        c.execute("SELECT *, oid FROM players")
        c.close()