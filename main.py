from nis import match
from statistics import mode
from time import sleep
from traceback import print_tb
from typing import overload
import pygame
import os
from enum import Enum  
# Consts
WIDTH, HEIGHT = 900, 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")
BACKGROUND = (186, 255, 255)
FPS = 3
CLOCK = pygame.time.Clock()
SNAKE_HEAD_IMG = pygame.image.load(os.path.join('pygame/Assets', 'Snake_head.png'))
SNAKE_TAIL_IMG = pygame.image.load(os.path.join('pygame/Assets', 'Snake_tail.png'))
SNAKE_HEAD = SNAKE_HEAD_IMG



# Classes for snake construction
class Snake_head:
    def __init__(self):
        self.Rectangle = pygame.Rect(WIDTH/2, HEIGHT/2, SNAKE_HEAD_IMG.get_width(), SNAKE_HEAD_IMG.get_height()) # Head hitbox
        self.Vector = [0,-1] # Going up
        WINDOW.blit(SNAKE_HEAD_IMG, (self.Rectangle.x, self.Rectangle.y))
        pygame.display.update()
    
    def move(self):
        self.Rectangle.x += self.Vector[0] * 15
        self.Rectangle.y += self.Vector[1] * 15
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
    def __init__(self, x = (WIDTH/2) , y = (WIDTH/2)+15, base_Vector = [0,-1]):
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
        self.places = [[(WIDTH/2) + 15, (HEIGHT/2) + 15]]    
    def append(self):
        x = (self.list_of_tails[-1].Rectangle.x)
        y = (self.list_of_tails[-1].Rectangle.y)
        Vector_x = (self.list_of_tails[-1].Vector[0])
        Vector_y = (self.list_of_tails[-1].Vector[1])

        self.list_of_tails.append(Snake_tail(x= x - (15* Vector_x), y = y - (15* Vector_y)))
        self.places.append([x, y])
    
    def move(self):       
        self.list_of_tails[0].Vector = self.Vector ###
        self.places[0] = [self.Rectangle.x, self.Rectangle.y]
        #First render then move
        
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
            print(self.list_of_tails[i].Rectangle)
            i = i +1
        
        self.append()

    def rotate(self, side):
        super().rotate(side)    

# Set defult 
WINDOW.fill(BACKGROUND)
pygame.display.update()


def main():
    run = True
    Hero = Snake()
    while run: # Main loop
        WINDOW.fill(BACKGROUND)
        CLOCK.tick(FPS)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            Hero.rotate(90)
        if keys_pressed[pygame.K_RIGHT]:
            Hero.rotate(270)
        if keys_pressed[pygame.K_DOWN]:
            Hero.rotate(180)
        if keys_pressed[pygame.K_UP]:
            Hero.rotate(0)  

        Hero.move() 
        
        for event in pygame.event.get(): # Getting all the events
            if event.type == pygame.QUIT:
                run = False     

    pygame.quit()            

if __name__ == "__main__": # Checks out file name
    main()