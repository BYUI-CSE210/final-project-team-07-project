import pygame
from flyingObject import Point
from flyingObject import Velocity
pygame.init()

class Player(Point,Velocity):
    def __init__(self):

        self.windowSize = [1000,500]
        self.screen = pygame.display.set_mode(self.windowSize)
        self.circleColour = pygame.color.Color('#858585')
        self.status = False


    def drawing_player(self):
        while not self.status:
            for event in pygame.event.get():
                pygame.draw.circle(self.screen,self.circleColour,[500,200], 25)
                pygame.display.flip()
                if event.type == pygame.QUIT:
                    self.status = True
        pygame.quit()

    def move_player():
        return