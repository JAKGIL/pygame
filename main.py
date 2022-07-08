import pygame

WIDTH, HEIGHT = 900, 900

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    run = True

    while run: # Main loop
        for event in pygame.event.get(): # Getting all the events
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()            

if __name__ == "__main__": # Checks out file name
    main()