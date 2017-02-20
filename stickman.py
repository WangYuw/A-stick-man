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
        self.win_text = self.canvas.create_text(150, 45, text='You Win!', state='hidden')

    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            else:
                time.sleep(1)
                self.canvas.itemconfig(self.win_text, state='normal')
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
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2

    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2

    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0

    # juge way of move and change image
    def animate(self):
        # if the stick man move or jump
        if self.x !=0 and self.y == 0:
            # if draw next image
            if time.time() - self.last_time > 0.1:
                # recount time
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.image_left[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.image_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.image_right[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.image_right[self.current_image])

    def coords(self):
        xy = list(self.game.canvas.coords(self.image))
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates

    def move(self):
        self.animate()
        # is jumping
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4
            # is falling
        if self.y > 0:
            self.jump_count -= 1
        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        # fall down the bottom of the canvas
        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0
            bottom = False
        # jump to the top of canvas
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False
        # collid left or right
        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right =  False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False
        # collid to other sprites
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            # not top and is jumping and stick man collid sprite by top
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y
                top = False
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False
            if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height and collided_bottom(1, co, sprite_co):
                falling = False
            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0
                left = False
                if sprite.endgame:
                    self.win(sprite)
            if right and self.x > 0 and collided_right(co, sprite_co):
                self.x = 0
                right = False
                if sprite.endgame:
                    self.win(sprite)
        if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
            self.y = 4
        self.game.canvas.move(self.image, self.x, self.y)

    def win(self, sprite):
        self.game.running = False
        sprite.opendoor()
        time.sleep(1)
        self.game.canvas.itemconfig(self.game, state='hidden')
        sprite.closedoor()

class DoorSprite(Sprite):
    
    def __init__(self, game, x, y, width, height):
        Sprite.__init__(self, game)
        self.close_door = PhotoImage(file="roles/door1.gif")
        self.open_door = PhotoImage(file="roles/door2.gif")
        self.image = game.canvas.create_image(x, y, image=self.close_door, anchor='nw')
        self.coordinates = Coords(x, y, x+width/2, y+height)
        self.endgame = True

    def opendoor(self):
        self.game.canvas.itemconfig(self.image, image=self.open_door)
        self.game.tk.update_idletasks()

    def closedoor(self):
        self.game.canvas.itemconfig(self.image, image=self.close_door)
        self.game.tk.update_idletasks()     
        

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

door = DoorSprite(g, 45, 30, 40, 35)
g.sprites.append(door)

s =StickManSprite(g)
g.sprites.append(s)

g.mainloop()