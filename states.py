"""This module contains the different stated for the game"""

import pygame
import random
from pipe import Pipe
from logger import *

def menu_state(screen, fonts, gamestate, running, dims, WHITE):
    """Function called when the game is in its menu state"""

    # game vars for current state that will be sent back
    gamestate = gamestate
    running = running

    # Show title and instructions
    title = fonts["flappy_font"].render("Floppy Bird", True, WHITE)
    title_rect = title.get_rect(center=(dims[0]/2, (dims[1]/2) - 180))
    screen.blit(title, title_rect)

    start = fonts["small_font"].render("Press space to play", True, WHITE)
    start_rect = start.get_rect(center=(dims[0]/2, (dims[1]/2) - 70))
    screen.blit(start, start_rect)

    instr = fonts["small_font"].render("Use space to jump", True, WHITE)
    instr_rect = instr.get_rect(center=(dims[0]/2, (dims[1]/2) - 10))
    screen.blit(instr, instr_rect)

    p_msg = fonts["small_font"].render("Press \"P\" to pause", True, WHITE)
    p_msg_rect = p_msg.get_rect(center=(dims[0]/2, (dims[1]/2) + 50))
    screen.blit(p_msg, p_msg_rect)

    h_msg = fonts["small_font"].render("Press \"H\" for high scores", True, WHITE)
    h_msg_rect = h_msg.get_rect(center=(dims[0]/2, (dims[1]/2) + 110))
    screen.blit(h_msg, h_msg_rect)

    quit_msg = fonts["small_font"].render("Press \"ESC\" to quit", True, WHITE)
    quit_msg_rect = quit_msg.get_rect(center=(dims[0]/2, (dims[1]/2) + 170))
    screen.blit(quit_msg, quit_msg_rect)

    # check if the enter key is pressed and change state to play
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gamestate = 'play'
            if event.key == pygame.K_h:
                gamestate = 'high_scores'
            if event.key == pygame.K_ESCAPE:
                running = False
                print('quit')
        if event.type == pygame.QUIT:
            running = False
            print('quit')
    
    return gamestate, running

def play_state(bird_group, pipe_group, gamestate, score, running, last_pipe, passed_pipe, WINDOW_HEIGHT, scales, sounds):
    """Function called when the game is on it's play state"""

    # game vars for current state that will be sent back
    gamestate = gamestate
    score = score
    running = running
    last_pipe = last_pipe
    passed_pipe = passed_pipe

    # check for any inputs and call jump if space is pressed
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pygame.mixer.Sound.play(sounds["pause_fx"])
                gamestate = 'paused'
            if event.key == pygame.K_ESCAPE:
                running = False
                print('quit')
            if event.key == pygame.K_SPACE:
                bird_group.sprites()[0].jump()
                pygame.mixer.Sound.play(sounds["jump_fx"])
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
                pygame.mixer.Sound.play(sounds["score_fx"])
    
    # set gamestate to gameover and save score if collision or hit top or bottom
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird_group.sprites()[0].rect.top < 0 or bird_group.sprites()[0].rect.bottom > WINDOW_HEIGHT-(32*scales[1]):
        save_score(score)
        pygame.mixer.Sound.play(sounds["explosion_fx"])
        pygame.mixer.Sound.play(sounds["hurt_fx"])
        gamestate='gameover'

    # generate new pipes
    now = pygame.time.get_ticks()
    if now - last_pipe > random.randint(1100,1700):
        btm_pipe = Pipe(-1, int(WINDOW_HEIGHT/2), scales=scales)
        top_pipe = Pipe(1, int(WINDOW_HEIGHT/2), scales=scales)
        pipe_group.add(btm_pipe)
        pipe_group.add(top_pipe)
        last_pipe = now
    
    # update the bird and the pipes
    bird_group.update()
    pipe_group.update()

    return gamestate, score, running, last_pipe, passed_pipe

def pause_state(screen, gamestate, running, dims, fonts, sounds, WHITE):
    """Function called when the game is on it's play state"""

    # game vars for current state that will be sent back
    gamestate = gamestate
    running = running

    # check for any inputs and resume if p is pressed
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pygame.mixer.Sound.play(sounds['pause_fx'])
                gamestate = 'play'
            if event.key == pygame.K_ESCAPE:
                running = False
                print('quit')
        if event.type == pygame.QUIT:
            running = False
            print('quit')
    
    # Show paused and instruction
    paused = fonts["huge_font"].render("PAUSED", True, WHITE)
    paused_rect = paused.get_rect(center=(dims[0]/2, (dims[1]/2) - 90))
    screen.blit(paused, paused_rect)

    p_msg = fonts["small_font"].render("Press \"P\" to continue", True, WHITE)
    p_msg_rect = p_msg.get_rect(center=(dims[0]/2, (dims[1]/2) + 35))
    screen.blit(p_msg, p_msg_rect)

    return gamestate, running

def game_over_state(screen, dims, fonts, WHITE):
    """Function called when the player loses"""

    # dim the background
    s = pygame.Surface((dims[0],dims[1]))
    s.set_alpha(128)
    s.fill((0,0,0))   
    screen.blit(s, [0,0])

    # restart instructions
    r_msg = fonts["small_font"].render("Press space to restart", True, WHITE)
    r_msg_rect = r_msg.get_rect(center=(dims[0]/2, (dims[1]/3) * 2 + 100))
    screen.blit(r_msg, r_msg_rect)

def high_scores_state(screen, dims, fonts, WHITE):
    """Function called when the game is in its high scores state"""

    # dim the background
    s = pygame.Surface((dims[0],dims[1]))
    s.set_alpha(128)
    s.fill((0,0,0))   
    screen.blit(s, [0,0])

    # show title and instructions
    title = fonts["medium_font"].render("High Scores", True, WHITE)
    title_rect = title.get_rect(center=(dims[0]/2, (dims[1]/2) - 230))
    screen.blit(title, title_rect)

    b_msg = fonts["small_font"].render("Press space to go back", True, WHITE)
    b_msg_rect = b_msg.get_rect(center=(dims[0]/2, (dims[1]/2) + 200))
    screen.blit(b_msg, b_msg_rect)