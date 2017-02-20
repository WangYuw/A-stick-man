from tkinter import *
import random
import time

#create canvas and title
class Game:
    
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Mr. Stick Man Races for the Exit")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=500, height=500, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500
        self.bg = PhotoImage(file="roles/background.gif")
        self.bg2 = PhotoImage(file="roles/background2.gif")
        w = self.bg.width()
        h = self.bg.height()
        draw = 0
        for x in range(0,5):
            for y in range(0,5):
                if draw == 1:
                    self.canvas.create_image(x*w, y*h, image=self.bg, anchor="nw")
                    draw = 0
                else:
                    self.canvas.create_image(x*w, y*h, image=self.bg2, anchor="nw")
                    draw = 1
        self.sprites = []
        self.running = True

    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

class Coords:

    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Sprite:
    
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates

class PlatformSprite(Sprite):
    
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x+width, y+height)

class StickManSprite(Sprite):
    
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.image_left = [PhotoImage(file="roles/stickman_L1.gif"),
                        PhotoImage(file="roles/stickman_L2.gif"),
                        PhotoImage(file="roles/stickman_L3.gif")]
        self.image_right = [PhotoImage(file="roles/stickman_R1.gif"),
                        PhotoImage(file="roles/stickman_R2.gif"),
                        PhotoImage(file="roles/stickman_R3.gif")]
        self.image = game.canvas.create_image(200, 470, image=self.image_left[0], anchor='nw')
        # increase x,y for every step
        self.x = -2
        self.y = 0
        # index of current image
        self.current_image = 0
        # index of next image
        self.current_image_add = 1
        self.jump_count = 0
        # the time that we move thr stick man the last time
        self.last_time = time.time()
        self.coordinates = Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<KeyPress-Up>', self.jump)
        game.canvas.bind_all('<space>', self.jump)
        
        

#if two sprites have the same part on x
def within_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
        or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
        or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
        or (co2.x2 > co1.x1 and co2.x2 < co1.x1):
        return True
    else: 
        return False

#if two sprites have the same part on y      
def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
        or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
        or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
        or (co2.y2 > co1.y1 and co2.y2 < co1.y1):
        return True
    else: 
        return False

def collided_left(co1, co2):
    if within_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            return True
    return False

def collided_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False

def collided_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False

def collided_bottom(y, co1, co2):
    if within_x(co1, co2):
        y_calc = co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False
        

        

g = Game()

platform1 = PlatformSprite(g, PhotoImage(file="roles/platform1.gif"), 0, 480, 100, 10)
platform2 = PlatformSprite(g, PhotoImage(file="roles/platform1.gif"), 150, 440, 100, 10)
platform3 = PlatformSprite(g, PhotoImage(file="roles/platform1.gif"), 300, 400, 100, 10)
platform4 = PlatformSprite(g, PhotoImage(file="roles/platform1.gif"), 300, 160, 100, 10)
platform5 = PlatformSprite(g, PhotoImage(file="roles/platform2.gif"), 175, 350, 66, 10)
platform6 = PlatformSprite(g, PhotoImage(file="roles/platform2.gif"), 50, 300, 66, 10)
platform7 = PlatformSprite(g, PhotoImage(file="roles/platform2.gif"), 170, 120, 66, 10)
platform8 = PlatformSprite(g, PhotoImage(file="roles/platform2.gif"), 45, 60, 66, 10)
platform9 = PlatformSprite(g, PhotoImage(file="roles/platform2.gif"), 380, 280, 66, 10)
platform10 = PlatformSprite(g, PhotoImage(file="roles/platform3.gif"), 230, 200, 32, 10)
platform11 = PlatformSprite(g, PhotoImage(file="roles/platform3.gif"), 170, 250, 32, 10)
g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)
g.sprites.append(platform11)

g.mainloop()