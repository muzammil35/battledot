import threading
import random
import time


class Player:
    
    def __init__(self, name):
        
        self.name = name
        self.row = None
        self.col = None
        self.grid = self.init_grid()
        self.target = None
        self.dead = False
    
    def init_grid(self):
        
        grid = [['.' for _ in range(10)] for _ in range(10)]
        row = random.randint(0, 9)
        self.row = row
        col = random.randint(0, 9)
        self.col = col
        grid[row][col] = 'S'
        return grid
    
    def print_board(self, log_file, shot_row=None, shot_col=None):
        hit = False
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (shot_row is not None and shot_col is not None) and i == shot_row and j == shot_col:
                    if self.grid[i][j] == 'S':
                        log_file.write('O ')
                        hit = True
                    else:
                        log_file.write('X ')
                elif self.grid[i][j] == 'S':
                    if not hit:
                        log_file.write('S ')
                else:
                    log_file.write('. ')
            log_file.write('\n') 
    
    def get_position(self,players):
        for pos,player in enumerate(players):
            if player.name == self.name:
                return pos
        return None
            
    

    def attack(self, log_file):
        
        if self.target and not self.dead:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            global last_shot_col 
            last_shot_col= col
            global last_shot_row 
            last_shot_row = row
            
            target_row, target_col = self.target.row, self.target.col
            if row == target_row and col == target_col:
                log_file.write(f"{self.name} hit {self.target.name}! (turn: {turn_counter})")
                log_file.write('\n')
                
                
                
                self.target.dead = True
                return True,self.target
            else:
                
                log_file.write(f"{self.name} missed {self.target.name}. (turn: {turn_counter})")
                log_file.write('\n')
                
     
                return False,self.target
    
    def set_target_and_attack(self, players, log_file):
        
      
        
        pos = self.get_position(players)
        
        if(pos == None):
            print("player that gave none: ", self.name)
            return (None,None)
        
        if(pos == len(players)-1):
            self.target = players[0]
            
        else:
            self.target = players[pos+1]
            
        return self.attack(log_file)
    
def play_game(players, lock, player, log_file):
    
    target_hit,target = player.set_target_and_attack(players, log_file)
    if target_hit:
        lock.acquire()
        try:
            players.remove(target)
        finally:
            lock.release()
    time.sleep(0.2)

#global var that counts turn
turn_counter = 0

last_shot_col = None
last_shot_row = None

target_ind = None
     
def main():
    
   
    log_file = open("game_log.txt", "w")
    
    num_players = 5
    players = [Player(chr(65 + i)) for i in range(num_players)]
    
    
    lock = threading.Lock()
    player_counter = 0
    
    while(len(players) > 1):
        
        
       
        
        player_threads = []
        for player in players:
            
            if(not player.dead):
                thread = threading.Thread(target=play_game, args=(players, lock, player, log_file))
                player_threads.append(thread)
                thread.start()
                
                global last_shot_row
                global last_shot_col
                print("last_shot_row", last_shot_row)
                print("last_shot_col", last_shot_col)
                
                target_player = player.target
                target_player.print_board(log_file,last_shot_row,last_shot_col)
                
        global turn_counter
        turn_counter += 1
    
        for thread in player_threads:
            thread.join()
            
    
    log_file.write(f"{players[0].name} WINS!!")
    
    log_file.close()

if __name__ == "__main__":
    main()
    
    
        
            
        