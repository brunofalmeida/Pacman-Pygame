import pygame

from Character import Character
from Constants import *

class Pacman (Character):
    images = [pygame.image.load ("player_u0.png").convert (), \
             pygame.image.load ("player_u1.png").convert (), \
             pygame.image.load ("player_r1.png").convert ()]
    for i in range (len (images)):
        images [i].set_colorkey ((0, 0, 0))

    def __init__ (self):
        '''in - (self)'''
        self.surface = Pacman.images [0]
        self.isFirstPic = True
        self.frame = 0
        self.rect = self.surface.get_rect ()
        self.rect.left = 315
        self.rect.top = 315
        self.direction = 0
        self.speed = 5
        self.moveUp = self.moveLeft = self.moveDown = self.moveRight = False
        self.score = 0
        self.lives = 3

    def reset (self):
        '''in - (self)
        Resets pacman's position, movement, direction, and sprite.'''
        self.surface = Pacman.images [0]
        self.isFirstPic = True
        self.frame = 0
        self.rect.left = 315
        self.rect.top = 315
        self.direction = 0
        self.moveUp = self.moveLeft = self.moveDown = self.moveRight = False

    def getSurface (self):
        '''in - (self)
        Animates and rotates pacman sprite.'''
        self.frame += 1
        if self.frame == 3:
            self.isFirstPic = not self.isFirstPic
            self.frame = 0
            
        if self.direction == 0:
            self.surface = Pacman.images [self.isFirstPic]
        elif self.direction == 1:
            self.surface = pygame.transform.rotate (Pacman.images [self.isFirstPic], 90)
        elif self.direction == 2:
            self.surface = pygame.transform.rotate (Pacman.images [self.isFirstPic], 180)
        elif self.direction == 3:
            self.surface = pygame.transform.rotate (Pacman.images [self.isFirstPic], 270)

    def move (self, walls):
        '''in - (self, list of walls)
        Determines what direction to move in and moves pacman.'''
        if self.moveUp and self.canMove (0, walls):
            Character.move (self, 0)
        if self.moveLeft and self.canMove (1, walls):
            Character.move (self, 1)
        if self.moveDown and self.canMove (2, walls):
            Character.move (self, 2)
        if self.moveRight and self.canMove (3, walls):
            Character.move (self, 3)

    def teleport (self):
        '''in - (self)
        Determines if pacman collided with one of teleport locations and moves him.'''
        if self.rect.colliderect (pygame.Rect ((100, 256), (6, 48))):
            self.rect.left += 400
        if self.rect.colliderect (pygame.Rect ((549, 256), (6, 48))):
            self.rect.left -= 400

    def getScoreSurface (self):
        '''in - (self)
        Creates surface object of pacman's score.
        out - Surface'''
        global YELLOW
        return pygame.font.SysFont (None, 48). render ("Score: " + str (self.score), True, YELLOW)

    def getLivesSurface (self):
        '''in - (self)
        Creates surface object of pacman's lives.
        out - Surface'''
        global YELLOW
        surface = pygame.font.SysFont (None, 48). render ("Lives:          ", True, YELLOW)
        x = 110
        for i in range (self.lives):
            surface.blit (Pacman.images [2], (x, 5))
            x += 25
        return surface

    def getWinningSurface (self):
        '''in - (self)
        Creates surface object of 'You Win!',
        out - Surface'''
        global YELLOW
        return pygame.font.SysFont (None, 72). render ("You Win!", True, YELLOW)

    def getLosingSurface (self):
        '''in - (self)
        Creates surface object of 'You Lose...'.
        out - Surface'''
        global YELLOW
        return pygame.font.SysFont (None, 72). render ("You Lose...", True, YELLOW)
