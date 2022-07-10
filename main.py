from ast import And
from nis import match
from statistics import mode
from time import sleep
from traceback import print_tb
from typing import overload
from xmlrpc.server import SimpleXMLRPCDispatcher
import pygame
import os
from enum import Enum  
import random
# Consts
WIDTH, HEIGHT = 900, 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
BACKGROUND = (186, 255, 255)
FPS = 5
CLOCK = pygame.time.Clock()

SNAKE_HEAD_IMG = pygame.image.load(os.path.join('pygame/Assets', 'Snake_head.png'))
SNAKE_TAIL_IMG = pygame.image.load(os.path.join('pygame/Assets', 'Snake_tail.png'))
SNAKE_HEAD = SNAKE_HEAD_IMG
STAR_IMG = pygame.image.load(os.path.join('pygame/Assets', 'Star.png'))

SPEED = 15

pygame.font.init() 
normal_size = pygame.font.SysFont('Comic Sans MS', 30)
huge_size = pygame.font.SysFont('Comic Sans MS', 50)


# Global functions
def blit(img, x, y): # Use it later!
    WINDOW.blit(img, (x, y))
    pygame.display.update()

def star_position(constant):
    return random.randint(7, ((constant/15)-7))*15

# Classes for snake construction
class Snake_head:
    def __init__(self):
        self.Rectangle = pygame.Rect(WIDTH/2, HEIGHT/2, SNAKE_HEAD_IMG.get_width(), SNAKE_HEAD_IMG.get_height()) # Head hitbox
        self.Vector = [0,-1] # Going up
        WINDOW.blit(SNAKE_HEAD_IMG, (self.Rectangle.x, self.Rectangle.y))
        pygame.display.update()
    
    def move(self):
        self.Rectangle.x += self.Vector[0] * SPEED
        self.Rectangle.y += self.Vector[1] * SPEED
        WINDOW.blit(SNAKE_HEAD, (self.Rectangle.x, self.Rectangle.y))
        pygame.display.update()
    
    def rotate(self, side):
        global SNAKE_HEAD_IMG 
        global SNAKE_HEAD
        SNAKE_HEAD = pygame.transform.rotate(SNAKE_HEAD_IMG, side)
        if side == 0 :
            self.Vector = [0,-1] 
        if side == 90 :
            self.Vector = [-1,0] 
        if side == 180 :
            self.Vector = [0,1] 
        if side == 270 :
            self.Vector = [1,0] 

        
class Snake_tail:
    def __init__(self, x = (WIDTH/2) , y = (WIDTH/2)+SPEED, base_Vector = [0,-1]):
        self.Rectangle = pygame.Rect(x, y, SNAKE_HEAD_IMG.get_width(), SNAKE_HEAD_IMG.get_height())
        self.Vector = base_Vector # Going up        
        WINDOW.blit(SNAKE_TAIL_IMG, (self.Rectangle.x, self.Rectangle.y))
        pygame.display.update()
    
    def move(self, x, y):
        self.Rectangle.x = x
        self.Rectangle.y = y
        WINDOW.blit(SNAKE_TAIL_IMG, (self.Rectangle.x, self.Rectangle.y))
        pygame.display.update()


class Snake(Snake_head):
    def __init__(self):
        super().__init__()
        self.list_of_tails = [Snake_tail()]
        self.places = [[(WIDTH/2) + SPEED, (HEIGHT/2) + SPEED]]   
        self.score = 0
    
    def append(self):
        x = (self.list_of_tails[-1].Rectangle.x)
        y = (self.list_of_tails[-1].Rectangle.y)
        Vector_x = (self.list_of_tails[-1].Vector[0])
        Vector_y = (self.list_of_tails[-1].Vector[1])

        self.list_of_tails.append(Snake_tail(x= x - (SPEED* Vector_x), y = y - (SPEED* Vector_y)))
        self.places.append([x, y])
    
    def move(self):       
        # Vectors
        self.list_of_tails[0].Vector = self.Vector ###

        overwrite = []
        i = 0
        while i < len(self.list_of_tails): # PYTHON YOU SUCCC
            overwrite.append(self.list_of_tails[i].Vector)
            i = i+1
        
        i=0
        while i < len(self.list_of_tails)-1:
            self.list_of_tails[i+1].Vector = overwrite[i]
            i=i+1

        # Places
        self.places[0] = [self.Rectangle.x, self.Rectangle.y]
        
        super().move()
        
        overwrite = []
        i = 0
        while i < len(self.places): # PYTHON YOU SUCCC
            overwrite.append(self.places[i])
            i = i+1
        
        i=0
 
        while i < len(self.places)-1:
            self.places[i+1] = overwrite[i]
            i=i+1
        
        i = 1
        while i < len(self.list_of_tails):
            self.list_of_tails[i].move(self.places[i][0], self.places[i][1])
            i = i +1

    def rotate(self, side):
        super().rotate(side)    

    def lose_condition(self):
        for i in self.list_of_tails:
            if (i.Rectangle.x == self.Rectangle.x) and (i.Rectangle.y == self.Rectangle.y):
                return True
        return False
    
    def collect_star(self, Star):
        if (Star.Rectangle.x == self.Rectangle.x) and (Star.Rectangle.y == self.Rectangle.y):
            Star.change_position()
            self.append()
            self.score +=1
            return True

class Star:
    def __init__(self, x, y):
        self.Rectangle = pygame.Rect(x, y, STAR_IMG.get_width(), STAR_IMG.get_height()) # Creating rectangle
        blit(STAR_IMG, x, y)

    def draw(self):
        blit(STAR_IMG, self.Rectangle.x, self.Rectangle.y)
    
    def change_position(self):
        self.Rectangle.x = star_position(WIDTH)
        self.Rectangle.y = star_position(HEIGHT)
    
# Set defult 
WINDOW.fill(BACKGROUND)
pygame.display.update()


def main():
    run = True
    
    label = huge_size.render("Welcome to Snake in Python!", 12, (0,0,0))
    blit(label, (WIDTH/2)-230, (HEIGHT/2)-100)

    label = normal_size.render("Press any key to start", 12, (0,0,0))
    blit(label, (WIDTH/2)-100, (HEIGHT/2)-60)

    sleep(3)
    while not pygame.key.get_pressed:
        print(pygame.key.get_pressed)
        sleep(1)
    
    Hero = Snake()
    Hero.append()
    
    star_x = star_position(WIDTH) 
    star_y = star_position(HEIGHT)

    print(star_x, star_y)   
    new_star = Star(star_x, star_y)

    while run: # Main loop
        keys_pressed = pygame.key.get_pressed()
        
        WINDOW.fill(BACKGROUND)
        CLOCK.tick(FPS)

        # Score sign
        label = normal_size.render("Score: {0}".format(Hero.score), 12, (0,0,0))
        WINDOW.blit(label, (0, 0))
        new_star.draw()
        
        if keys_pressed[pygame.K_LEFT]:
            Hero.rotate(90)
        if keys_pressed[pygame.K_RIGHT]:
            Hero.rotate(270)
        if keys_pressed[pygame.K_DOWN]:
            Hero.rotate(180)
        if keys_pressed[pygame.K_UP]:
            Hero.rotate(0)  
        if keys_pressed[pygame.K_a]:
            Hero.append()
        Hero.collect_star(new_star)
        Hero.move() 
        
        for event in pygame.event.get(): # Getting all the events
            if event.type == pygame.QUIT:
                run = False     
        
        if Hero.lose_condition() == True:
            run = False

    
    WINDOW.fill(BACKGROUND)
    # render text
    label = normal_size.render("YOU FAILED!", 1, (0,0,0))
    WINDOW.blit(label, ((WIDTH/2)-80, HEIGHT/2))
    pygame.display.update()    
    sleep(10)
    pygame.quit()            

if __name__ == "__main__": # Checks out file name
    main()