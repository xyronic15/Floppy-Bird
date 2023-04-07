"""Main file that runs the game itself"""

import sys
import pygame
from pygame import mixer
import random
from bird import Bird
from pipe import Pipe
from logger import *
from states import *

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
fonts = {"small_font": pygame.font.Font('fonts/font.ttf', 40),
        "medium_font": pygame.font.Font('fonts/flappy.ttf', 75),
        "flappy_font": pygame.font.Font('fonts/flappy.ttf', 100),
        "huge_font": pygame.font.Font('fonts/flappy.ttf', 120)}

# Define colors
WHITE = (255, 255, 255)

# load the background and ground
background = pygame.transform.scale(pygame.image.load('imgs/background.png'), (1157*scale_x, 288*scale_y))
ground = pygame.transform.scale(pygame.image.load('imgs/ground.png'), (2200*scale_x, 32*scale_y))

# load the medal images
gold = pygame.transform.scale(pygame.image.load('imgs/gold.png'), (26*scale_x, 30*scale_y))
silver = pygame.transform.scale(pygame.image.load('imgs/silver.png'), (26*scale_x, 30*scale_y))
bronze = pygame.transform.scale(pygame.image.load('imgs/bronze.png'), (26*scale_x, 30*scale_y))

# load sounds/music
mixer.init()
mixer.music.load('sounds/marios_way.mp3')
mixer.music.play(-1)
sounds = {"jump_fx": mixer.Sound("sounds/jump.wav"),
        "explosion_fx": mixer.Sound("sounds/explosion.wav"),
        "hurt_fx": mixer.Sound("sounds/hurt.wav"),
        "score_fx": mixer.Sound("sounds/score.wav"),
        "pause_fx": mixer.Sound("sounds/pause.wav")}

# Define our game variables
BACKGROUND_SCROLL_SPEED = 4
GROUND_SCROLL_SPEED = 8

def disp_score(screen, score):
    """function will continuously show the score when applicable"""
    value = fonts["small_font"].render(f"Score: {score}", True, WHITE)
    screen.blit(value, [10, 10])

def disp_results(screen, score):
    """Function will check the person's score and display the results with the corresponding medal"""

    # check score
    if score >=  20:
        medal = pygame.transform.scale(gold, (26*scale_x*4, 30*scale_y*4))
        medal_rect = medal.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) - 75))
        screen.blit(medal, medal_rect)
    elif score < 20 and score >= 10:
        medal = pygame.transform.scale(silver, (26*scale_x*4, 30*scale_y*4))
        medal_rect = medal.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) - 75))
        screen.blit(medal, medal_rect)
    elif score < 10:
        medal = pygame.transform.scale(bronze, (26*scale_x*4, 30*scale_y*4))
        medal_rect = medal.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) - 75))
        screen.blit(medal, medal_rect)
    
    # display the score
    value = fonts["medium_font"].render(f"You scored {score} points!", True, WHITE)
    value_rect = value.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/3) * 2 + 30))
    screen.blit(value, value_rect)    

def disp_high_scores(screen):
    """Function calls logger function and reads top three scores from scores.csv"""

    # read from csv
    data = read_top_three()

    # display the error msg if a string is given
    if isinstance(data, str):
        msg = fonts["medium_font"].render(data, True, WHITE)
        msg_rect = msg.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT/2)))
        screen.blit(msg, msg_rect)
    
    # display the scores with their corresponding medals if list is given
    else:
        for i in range(len(data)):
            msg = fonts["medium_font"].render(f"{i+1}    {data[i]['score']}", True, WHITE)
            msg_rect = msg.get_rect(center=((WINDOW_WIDTH/2) - 120, (WINDOW_HEIGHT/2) - 90 + (90*i)))
            screen.blit(msg, msg_rect)

            # show corresponding medal
            if data[i]['medal'] == 'gold':
                medal = gold
                medal_rect = medal.get_rect(center=((WINDOW_WIDTH/2) + 190, (WINDOW_HEIGHT/2) - 90 + (90*i)))
            elif data[i]['medal'] == 'silver':
                medal = silver
                medal_rect = medal.get_rect(center=((WINDOW_WIDTH/2) + 190, (WINDOW_HEIGHT/2) - 90 + (90*i)))
            else:
                medal = bronze
                medal_rect = medal.get_rect(center=((WINDOW_WIDTH/2) + 190, (WINDOW_HEIGHT/2) - 90 + (90*i)))
            screen.blit(medal, medal_rect)

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
    bird_group.add(Bird((WINDOW_WIDTH/4) - (8*scale_x),(WINDOW_HEIGHT/2) - (8*scale_y), scales=[scale_x,scale_y]))

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
            
            # run menu state function and get the return values from there
            gamestate, running = menu_state(screen, fonts, gamestate, running, [WINDOW_WIDTH, WINDOW_HEIGHT], WHITE)
                
        # playing state
        elif gamestate == 'play':

            # run play state function and get the return values from there
            gamestate, score, running, last_pipe, passed_pipe = play_state(bird_group, pipe_group, gamestate, score, running, last_pipe, passed_pipe, WINDOW_HEIGHT, [scale_x, scale_y], sounds)

            scrolling = True
            disp_score(screen, score)
        
        # pause state
        elif gamestate == 'paused':

            # run pause state function and the get the return values from there
            gamestate, running = pause_state(screen, gamestate, running, [WINDOW_WIDTH, WINDOW_HEIGHT], fonts, sounds, WHITE)
                
            # stop the background moving backgrounds
            scrolling = False

            disp_score(screen, score)
        
        # gameover state
        elif gamestate == 'gameover':

            # check for any inputs and restart if r is pressed
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        run(screen, clock)
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        print('quit')
                if event.type == pygame.QUIT:
                    running = False
                    print('quit')
            
            # run game over state function
            game_over_state(screen, [WINDOW_WIDTH, WINDOW_HEIGHT], fonts, WHITE)

            # stop the background moving backgrounds
            scrolling = False

            # display the results
            disp_results(screen, score)
        
        # high scores state
        elif gamestate == 'high_scores':
            
            # check for any inputs and go back if b is pressed
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        run(screen, clock)
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        print('quit')
                if event.type == pygame.QUIT:
                    running = False
                    print('quit')
            
            # run high scores states function
            high_scores_state(screen, [WINDOW_WIDTH, WINDOW_HEIGHT], fonts, WHITE)

            # display the high scores
            disp_high_scores(screen)

def main():
    """Function loads the pygame display and sets the clock"""

    # Set the display size
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Floppy Bird")

    # Create a clock
    clock = pygame.time.Clock()

    # Call the run function to run the game
    run(screen, clock)
    


# Call main function
if __name__ == '__main__':
    main()
    # quit pygame when done
    pygame.quit()
    