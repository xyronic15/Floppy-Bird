"""Main file that runs the game itself"""

import sys
import pygame
import random
from bird import Bird
from pipe import Pipe

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
small_font = pygame.font.Font('fonts/font.ttf', 40)
medium_font = pygame.font.Font('fonts/flappy.ttf', 75)
flappy_font = pygame.font.Font('fonts/flappy.ttf', 100)
huge_font = pygame.font.Font('fonts/flappy.ttf', 120)

# Define colors
WHITE = (255, 255, 255)

# load the background and ground
background = pygame.transform.scale(pygame.image.load('imgs/background.png'), (1157*scale_x, 288*scale_y))
ground = pygame.transform.scale(pygame.image.load('imgs/ground.png'), (2200*scale_x, 32*scale_y))

# Define our game variables
BACKGROUND_SCROLL_SPEED = 4
GROUND_SCROLL_SPEED = 8

# TBC
def disp_score(screen, score):
    """function will continuously show the score when applicable"""
    value = small_font.render(f"Score: {score}", True, WHITE)
    screen.blit(value, [10, 10])


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

    # create the sprite groups for birds and pipes
    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()
    last_pipe = pygame.time.get_ticks()

    # Add the bird into the sprite group
    bird_group.add(Bird((WINDOW_WIDTH/3) - (8*scale_x),(WINDOW_HEIGHT/2) - (8*scale_y), scales=[scale_x,scale_y]))

    # set score var
    score = 0
    passed_pipe = False

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
        
        # draw the bird and pipes
        bird_group.draw(screen)
        pipe_group.draw(screen)
        
        # use if statements to handle gamestate
        # main menu state
        if gamestate == 'menu':
            # Show title and instructions
            title = flappy_font.render("Floppy Bird", True, WHITE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) - 150))
            screen.blit(title, title_rect)

            start = small_font.render("Press \"enter\" to play", True, WHITE)
            start_rect = start.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) - 70))
            screen.blit(start, start_rect)

            instr = small_font.render("Use the spacebar to jump", True, WHITE)
            instr_rect = instr.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) + 10))
            screen.blit(instr, instr_rect)

            p_msg = small_font.render("Press \"P\" to pause", True, WHITE)
            p_msg_rect = p_msg.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) + 85))
            screen.blit(p_msg, p_msg_rect)

            quit_msg = small_font.render("Press \"ESC\" to quit", True, WHITE)
            quit_msg_rect = quit_msg.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) + 150))
            screen.blit(quit_msg, quit_msg_rect)

            # check if the enter key is pressed and change state to play
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gamestate = 'play'
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        print('quit')
                if event.type == pygame.QUIT:
                    running = False
                    print('quit')
                
        # playing state
        elif gamestate == 'play':

            # check for any inputs and call jump if space is pressed
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        gamestate = 'paused'
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        print('quit')
                    if event.key == pygame.K_SPACE:
                        bird_group.sprites()[0].jump()
                if event.type == pygame.QUIT:
                    running = False
                    print('quit')

            # check the score
            if len(pipe_group) > 0:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and passed_pipe == False:
                    passed_pipe = True
                if passed_pipe == True:
                    if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                        score += 1
                        passed_pipe = False
            
            # set gamestate to gameover if collision or hit top or bottom
            if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird_group.sprites()[0].rect.top < 0 or bird_group.sprites()[0].rect.bottom > WINDOW_HEIGHT-(32*scale_y):
                gamestate='gameover'

            # generate new pipes
            now = pygame.time.get_ticks()
            if now - last_pipe > random.randint(1100,1700):
                btm_pipe = Pipe(-1, int(WINDOW_HEIGHT/2), scales=[scale_x, scale_y])
                top_pipe = Pipe(1, int(WINDOW_HEIGHT/2), scales=[scale_x, scale_y])
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = now
            
            # update the bird and the pipes
            bird_group.update()
            pipe_group.update()
            scrolling = True
            disp_score(screen, score)
        
        # pause state
        elif gamestate == 'paused':

            # check for any inputs and resume if p is pressed
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        gamestate = 'play'
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        print('quit')
                if event.type == pygame.QUIT:
                    running = False
                    print('quit')
            
            # Show paused and instruction
            paused = huge_font.render("PAUSED", True, WHITE)
            paused_rect = paused.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) - 90))
            screen.blit(paused, paused_rect)

            p_msg = small_font.render("Press \"P\" to continue", True, WHITE)
            p_msg_rect = p_msg.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) + 35))
            screen.blit(p_msg, p_msg_rect)
                
            # stop the background moving backgrounds
            scrolling = False

            disp_score(screen, score)
        
        # gameover state
        elif gamestate == 'gameover':

            # check for any inputs and restart if r is pressed
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        running = False
                        run(screen, clock)
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        print('quit')
                if event.type == pygame.QUIT:
                    running = False
                    print('quit')

            # stop the background moving backgrounds
            scrolling = False

            disp_score(screen, score)


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
    # quit pygame when done
    pygame.quit()
    