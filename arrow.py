import pygame

GREEN = (0, 255, 0)

class Arrow:

    def __init__(self, screen, x, y, width, height, gravity, rotation):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gravity = gravity
        self.rotation = rotation
        self.image = pygame.image.load('Arrow.webp')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update(self):
        self.y += self.gravity

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        self.screen.blit(rotated_image, (self.x, self.y))
        
