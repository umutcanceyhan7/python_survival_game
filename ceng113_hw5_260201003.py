# Umutcan CEYHAN 260201003  
import numpy
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

class Game():
    def __init__(self,map_width,map_height,init_time, action_cost):
        # The Game initializes map parameters.
        self.mapwidth = map_width
        self.mapheight = map_height
        # The Game initializes its map with all empty squares.
        self.map = [['empty' for col in range(map_width)] for row in range(map_height)]
        # The Game creates its player object.
        self.player = Player()
        # The Game creates its time object.
        self.time = Time(0,init_time, action_cost)
        # The Game initializes the player icon.
        self.picon = person
        # The Game sets the continue state to true (still has time)
        self.cont = True
        # The Game sets the safe state to false (still not in shelter)
        self.safe = False
        # The Game initializes the list of squares that constitutes the shelter 
        self.score_map = []
        # The Game randomly inserts wood, dirt or water on the map.
        self.generate_map()
        # The Game prints the current status on the screen.
        self.update_screen()
    def generate_map(self):
        for row in range(self.mapheight):
            for col in range(self.mapwidth):
                square = numpy.random.randint(0, 11)
                if( 1 >= square <= 3):
                     self.map[row][col] = "wood "
                elif( 4 >= square <= 6):
                     self.map[row][col] = "dirt "
                elif( 7 >= square <= 8):
                     self.map[row][col] = "water"
                else:
                     self.map[row][col] = "empty"
        # For each square, put wood with probability of 0.3, put dirt with probability of 0.3,
        # put water with probability of 0.2 or leave empty with probability of 0.2. You have
        # to use 'numpy.random.randint' function.          
    def show_controls(self):        
        print()
        print("**************************** Game Control ****************************")
        print("w: up          s: down        a: left        d: rigth")
        print("1: put brick   2: put dirt    3: put plank   4: put water  5: put wood")
        print("q: pick        e: make plank  r: make brick  o: exit game")
        print("plank: 2 woods brick: 2 dirt 1 water")
        print("plank: 2 pts   brick: 3 pts   enclosed square: 3 pts")
        print("**********************************************************************")
        print()
    def show_map(self):
        ppy = self.player.pos[0]
        ppx = self.player.pos[1]
        print()
        for row in range(MAP_HEIGHT):
            color_row = [COLORS[self.map[row][c]] for c in range(MAP_WIDTH)]
            if row == ppy:
                color_row[ppx] = color_row[ppx].replace('   ',' '+self.picon+' ')
            print(''.join(color_row))    
    def update_screen(self):
        self.player.show_inventory()
        self.time.show_time()
        self.show_map()
        self.show_controls()
    def _flood_fill(self,wmf,ppx,ppy,source,target,conn8=True):
            if wmf[ppy,ppx]!=source:
                return
            wmf[ppy,ppx] = target
            if ppy>0: self._flood_fill(wmf,ppx,ppy-1,source,target,conn8)
            if ppy<wmf.shape[0]-1: self._flood_fill(wmf,ppx,ppy+1,source,target,conn8)
            if ppx>0: self._flood_fill(wmf,ppx-1,ppy,source,target,conn8)
            if ppx<wmf.shape[1]-1: self._flood_fill(wmf,ppx+1,ppy,source,target,conn8)
            if conn8:
                if ppy>0 and ppx>0: self._flood_fill(wmf,ppx-1,ppy-1,source,target,conn8)
                if ppy>0 and ppx<wmf.shape[1]-1: self._flood_fill(wmf,ppx+1,ppy-1,source,target,conn8)
                if ppy<wmf.shape[0]-1 and ppx>0: self._flood_fill(wmf,ppx-1,ppy+1,source,target),conn8
                if ppy<wmf.shape[0]-1 and ppx<wmf.shape[1]-1: self._flood_fill(wmf,ppx+1,ppy+1,source,target,conn8)
    def check_safety(self):
        # This function checks if the player is in a shelter. It should be called
        # at the end of each successfully executed action to check if the game 
        # has finished. You do not have to do anything here.
        wall_map = numpy.zeros((game.mapwidth+2,game.mapheight+2)).astype(int)
        wall_map_bool = [numpy.in1d(row, ['brick','plank']) for row in game.map]
        wall_map[1:-1,1:-1] = numpy.array(wall_map_bool).astype(int)
        label = 2
        while((wall_map == 1).any()):
            py = numpy.where(wall_map==1)[0][0]
            px = numpy.where(wall_map==1)[1][0]
            self._flood_fill(wall_map, px, py, 1, label, False)
            label += 1
        ppx = game.player.pos[1]+1
        ppy = game.player.pos[0]+1
        if not wall_map[ppy,ppx]:
            for wall in range(2,label):
                wall_map_fill = (wall_map == wall).astype(int) 
                self._flood_fill(wall_map_fill,ppx,ppy,0,label)
                edges = [wall_map_fill[0,:],wall_map_fill[-1,:], wall_map_fill[:,0],wall_map_fill[:,-1]]
                if label not in numpy.array(edges):
                    self.safe = True
                    self.score_map = wall_map_fill[1:-1,1:-1]
                    self.picon = happy
                    break
    def calc_score(self):
        final_map = (numpy.array(self.map) == 'brick').astype(int) + self.score_map
        unique, counts = numpy.unique(final_map, return_counts=True)
        score = counts[-1]*3 + counts[-2]*3 + counts[-3]*2 #area*3+brick*3+plank*2
        return score
    def move_player(self,direction):
        self.player.move(direction)
        self.update_screen()
    def pick_item(self):
        ppx = self.player.pos[0]    #satır  Row
        ppy = self.player.pos[1]    #sütun  Column
        if (self.map[ppx][ppy] == "empty"):
            print("There is nothing to pick!")
        else:
            self.player.pick(self.map[ppx][ppy])  #Picks the item where it is
            self.map[ppx][ppy] = "empty"
            self.update_screen()
        # Pick item using the player object's pick method and update the map if 
        # there is an item to pick, otherwise print "There is nothing to pick!".     
    def put_item(self,item):
        ppx = self.player.pos[0]
        ppy = self.player.pos[1]
        if(self.map[ppx][ppy] == "empty"):
            self.player.put(item)
            self.update_screen()
        else:
            print("There is nowhere to put!")
        # Put the given item using the player object's put method if the current
        # square is empty, otherwise print ""There is nowhere to put!". If the
        # player scan successfully put the item, update the map.
        pass
    def make(self,item):
        if(item == "e"):
            if(self.player.make_plank()):
                self.update_screen()
            else:
                print("Not enough material!")
        else:
            if(self.player.make_brick()):
                self.update_screen()
            else:
                print("Not enough material!")
                
        # Make the given item using the player object's corresponding method. If
        # the player can not make the item, print "Not enough material!".

class Player():
    def __init__(self):
        # Initialize the player position at the top left corner
        self.pos = [0,0]
        # Initialize the inventory as empty
        self.inventory = {'wood ':0,'dirt ':0,'water':0,'plank':0,'brick':0}
    def move(self, direction):
        # Update the player position with respect to move direction.
        if(direction == "w" ):
            if not(self.pos[0] == 0):
                self.pos[0] -= 1
                game.time.spend()
            else:
                print("Sorry I can not move up")
        elif(direction == "s"):
            if not(self.pos[0] == MAP_HEIGHT-1):
                self.pos[0] += 1   
                game.time.spend()
            else:
                print("Sorry I can not move down")
        elif(direction == "a"):
            if not(self.pos[1] == 0):
                self.pos[1] -= 1
                game.time.spend()
            else:
                print("Sorry I can not move left")
        else:
            if not(self.pos[1] == MAP_WIDTH-1):
                self.pos[1] += 1
                game.time.spend()
            else:
                print("Sorry I can not move right")
        return self.pos
        
    # Pick and update the player inventory with respect to the item.
    def pick(self, item):
        if(item == "brick"):
            self.inventory["brick"] += 1 
            game.time.spend()
        elif(item == "dirt "):
            self.inventory["dirt "] += 1
            game.time.spend()
        elif(item == "plank"):
            self.inventory["plank"] += 1
            game.time.spend()
        elif(item == "water"):
            self.inventory["water"] += 1
            game.time.spend()
        elif(item == "wood "):
            self.inventory["wood "] += 1
            game.time.spend()
        
    # Put and update the player inventory with respect to the item, if the
    # player has one or more of that item in the inventory. Return true if
    # successfully put, otherwise false.
    def put(self,item):
        ppx = game.player.pos[0]   #Row
        ppy = game.player.pos[1]   #Column
        if(item == "1"):
            if(self.inventory["brick"] >= 1):
                self.inventory["brick"] -= 1
                game.map[ppx][ppy] = "brick"
                game.time.spend()
                return True
            else:
                print("There is nothing to put!")
                return False 
        elif(item == "2"):
            if(self.inventory["dirt "]  >= 1):
                self.inventory["dirt "] -= 1
                game.map[ppx][ppy] = "dirt "
                game.time.spend()
                return True
            else:
                print("There is nothing to put!")
                return False
        elif(item == "3"):
            if(self.inventory["plank"] >= 1):
                self.inventory["plank"] -= 1
                game.map[ppx][ppy] = "plank"
                game.time.spend()
                return True
            else:
                print("There is nothing to put!")
                return False
        elif(item == "4"):
            if(self.inventory["water"] >= 1):
                self.inventory["water"] -= 1
                game.map[ppx][ppy] = "water" 
                game.time.spend()
                return True
            else:
                print("There is nothing to put!")
                return False
        else:
            if(self.inventory["wood "] >= 1):
                self.inventory["wood "] -= 1
                game.map[ppx][ppy] = "wood "
                game.time.spend()
                return True
            else:
                print("There is nothing to put!")
                return False
    # Make plank and update the player inventory with respect to the action,
    # if the player has enough materials. Return true if plank is successfully 
    # made, otherwise false.    
    def make_plank(self):
        if(self.inventory["wood "] >= 2):
            self.inventory["wood "] -= 2 
            self.inventory["plank"] += 1
            game.time.spend()
            return True
        return False
    # Make brick and update the player inventory with respect to the action,
    # if the player has enough materials. Return true if brick is successfully 
    # made, otherwise false.
    def make_brick(self):
        if(self.inventory["dirt "] >= 2 and self.inventory["water"] >= 1):
            self.inventory["dirt "] -= 2 
            self.inventory["water"] -= 1 
            self.inventory["brick"] += 1
            game.time.spend()
            return True
        return False
    
    # Shows the player inventory
    def show_inventory(self):
        print()
        c = 1
        for key in sorted(self.inventory.keys()):
            print("{}. {}\t: {}".format(c, key, (COLORS[key]+" ")*self.inventory[key]))
            c += 1
        print()   

class Time():
    def __init__(self, mins, hours, action_cost):
        self.mins = mins
        self.hours = hours
        self.action_cost = action_cost
    # Spend the action cost and update mins and/or hours. If the time is
    # up return False, otherwise True.
    def spend(self):
        if(self.hours > 0 and self.mins == 0):
            self.mins = 60
            self.mins -= self.action_cost
            self.hours -= 1
            return True
        else:
            self.mins -= self.action_cost
            if(self.hours == 0 and self.mins == 0):
                game.cont = False
                return False
            return True

        
    def show_time(self):
        print("{} hours {} minutes left!!!".format(self.hours, self.mins))


MAP_WIDTH = 10
MAP_HEIGHT = 10
ACTION_COST = 15 #minutes
INIT_TIME = 16   #hours
person =u"\u2687"        #u'U'                  #u'\u267f'                       #u'\u2687'                       
happy = u"\u263b"
COLORS = {'empty':'\033[40m   \033[0m', 'wood ':'\033[42m   \033[0m',
          'dirt ':'\033[47m   \033[0m', 'water':'\033[46m   \033[0m',
          'plank':'\033[43m   \033[0m', 'brick':'\033[41m   \033[0m'}
    
moves = {"w":"up", "s":"down", "a":"left", "d":"right"}
items = {"1":"brick", "2":"dirt ", "3":"plank", "4":"water", "5":"wood "}
products = {"e":"plank", "r":"brick"}

# A Game class is instantiated each time a new game begins.


game = Game(MAP_WIDTH, MAP_HEIGHT, INIT_TIME, ACTION_COST)
out = False

################## THIS PART CAUSES AN INFINITE LOOP!!! ##################
# Implement the game play. Take the instructions from the user and execute them.
while game.cont and not game.safe:
    instructions = input("Make your move : ")
    if(instructions == "o"):
        game.cont = False
        out = True
    elif(instructions == "a" or instructions == "w" or instructions == "d" or instructions == "s" ):
        game.move_player(instructions)
    elif(instructions == "q"):
        game.pick_item()
    elif(instructions == "1" or instructions == "2" or instructions == "3" or instructions == "4" or instructions == "5"):
        game.put_item(instructions)
    elif(instructions == "e" or instructions == "r"):
        game.make(instructions)
    game.check_safety()
    
if game.safe:
    print("Congratulations! You are safe!!!")
    print("Your score is {}.".format(game.calc_score()))
elif out:
    print("Bye!")
else:
    print("Too late! They are coming!!!")                  
