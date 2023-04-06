import pygame
# from main import scale_x, scale_y, WINDOW_WIDTH, WINDOW_HEIGHT

# gravity constant
GRAVITY = 1

class Bird(pygame.sprite.Sprite):
    """This is the bird class where the bird's properties and functions are located"""
    def __init__(self, x, y, scales):
        """Constructor for the bird"""

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('imgs/bird.png'), (38*scales[0], 24*scales[1]))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.dy = 0
    
    def update(self):
        """Function to handle any updates on teh bird object"""

        # Let its speed increase as more time passes
        self.dy += GRAVITY

        # update the position of the bird
        self.rect.y += self.dy
    
    def jump(self):
        """Called when the player presses spacebar"""

        # change the speed to negative 5
        self.dy = -15
