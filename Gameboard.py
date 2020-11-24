import random as random    
import pygame as pygame
import Toolbar as tb

pygame.init()                                 #start up dat pygame
clock = pygame.time.Clock()                   #for framerate or something? still not very sure
Screen = pygame.display.set_mode([1000, 1000])  #making the window
Done = False                                  #variable to keep track if window is open
MapSize = 50                                  #how many tiles in either direction of grid

TileWidth = 20                                #pixel sizes for grid squares
TileHeight = 20
TileMargin = 3

BLACK = (0, 0, 0)                             #some color definitions
WHITE = (255, 255, 255)
GREEN = (30, 220, 20)
RED = (220, 20, 20)
BLUE = (20, 20, 235)
TRANS_BLUE = (0,0,255)

ROSEA = pygame.image.load('C:/Users/katie/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/anmlnctr/ecogen/img/ROSEA.png')
CORDY = pygame.image.load('C:/Users/katie/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/anmlnctr/ecogen/img/CORDY.png')
FABAC = pygame.image.load('C:/Users/katie/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/anmlnctr/ecogen/img/FABAC.png')

KeyLookup = {
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_DOWN: "DOWN",
    pygame.K_UP: "UP"
}

class MapTile(object):                       #The main class for stationary things that inhabit the grid ... grass, trees, rocks and stuff.
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row
        self.Image = None
        self.Nutrients = self.get_nutrients()
        self.Score = len(self.Nutrients)
        self.Type = 'Tile'
        self.Cover = False
        self.Color = self.get_color()
        self.HP = 10
        self.Energy = 100
        self.Status = 'ALIVE'
        self.collection = []
        if Name != 'BARE' and Name != 'GRASS':
            self.Type = Name
            self.collection.append(9)
            self.Name = self.get_random_instance(self.Type)

    def get_nutrients(self):
        total = random.randint(20,200)
        switch = total % 3
        nutes = []
        for n in range(1,total):
            get_num = True
            num = ''
            while (get_num):
                numby = random.randint(1,10)
                if numby < 5:
                    num+=(str(1))
                elif numby < 8:
                    num+=(str(2))
                elif numby < 10:
                    num+=(str(3))
                elif numby == 10:
                    num+=(str(4))

                if switch == 0:
                    get_num = True
                    num+='.'
                    switch = random.randint(0,3)
                else:
                    get_num = False
            nutes.append(num)
        self.Nutrients = nutes
        return nutes

    def get_random_instance(self,Type):
        trees = ['FIR','BIRCH','OAK','GNARLY OAK', 'SWAMP OAK']
        rocks = ['SHARP ROCK', 'SANDY SPOT', 'BOULDER', 'BROKEN CEMENT']
        plants = ['HOLLY','DANDELION','BURDOCK','ROSE','INDIAN PAINTBRUSH']
        r = random.randint(1,100)
        new_name = self.Name
        t = Type
        if t == 'TREE':
            p = r % (len(trees))
            new_name = trees[p]
        if t == 'ROCK':
            p = r % (len(rocks))
            new_name = rocks[p]
        if t == 'PLANT':
            p = r % (len(plants))
            new_name = plants[p]
        return new_name

    def get_color(self):
        cols = [0,0,0]
        if self.Name == 'BARE':
            cols = [161,144,144]
        if self.Name == 'GRASS':
            cols = [153,161,144]
        if self.Name == 'TREE':
            cols = [88,141,19]
        if self.Name == 'ROCK':
            cols = [56,61,48]
        if self.Name == 'PLANT':
            cols = [102,204,0]
        return tuple(cols)

    def uptake(self):
        soil = Map.Grid[self.Column][self.Row][0]
        if (self.Type == 'PLANT' or self.Type == 'TREE') and len(soil.Nutrients) > 0 and self.collection.count(9) > 0:
            uptake = soil.Nutrients.pop()
            print('On the uptake: ' + self.Name + str(self.Column) + str(self.Row) + ' : ' + str(uptake))
            self.collection.append(uptake)
            self.collection.append(9)
        if (len(soil.Nutrients))<1 or self.collection.count(9) < 1:
            self.decay()

    def decay(self):
        self.HP-=1
        self.Energy -=1
        print (self.Name + "has decayed at " + str(self.Column) + ', ' + str(self.Row))
        if self.HP == 0:
            self.die()

    def die(self):
        x = self.Column
        y = self.Row
        #spot = Map.Grid[x][y]
        print(self.Name + ' has died! At ' + str(self.Column) + ', ' + str(self.Row))
        self.Status = 'DEAD'
        #(Map.Grid[self.Column][self.Row]).remove(spot[1])
        #Map.Plants.remove(Map.Plants[x][y])

    def report_nutrients(self):
        nutes = self.Nutrients
        s = set(nutes)
        nute_report = []
        total = len(nutes)
        unique = len(s)
        if total > 0:
            biggest = max(nutes)
            def sorter(x):
                return x[2]

            nute_report.append('Total: ' + str(total) + '| Unique: ' + str(unique) + '| Longest: ' + str(biggest))
            for n in s:
                x = nutes.count(n)
                freq = x/total
                freq = "{:.2f}".format(freq)
                nute_report.append([n,x,freq])
            nute_report.sort(key=sorter)
        else:
            nute_report = 'Nothing here.'
        return nute_report


class Character(object):                    #Characters can move around and do cool stuff
    def __init__(self, Name, HP, Column, Row):
        self.Age = 1
        self.HP = HP
        self.Column = Column
        self.Row = Row
        self.Energy = 100
        self.Image = None
        self.Type ='Player'
        self.Name = Name
        self.Aggro = random.randint(0,1)
        if Name == "Organism":
            self.Type = Name
            self.Name = self.get_random_instance(self.Type)
        self.Mated = False
        self.Color = [255,255,255]

    def s_color(self,x,y,z):
        if self.Age > 5:
            r = random.randint(45,900)
            r_1 = (int(r/13))%255
            r_2 = int(r%255)
            r_3 = int(r*80)%255
            self.Color = [r_1,r_2,r_3]
        return

    def return_to_form(self):
        if self.Mated == True:
            self.Mated = False

    def get_random_instance(self,name):
        n = name
        orgs = ['BIRD', 'LARGE BIRD', 'MEAT MONSTER','INVISIBLE BIRD', 'WORM', 'TIGER', 'TWO TIGERS','LIGER']
        r = random.randint(1,100)
        if n == 'Organism':
            p = r % (len(orgs))
            new_name = orgs[p]
        return new_name


    def col_detect(self, col_coords, col_name):
        antagonist = (Map.Grid[col_coords[0]][col_coords[1]])[1]
        if self.Name == "Hero" and col_name == "ROCK":
            self.take_damage(antagonist)
            print("Hero struck by " +  str(antagonist.Name) + "! | HP: " + str(self.HP) + " | Age: " + str(self.Age) + " | Energy: " + str(self.Energy))
        else:
            if self.Type == "Organism" and antagonist.Type == "Organism":
                print("Orgs Collide: " + str(antagonist.Energy) + " | " + str(self.Energy))
                if ((antagonist.Energy > 30 and self.Energy > 30) and ((self.Mated is False) and (antagonist.Mated is False))):
                    x = int(self.Energy/30)
                    self.reproduce(antagonist,col_coords)
                    self.Mated = True
                    antagonist.Mated = True
                elif self.HP < antagonist.HP and antagonist.Aggro > 0:
                    self.take_damage(antagonist)
                    print (self.Name + " struck by " + antagonist.Name + "! New Health: " + str(self.HP))
            elif antagonist.Type == "TREE":
                (Map.Grid[col_coords[0]][col_coords[1]]).remove(antagonist)
                self.HP += 5
                self.Energy += 20
                print(self.Name+ ' consumed ' + col_name + ' at ' + str(col_coords))
    def detect_env(self):
        x = self.Column
        y = self.Row
        neighbors = []
        if x - 1 > 0:
            if y - 1 > 0 and len(Map.Grid[x-1][y-1])>1:
                neighbors.append((Map.Grid[x-1][y-1])[1])
            if y + 1 < MapSize and len(Map.Grid[x-1][y+1])>1:
                neighbors.append((Map.Grid[x-1][y+1])[1])
        if x + 1 < MapSize:
            if y - 1 > 0 and len(Map.Grid[x+1][y-1])>1:
                neighbors.append((Map.Grid[x+1][y-1])[1])
            if y + 1 < MapSize and len(Map.Grid[x+1][y+1])>1:
                neighbors.append((Map.Grid[x+1][y+1])[1])
        for n in neighbors:
            if n.Type == 'Organism':
                if n.Aggro > 0:
                    print(self.Name + " | Aggressor detected!" + n.Name)
                if n.Name == self.Name and n.Mated is False:
                    print("Potential Mate?")
            if n.Type == 'PLANT':
                print(self.Name + ' senses a plant, ' + n.Type)
    def reproduce(self,antagonist,coords):
        parents = []
        parents.append([self.Type,antagonist.Type])
        parents.append([self.Name,antagonist.Name])
        child = []
        for trait in parents:
            r = random.randint(0,1)
            if r == 1:
                child.append(trait[1])
            else:
                child.append(trait[0])
        x = coords[0]
        y = coords[1]
        a_Mated = False
        i = -1
        for i in range(-1,2):
            for e in range (-1,1):
                Col = (x+i)%MapSize
                Row = (y+e)%MapSize
                target = Map.Grid[Col][Row]
                if len(target)<2 and self.Mated is False:
                    print(Col,Row)
                    baby = Character(str(child[0]),50,Col,Row)
                    print(baby.Color)
                    baby.s_color(255,255,255)
                    Map.Orgs.append(baby)
                    print("\tBaby " + child[1] + " born at " + str(x+i) + ',' + str(y+e))
                    self.Mated = True
                    antagonist.Mated = True
                    Map.update()
        return

    def take_damage(self,antagonist):
        h = self.HP
        a_h = antagonist.HP
        a_e = antagonist.Energy
        dmg = int(.1 * a_e)
        self.HP = h-dmg
        if self.HP < 0:
            self.die()

    def die(self):
        self.set_color(0,0,0)
        self.Age = -1
        self.Energy = 0
        print (self.Name + " Died!")

    def Move(self, Direction):
        col_test = self.CollisionCheck(Direction)
        if col_test[0]:
            print('Collision: %s on %s!' % (col_test[2], col_test[1]))
            return
        if Direction == "UP":
            if self.Row > 0:                #If within boundaries of grid
                self.Row -= 1
            #Go ahead and move
        elif Direction == "LEFT":
            if self.Column > 0:
                self.Column -= 1

        elif Direction == "RIGHT":
            if self.Column < MapSize-1:
                self.Column += 1

        elif Direction == "DOWN":
            if self.Row < MapSize-1:
                self.Row += 1

        self.Energy -= 1
        self.Age += 1
        if self.Age == 5:
            self.set_color()
        Map.update()

    def CollisionCheck(self, Direction):
        collision = False
        c_name = ''
        c_coords = []
        if Direction == "UP":
            if (self.Row-1)>0:
                if len(Map.Grid[self.Column][(self.Row)-1]) > 1:
                    collision = True
                    c_name = (Map.Grid[self.Column][(self.Row)-1])[1].Name
                    c_coords = [self.Column,(self.Row)-1]
        elif Direction == "LEFT":
            if (self.Column-1)>0:
                if len(Map.Grid[self.Column-1][(self.Row)]) > 1:
                    collision = True
                    c_name = (Map.Grid[self.Column-1][(self.Row)])[1].Name
                    c_coords = [(self.Column)-1,self.Row]
        elif Direction == "RIGHT":
            if (self.Column+1)<MapSize:
                if len(Map.Grid[self.Column+1][(self.Row)]) > 1:
                    collision = True
                    c_name = (Map.Grid[self.Column+1][(self.Row)])[1].Name
                    c_coords = [(self.Column)+1,self.Row]
        elif Direction == "DOWN":
            if (self.Row+1<MapSize):
                if len(Map.Grid[self.Column][(self.Row)+1]) > 1:
                    collision = True
                    c_name = (Map.Grid[self.Column][(self.Row)+1])[1].Name
                    c_coords = [self.Column,(self.Row)+1]
        if collision:
            self.col_detect(c_coords, c_name)
        return [collision, c_name, c_coords]

    def get_location(self):
        return self.Column, self.Row
        #return self.Column, self.Row
    def set_color(self):
        e = self.Energy
        t = self.Type
        transparency = int((e/100)*255)
        new_color = self.Color
        pos = random.randint(0,2)
        new_color[pos] = (new_color[pos] + 10) % 255
        #new_color[3] = transparency
        self.Color = new_color
        return tuple(self.Color)

    def get_color(self):
        return tuple(self.Color)

    def print_information(self):
        print("Name: " + str(self.Name) + "| Type: " + str(self.Type))
        print("Coordinates: " + str(self.Column) + ", " + str(self.Row))

class Map(object):              #The main class; where the action happens
    global MapSize

    Grid = []
    Orgs = []
    Plants = []

    def get_random_type():
        obstacles = ['BARE', 'GRASS']
        r = random.randint(0,(len(obstacles)-1))
        return obstacles[r]

    for Row in range(MapSize):     # Creating grid
        Grid.append([])
        for Column in range(MapSize):
            Grid[Row].append([])

    for Row in range(MapSize):     #Filling grid with grass
        for Column in range(MapSize):
            TempTile = MapTile("GRASS", Column, Row)
            Grid[Column][Row].append(TempTile)

    for Row in range(MapSize):     #Putting some rocks near the top
        for Column in range(MapSize):
            TempTile = MapTile("ROCK", Column, Row)
            if Row == 4:
                Grid[Column][Row].append(TempTile)

    stuff = ['TREE','ROCK','PLANT']
    for i in range(40):          #Placing Random trees
        RandomRow = random.randint(0, MapSize - 1)
        RandomColumn = random.randint(0, MapSize - 1)
        RandomThing = stuff[(random.randint(0,len(stuff)-1))]
        TempTile = MapTile(RandomThing, RandomColumn, RandomRow)
        g = Grid[RandomColumn][RandomRow]
        if len(g) < 2:
            g.append(TempTile)
            if RandomThing == 'PLANT':
                Plants.append(TempTile)

    for i in range(20):
        seek = True
        while (seek):
            RandomRow = random.randint(0, MapSize -1)
            RandomColumn = random.randint(0, MapSize - 1)
            TempTile = Character("Organism", 100, RandomColumn, RandomRow)
            g = Grid[RandomColumn][RandomRow]
            if len(g) < 2:
                g.append(TempTile)
                Orgs.append(TempTile)
                seek = False

    RandomRow = random.randint(0, MapSize - 1)      #Dropping the hero in
    RandomColumn = random.randint(0, MapSize - 1)
    Hero = Character("Hero", 100, RandomColumn, RandomRow)

    def update(self):        #Very important function
                             #This function goes through the entire grid
                             #And checks to see if any object's internal coordinates
                             #Disagree with its current position in the grid
                             #If they do, it removes the objects and places it 
                             #on the grid according to its internal coordinates 

        for Column in range(MapSize):
            for Row in range(MapSize):
                for i in range(len(Map.Grid[Column][Row])):
                    if (Map.Grid[Column][Row])[i].Column != Column:
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
                    elif Map.Grid[Column][Row][i].Name == "Hero":
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
                    elif Map.Grid[Column][Row][i].Type == "Organism":
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
                    elif Map.Grid[Column][Row][i].Type == "PLANT" and Map.Grid[Column][Row][i].Status == "DEAD":
                        (Map.Grid[Column][Row]).remove(Map.Grid[Column][Row][i])
        Map.Grid[int(Map.Hero.Column)][int(Map.Hero.Row)].append(Map.Hero)
        for o in Map.Orgs:
            Map.Grid[int(o.Column)][int(o.Row)].append(o)

Map = Map()

toolbar = tb.Toolbar(600, 80)

while not Done:
    #Main pygame loop
    toolbar.update()
    toolbar.draw(Screen)

    for event in pygame.event.get():         #catching events
        if event.type == pygame.QUIT:
            Done = True


        elif event.type == pygame.MOUSEBUTTONDOWN:
            Pos = pygame.mouse.get_pos()
            if Pos[0] < 1000:
                if Pos[1] < 1000:
                    Column = Pos[0] // (TileWidth + TileMargin)  #Translating the position of the mouse into rows and columns
                    Row = Pos[1] // (TileHeight + TileMargin)

                    if (Map.Grid[Column][Row]):
                        print(str(Row) + ", " + str(Column) + "\n")
                        for i in range(len(Map.Grid[Column][Row])):
                            cell = Map.Grid[Column][Row][i]
                            print('Name: ' + str(cell.Name) + '|' + str(cell.Type))
                            if (cell.Type == 'Tile'):
                                r = cell.report_nutrients()
                                print(str(r[0]))
                                print('HP: ' + str(cell.HP) + ' | E: ' + str(cell.Energy) + ' | Collected: ' + str(len(cell.collection)))
                                for i in range(1,len(r)-1):
                                    print(str(r[i][0]) + ' count: ' + str(r[i][1]) + 'freq: ' + str(r[i][2]))
                            elif cell.Type == "Organism" or cell.Name == "Hero":
                                print('Age: ' + str(cell.Age) + '| Energy: ' + str(cell.Energy) + 'HP: ' + str(cell.HP))#print stuff that inhabits that square

        elif event.type == pygame.KEYDOWN:
            Map.Hero.Move(KeyLookup[event.key])
            for p in Map.Plants:
                p.uptake()
            ranDir = ''
            for o in Map.Orgs:
                o.detect_env()
                dice = random.randint(1,4)
                if dice == 1:
                    ranDir = "LEFT"
                elif dice == 2:
                    ranDir = "RIGHT"
                elif dice == 3:
                    ranDir = "UP"
                else:
                    ranDir = "DOWN"
                o.Move(ranDir)
 #           Map.Org.Move(KeyLookup[dice])
        #elif event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_LEFT:
             #   Map.Hero.Move("LEFT")
           # if event.key == pygame.K_RIGHT:
           #     Map.Hero.Move("RIGHT")
           # if event.key == pygame.K_UP:
           #    Map.Hero.Move("UP")
            #if event.key == pygame.K_DOWN:
             #   Map.Hero.Move("DOWN")

    Screen.fill(BLACK)

    for Row in range(MapSize):           # Drawing grid
        for Column in range(MapSize):
            for i in range(0, len(Map.Grid[Column][Row])):
                Color = WHITE
                g = Map.Grid[Column][Row]
                if (g[i]):
                    Color = g[i].Color
                if g[i].Name == "Hero":
                    Color = GREEN
                if Map.Grid[Column][Row][i].Name == "Organism":
                    Color = g[i].Color

            pygame.draw.rect(Screen, Color, [(TileMargin + TileWidth) * Column + TileMargin,
                                             (TileMargin + TileHeight) * Row + TileMargin,
                                             TileWidth,
                                             TileHeight])

    clock.tick(60)      #Limit to 60 fps or something

    pygame.display.flip()     #Honestly not sure what this does, but it breaks if I remove it
    Map.update()

pygame.quit()
