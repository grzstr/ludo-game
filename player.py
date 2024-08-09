from counter import Counter
import random

#CREATED BY https://github.com/grzstr/ludo-game


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
