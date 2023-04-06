"""Main file that runs the game itself"""

import sys
import pygame

# intialize pygame
pygame.init()

### Setting the constants

# Setting Window, virtual dims and the scale
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
VIRTUAL_WIDTH = 512
VIRTUAL_HEIGHT = 288
scale_x = WINDOW_WIDTH/VIRTUAL_WIDTH
scale_y = WINDOW_HEIGHT/VIRTUAL_HEIGHT

# FPS
FPS = 60

# Define our fonts
small_font = pygame.font.Font('fonts/font.ttf', 8)
medium_font = pygame.font.Font('fonts/flappy.ttf', 14)
flappy_font = pygame.font.Font('fonts/flappy.ttf', 28)
huge_font = pygame.font.Font('fonts/flappy.ttf', 56)

# load the background and ground
background = pygame.transform.scale(pygame.image.load('imgs/background.png'), (1157*scale_x, 288*scale_y))
ground = pygame.transform.scale(pygame.image.load('imgs/ground.png'), (2200*scale_x, 32*scale_y))

# Define our game variables
BACKGROUND_SCROLL_SPEED = 4
GROUND_SCROLL_SPEED = 8

def run(screen, clock):
    """ This is where the endless while loop with the will run.
        This function will handle any state changes (i.e. main menu, play, etc)"""

    # make gamestate var and running var
    gamestate = 'menu'
    running = True

    # scrolling vars
    background_scroll = 0
    ground_scroll = 0
    scrolling = True

    # Infinite while loop so long as running
    while running:

        # set the clock's fps
        clock.tick(FPS)

        # Constantly update the display
        pygame.display.update()

        # draw the background and the ground
        # for i in range(2):
        screen.blit(background, (background_scroll,0))
        screen.blit(ground, (ground_scroll, WINDOW_HEIGHT-(32*scale_y)))

        # logic for ground and background scrolling
        if scrolling:
            background_scroll = background_scroll - BACKGROUND_SCROLL_SPEED
            if abs(background_scroll) > (413*scale_x):
                background_scroll=0
            ground_scroll = ground_scroll - GROUND_SCROLL_SPEED
            if abs(ground_scroll) > (ground.get_width() - WINDOW_WIDTH):
                ground_scroll=0

        # TBR -> quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def main():
    """Function loads the pygame display and sets the clock"""

    # Set the display size
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Floppy Bird")

    # Create a clock
    clock = pygame.time.Clock()

    # Call the run function
    run(screen, clock)
    


# Call main function
if __name__ == '__main__':
    main()
    