import pygame

import copy

from Character import Character
from Constants import *

class Ghost (Character):
    images = [pygame.image.load ("orange_0.png").convert (), \
              pygame.image.load ("cyan_0.png").convert ()]
    for i in range (len (images)):
        images [i].set_colorkey ((0, 0, 0))
    ISBLUE_TIME = int (10 * FPS)
    ADD_TIME = int (30 * FPS)
    add_time = ADD_TIME

    def __init__ (self):
        '''in - (self)'''
        self.surface = Ghost.images [0]
        self.rect = self.surface.get_rect ()
        self.rect.left = 315
        self.rect.top = 275
        self.speed = 1
        self.course = [0] * (50 / self.speed)
        self.isBlue = False
        self.isBlue_time = 0

    def makeBlue (self):
        '''in - (self)
        Changes ghost into a blue ghost.'''
        self.isBlue = True
        self.isBlue_time = Ghost.ISBLUE_TIME       # number of frames
        self.surface = Ghost.images [1]
        self.course = []

    def makeNotBlue (self):
        '''in - (self)
        Changes blue ghost into a regular ghost.'''
        self.surface = Ghost.images [0]
        self.course = []
        self.isBlue = False
        self.isBlue_time = 0

    def checkBlue (self):
        '''in - (self)
        Checks if the ghost should return to normal, and does if necessary.'''
        self.isBlue_time -= 1
        if self.isBlue_time <= 0:
            self.makeNotBlue ()

    def reset (self):
        '''in - (self)
        Resets ghost's position and makes it regular (not blue).'''
        self.makeNotBlue ()
        self.rect.left = 315
        self.rect.top = 275
        self.course = [0] * (50 / self.speed)

    def add (self, ghosts):
        '''in - (self, list of ghosts)
        Determines is a ghost must be added, adds it to the list, and resets the add ghost timer.
        Subtracts from the add ghost timer is no ghost is added.'''
        Ghost.add_time -= 1
        if len (ghosts) == 0:
            if Ghost.add_time > int (Ghost.ADD_TIME / 10.0):
                Ghost.add_time = int (Ghost.ADD_TIME / 10.0)
            
        if Ghost.add_time <= 0:
            ghosts.append (Ghost ())
            Ghost.add_time = Ghost.ADD_TIME
            

    def canMove_distance (self, direction, walls):
        '''in - (self, direction, list of walls)
        Determines the number of steps the ghost can take in the specified direction.
        out - int'''
        test = copy.deepcopy (self)
        counter = 0
        while True:
            if not Character.canMove (test, direction, walls):
                break
            Character.move (test, direction)
            counter += 1
        return counter

    def move (self, walls, pacman):
        '''in - (self, list of walls, pacman)
        Uses AI to move ghost towards pacman.'''
        if len (self.course) > 0:
            if self.canMove (self.course [0], walls) or self.rect.colliderect (pygame.Rect((268, 248), (112, 64))):
                Character.move (self, self.course [0])
                del self.course [0]
            else:
                self.course = []

        else:
            xDistance = pacman.rect.left - self.rect.left
            yDistance = pacman.rect.top - self.rect.top
            choices = [-1, -1, -1, -1]

            if abs (xDistance) > abs (yDistance):       # horizontal 1st
                if xDistance > 0:       # right 1st
                    choices [0] = 3
                    choices [3] = 1
                elif xDistance < 0:     # left 1st
                    choices [0] = 1
                    choices [3] = 3
                    
                if yDistance > 0:       # down 2nd
                    choices [1] = 2
                    choices [2] = 0
                elif yDistance < 0:     # up 2nd
                    choices [1] = 0
                    choices [2] = 2
                else:       # yDistance == 0
                    if self.canMove_distance (2, walls) < self.canMove_distance (0, walls):     # down 2nd
                        choices [1] = 2
                        choices [2] = 0
                    elif self.canMove_distance (0, walls) < self.canMove_distance (2, walls):       # up 2nd
                        choices [1] = 0
                        choices [2] = 2
                            
            elif abs (yDistance) >= abs (xDistance):        # vertical 1st
                if yDistance > 0:       # down 1st
                    choices [0] = 2
                    choices [3] = 0
                elif yDistance < 0:     # up 1st
                    choices [0] = 0
                    choices [3] = 2
                    
                if xDistance > 0:       # right 2nd
                    choices [1] = 3
                    choices [2] = 1
                elif xDistance < 0:     # left 2nd
                    choices [1] = 1
                    choices [2] = 3
                else:       # xDistance == 0
                    if self.canMove_distance (3, walls) < self.canMove_distance (1, walls):     # right 2nd
                        choices [1] = 3
                        choices [2] = 1
                    elif self.canMove_distance (1, walls) < self.canMove_distance (3, walls):       # left 2nd
                        choices [1] = 1
                        choices [2] = 3

            if self.isBlue:
                choices.reverse ()
            choices_original = choices [:]
            for i, x in enumerate (choices [:]):
                if x == -1 or (not Character.canMove (self, x, walls)):
                    del choices [choices.index (x)]

            if len (choices) > 0:
                Character.move (self, choices [0])
                if choices_original.index (choices [0]) >= 2:       # if move is 3rd or 4th choice
                    global FPS
                    for i in range (int (FPS * 1.5)):
                        self.course.append (choices [0])
