import os
import numpy as np
import cv2
from time import sleep

# import scripts
import proba
from supermarket import Customer


TILE_SIZE = 32

MARKET = """
##################
##..............##
#p..Bt..Is..dA..b#
#l..Bg..IL..Te..a#
#p..Kg..zP..Tm..f#
#h..KS..zH..kc..u#
#h..lS..iY..sO..o#
##...............#
##..C#..C#..C#...#
##..##..##..##...#
##...............#
##############GG##
""".strip()


class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """

        self.tiles = tiles
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in layout.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)
        self.image = np.zeros(
            (self.nrows*TILE_SIZE, self.ncols*TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def extract_tile(self, row, col):
        """extract a tile array from the tiles image"""
        y = row*TILE_SIZE
        x = col*TILE_SIZE
        return self.tiles[y:y+TILE_SIZE, x:x+TILE_SIZE]

    def get_tile(self, char):
        """returns the array for a given tile character"""
        #furniture
        if char == "#":
            return self.extract_tile(0, 0)
        elif char == "G":
            return self.extract_tile(7, 3)
        elif char == "C":
            return self.extract_tile(2, 8)
        
        #fruit
        elif char == "b":
            return self.extract_tile(0, 4) #banana
        elif char == "f":
            return self.extract_tile(1, 5) #strawberry
        elif char == "a":
            return self.extract_tile(3, 4) #watermelon
        elif char == "u":
            return self.extract_tile(4, 4) #grapes
        elif char == "A":
            return self.extract_tile(5, 4) #ananas
        elif char == "o":
            return self.extract_tile(1, 4) #orange
        elif char == "e":
            return self.extract_tile(1, 11) #eggplant
        elif char == "c":
            return self.extract_tile(2, 11) #carrot
        elif char == "m":
            return self.extract_tile(6, 11) #mushroom
        elif char == "O":
            return self.extract_tile(0, 11) #onion
        
        #drinks
        elif char == "T":
            return self.extract_tile(5,6) #cake
        elif char == "d":
            return self.extract_tile(6,6) #beignet
        elif char == "k":
            return self.extract_tile(5,8) #candy
        elif char == "H":  
            return self.extract_tile(7,7) #stick5
        elif char == "P":
            return self.extract_tile(4,7) #stick1
        elif char == "L":
            return self.extract_tile(5,7) #stick2
        elif char == "Y":
            return self.extract_tile(6,7) #stick3
        elif char == "s":
            return self.extract_tile(0,8) #stick4

        #dairy
        elif char == "I":                 
            return self.extract_tile(7,5) #Icecream
        elif char == "i":                 
            return self.extract_tile(1,6) #icecram2
        elif char == "z":                 
            return self.extract_tile(2,6) #icecram3 
        elif char == "g":                 
            return self.extract_tile(7,11) #egg
        elif char == "t":                 
            return self.extract_tile(4,13) #chicken
        elif char == "S":                 
            return self.extract_tile(2,14) #sandwich

        #drinks
        elif char == "h":  
            return self.extract_tile(4,9) #potion 1
        elif char == "p":
            return self.extract_tile(5,9) #potion2
        elif char == "l":
            return self.extract_tile(6,9) #potion3 
        elif char == "B":                 
            return self.extract_tile(6,13) #beer
        elif char == "K":                 
            return self.extract_tile(3,13) #cocktail
        


        #random
        elif char == "X":
            return self.extract_tile(3, 10)
        elif char == "x":
            return self.extract_tile(4,10)


##################
##..............##
##..#t..Ip..dA..b#
##..#g..Il..Te..a#
##..#g..zp..Tm..f#
##..#S..zh..kc..u#
##..#S..ih..sO..o#
##...............#
##..C#..C#..C#...#
##..##..##..##...#
##...............#
##############GG##




        else:
            return self.extract_tile(1, 2)

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = row*TILE_SIZE
                x = col*TILE_SIZE
                self.image[y:y+TILE_SIZE, x:x+TILE_SIZE] = bm

    def draw(self, frame):
        """
        draws the image into a frame
        """
        frame[0:self.image.shape[0], 0:self.image.shape[1]] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


class GhostCustomer(Customer):
    """
    a single ghost-customer that moves through the dungeon supermarket
    """

    def __init__(self, supermarket, avatar, row, col):
        """
        supermarket: A SuperMarketMap object
        avatar : a numpy array containing a 32x32 tile image
        row: the starting row
        col: the starting column
        """
        super().__init__('a pink gost')
        
        self.supermarket = supermarket
        self.avatar = self.supermarket.extract_tile(7,2)
        self.row = row
        self.col = col

    def __repr__(self):
        return f"{self.name} is in {self.state}."

    def draw(self, frame):
      x = self.col * TILE_SIZE
      y = self.row * TILE_SIZE
      frame[x:x+self.avatar.shape[0], y:y+self.avatar.shape[1]] = self.avatar

    def move(self, direction):
        new_row = self.row
        new_col = self.col

        if direction == 'up':
            new_row = new_row - 1
        elif direction == 'down':
            new_row = new_row + 1
        elif direction == 'left':
            new_col == new_col - 1
        elif direction == 'right':
            new_col == new_col + 1

        if self.supermarket.contents[new_row][new_col] == '.':
            self.col = new_col
            self.row = new_row    

    




if __name__ == "__main__":

    background = np.zeros((512, 704, 3), np.uint8)
    tiles = cv2.imread("../data/images/tiles.png")

    market = SupermarketMap(MARKET, tiles)
    ghost = GhostCustomer(market, market.extract_tile(7,2),21,14)

    while True:
        frame = background.copy()
        market.draw(frame)
        ghost.draw(frame)
        


        # https://www.ascii-code.com/
        key = cv2.waitKey(1)

        if key == 113: # 'q' key
            break
    
        cv2.imshow("dungeon-like supermarket", frame)
        #ghost.move('up')


    cv2.destroyAllWindows()

    path = "output"
    if not os.path.exists(path):
        os.makedirs(path)
    market.write_image("output/dungeon_supermarket.png")
