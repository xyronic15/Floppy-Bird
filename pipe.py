import pygame
import random

# Constants
# Starting x-value for pipe
STARTING = 1300

# scroll speed
SCROLL_SPEED = 8

class Pipe(pygame.sprite.Sprite):
    """This is the pipe class where the pipe properties and functions are located"""

    def __init__(self, orientation, y, scales):
        """Constructor for the pipe"""

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('imgs/pipe.png'), (70*scales[0], 288*scales[1]))
        self.rect = self.image.get_rect()

        # set the pipe's orientation
        # 1 for from the top and -1 from the bottom
        if orientation == 1:
            # flip the image and then set it's coordinates
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [STARTING, y - (int(random.randint(150, 300) / 2))]

        if orientation == -1:
            self.rect.topleft = [STARTING, y + (int(random.randint(150, 300) / 2))]
    
    def update(self):
        """Called to update the position of the pipe during the play state"""

        # update the position using the scroll speed
        self.rect.x -= SCROLL_SPEED

        # delete if goes past left side
        if self.rect.right < 0:
            self.kill()