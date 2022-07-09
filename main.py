import pygame

# Consts
WIDTH, HEIGHT = 900, 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")
BACKGROUND = (186, 255, 255)
FPS = 2
CLOCK = pygame.time.Clock()
SNAKE_HEAD_IMG = pygame.image.load("./pygame/Snake_head.png")
SNAKE_TAIL_IMG = pygame.image.load("./pygame/Snake_tail.png")

# Classes for snake construction
class Snake_head:
    def __init__(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        WINDOW.blit(SNAKE_HEAD_IMG, (self.x, self.y))
        pygame.display.update()
    def move(self):
        self.y -= 15
        WINDOW.blit(SNAKE_HEAD_IMG, (self.x, self.y))
        pygame.display.update()
class Snake_tail:
    def __init__(self, x = (WIDTH/2) , y = (WIDTH/2)+15):
        self.x = x
        self.y = y  
        WINDOW.blit(SNAKE_TAIL_IMG, (self.x, self.y))
        pygame.display.update()
    def move(self):
        self.y -= 15
        WINDOW.blit(SNAKE_TAIL_IMG, (self.x, self.y))
        pygame.display.update()

class Snake(Snake_head):
    def __init__(self):
        super().__init__()
        self.list_of_tails = [Snake_tail()]
    def move(self):
        super().move()
        for i in self.list_of_tails:
            i.move()

# Set defult 
WINDOW.fill(BACKGROUND)
pygame.display.update()


def main():
    run = True
    Hero = Snake()
    while run: # Main loop
        CLOCK.tick(FPS)
        Hero.move()
        for event in pygame.event.get(): # Getting all the events
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()            

if __name__ == "__main__": # Checks out file name
    main()