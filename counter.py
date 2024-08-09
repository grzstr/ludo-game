
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