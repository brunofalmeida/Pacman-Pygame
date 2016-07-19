# Set up pygame and modules
import pygame, random, copy
from pygame.locals import *
pygame.init ()

# Create constants
WINDOWSIZE = (650, 600)
FPS = 60        # frames per second
YELLOW = (255, 255, 0)

# Create window
wSurface = pygame.display.set_mode (WINDOWSIZE, 0, 32)
pygame.display.set_caption ("Pacman")




class Character (object):
    def __init__ (self):
        '''in - (self)'''
        self.surface = None
        self.rect = None
        self.speed = None
        
    def canMove (self, direction, walls):
        '''in - (self, direction, list of walls)
        Determines if character can move without colliding with any of the walls.
        out - bool'''
        if direction == 0:
            rectTest = self.rect.move ((0, -self.speed))
        elif direction == 1:
            rectTest = self.rect.move ((-self.speed, 0))
        elif direction == 2:
            rectTest = self.rect.move ((0, self.speed))
        elif direction == 3:
            rectTest = self.rect.move ((self.speed, 0))

        for wall in walls:
            if wall.colliderect (rectTest):
                return False
        return True

    def move (self, direction):
        '''in - (self, direction (0-3))
        Moves character in specified direction.'''
        if direction == 0:
            self.rect.top -= self.speed
        elif direction == 1:
            self.rect.left -= self.speed
        elif direction == 2:
            self.rect.top += self.speed
        elif direction == 3:
            self.rect.left += self.speed


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


class Walls (object):
    def createList (self):
        '''in - (self)
        Creates a list of wall Rect objects.
        out - list'''
        walls = []
        #walls.append(pygame.Rect((x, y), (width, height)))
        walls.append(pygame.Rect((100, 48), (448, 8)))
        walls.append(pygame.Rect((100, 55), (7, 152)))
        walls.append(pygame.Rect((180, 200), (8, 64)))
        walls.append(pygame.Rect((268, 248), (8, 64)))
        walls.append(pygame.Rect((140, 88), (48, 32)))
        walls.append(pygame.Rect((220, 88), (64, 32)))
        walls.append(pygame.Rect((364, 88), (65, 32)))
        walls.append(pygame.Rect((460, 88), (49, 32)))
        walls.append(pygame.Rect((100, 200), (86, 8)))
        walls.append(pygame.Rect((140, 152), (48, 16)))
        walls.append(pygame.Rect((316, 55), (16, 65)))
        walls.append(pygame.Rect((540, 55), (8, 153)))
        walls.append(pygame.Rect((460, 200), (88, 8)))
        walls.append(pygame.Rect((460, 152), (49, 16)))
        walls.append(pygame.Rect((412, 152), (16, 112)))
        walls.append(pygame.Rect((364, 200), (50, 16)))
        walls.append(pygame.Rect((268, 152), (112, 16)))
        walls.append(pygame.Rect((316, 166), (16, 50)))
        walls.append(pygame.Rect((220, 152), (16, 112)))
        walls.append(pygame.Rect((235, 200), (49, 16)))
        walls.append(pygame.Rect((100, 256), (88, 8)))
        walls.append(pygame.Rect((460, 256), (89, 8)))
        walls.append(pygame.Rect((460, 296), (89, 8)))
        walls.append(pygame.Rect((460, 352), (88, 8)))
        walls.append(pygame.Rect((460, 296), (9, 64)))
        walls.append(pygame.Rect((412, 296), (17, 65)))
        walls.append(pygame.Rect((220, 296), (16, 64)))
        walls.append(pygame.Rect((460, 200), (8, 64)))
        walls.append(pygame.Rect((100, 296), (88, 8)))
        walls.append(pygame.Rect((179, 296), (9, 64)))
        walls.append(pygame.Rect((100, 352), (88, 8)))
        walls.append(pygame.Rect((100, 352), (8, 193)))
        walls.append(pygame.Rect((107, 440), (33, 16)))
        walls.append(pygame.Rect((100, 536), (448, 9)))
        walls.append(pygame.Rect((540, 352), (8, 193)))
        walls.append(pygame.Rect((508, 440), (34, 16)))
        walls.append(pygame.Rect((268, 248), (40, 8)))
        walls.append(pygame.Rect((340, 248), (41, 8)))
        walls.append(pygame.Rect((460, 200), (9, 64)))
        walls.append(pygame.Rect((139, 392), (49, 17)))
        walls.append(pygame.Rect((171, 406), (17, 51)))
        walls.append(pygame.Rect((220, 392), (64, 17)))
        walls.append(pygame.Rect((364, 392), (65, 17)))
        walls.append(pygame.Rect((460, 392), (49, 17)))
        walls.append(pygame.Rect((460, 406), (17, 51)))
        walls.append(pygame.Rect((412, 440), (17, 50)))
        walls.append(pygame.Rect((364, 488), (145, 17)))
        walls.append(pygame.Rect((267, 440), (114, 17)))
        walls.append(pygame.Rect((316, 358), (16, 51)))
        walls.append(pygame.Rect((220, 440), (16, 50)))
        walls.append(pygame.Rect((139, 488), (145, 17)))
        walls.append(pygame.Rect((372, 248), (9, 64)))
        walls.append(pygame.Rect((268, 304), (113, 7)))
        walls.append(pygame.Rect((268, 344), (112, 16)))
        walls.append(pygame.Rect((316, 455), (16, 50)))
        # This wall blocks off the central box area, as it is a trap for ghosts
        walls.append(pygame.Rect((268, 248), (112, 64)))
        return walls


class Pellets (object):
    images = [pygame.image.load ("dot.png").convert (), \
              pygame.image.load ("bigdot.png").convert ()]
    imageRects = [images [0].get_rect (), images [1].get_rect ()]
    shifts = [(-images [0].get_width () / 2, -images [0].get_height () / 2), \
              (-images [1].get_width () / 2, -images [1].get_height () / 2)]
    
    def createListSmall (self):
        '''in - (self)
        Creates a list of small pellet (x, y) tuples.
        out - list'''
        pellets = []
        pellets.append((350, 72))
        pellets.append((350, 423))
        pellets.append((485, 185))
        pellets.append((125, 185))
        pellets.append((445, 424))
        pellets.append((485, 136))
        pellets.append((125, 378))
        pellets.append((395, 378))
        pellets.append((485, 72))
        pellets.append((395, 424))
        pellets.append((445, 72))
        pellets.append((445, 136))
        pellets.append((165, 424))
        pellets.append((255, 185))
        pellets.append((395, 136))
        pellets.append((125, 104))
        pellets.append((205, 424))
        pellets.append((205, 136))
        pellets.append((395, 474))
        pellets.append((165, 520))
        pellets.append((255, 136))
        pellets.append((165, 72))
        pellets.append((205, 72))
        pellets.append((255, 378))
        pellets.append((395, 330))
        pellets.append((205, 330))
        pellets.append((350, 104))
        pellets.append((525, 185))
        pellets.append((525, 378))
        pellets.append((525, 474))
        pellets.append((485, 474))
        pellets.append((445, 185))
        pellets.append((525, 424))
        pellets.append((300, 72))
        pellets.append((350, 474))
        pellets.append((350, 232))
        pellets.append((485, 520))
        pellets.append((445, 520))
        pellets.append((485, 424))
        pellets.append((445, 280))
        pellets.append((165, 378))
        pellets.append((395, 185))
        pellets.append((445, 378))
        pellets.append((125, 474))
        pellets.append((205, 520))
        pellets.append((205, 185))
        pellets.append((350, 185))
        pellets.append((255, 520))
        pellets.append((350, 378))
        pellets.append((350, 136))
        pellets.append((300, 136))
        pellets.append((300, 104))
        pellets.append((445, 232))
        pellets.append((205, 232))
        pellets.append((445, 330))
        pellets.append((300, 474))
        pellets.append((125, 424))
        pellets.append((255, 72))
        pellets.append((125, 136))
        pellets.append((300, 520))
        pellets.append((395, 520))
        pellets.append((205, 281))
        pellets.append((205, 104))
        pellets.append((300, 185))
        pellets.append((255, 330))
        pellets.append((165, 185))
        pellets.append((165, 136))
        pellets.append((205, 474))
        pellets.append((205, 378))
        pellets.append((255, 474))
        pellets.append((395, 232))
        pellets.append((165, 474))
        pellets.append((255, 232))
        pellets.append((300, 378))
        pellets.append((350, 330))
        pellets.append((255, 280))
        pellets.append((525, 104))
        pellets.append((300, 330))
        pellets.append((525, 136))
        pellets.append((395, 72))
        pellets.append((485, 378))
        pellets.append((445, 104))
        pellets.append((350, 520))
        pellets.append((300, 424))
        pellets.append((300, 232))
        pellets.append((445, 474))
        pellets.append((395, 280))
        pellets.append((255, 424))
        return pellets

    def createListLarge (self):
        '''in - (self)
        Creates a list of large pellet (x, y) tuples.
        out - list'''
        pellets = []
        pellets.append((125, 72))
        pellets.append((125, 520))
        pellets.append((525, 72))
        pellets.append((525, 520))
        return pellets

    def check (self, pellets_s, pellets_l, pacman, ghosts):
        '''in - (self, list of small pellets, list of large pellets, pacman, list of ghosts)
        Checks if pacman has eaten pellets, deletes eaten pellets, and plays pickup sound.'''
        for i, p in enumerate (pellets_s [:]):
            p_rect = Pellets.imageRects [0]
            (p_rect.centerx, p_rect.centery) = p
            if p_rect.colliderect (pacman.rect):
                del pellets_s [i]
                pacman.score += 10
                if not Sound.channel.get_busy ():
                    Sound.channel.play (Sound.pickUp_small)

        for i, p in enumerate (pellets_l [:]):
            p_rect = Pellets.imageRects [1]
            (p_rect.centerx, p_rect.centery) = p
            if p_rect.colliderect (pacman.rect):
                for g in ghosts:
                    g.makeBlue ()
                del pellets_l [i]
                pacman.score += 50
                if not Sound.channel.get_busy ():
                    Sound.channel.play (Sound.pickUp_large)


class Sound (object):
    channel = pygame.mixer.Channel (2)
    opening = pygame.mixer.Sound ("opening_song.wav")
    pickUp_small = pygame.mixer.Sound ("waka_waka.wav")
    pickUp_large = pygame.mixer.Sound ("eating_cherry.wav")
    eatGhost = pygame.mixer.Sound ("eating_ghost.wav")
    death = pygame.mixer.Sound ("pacmandies.wav")
    lose = pygame.mixer.Sound ("gameover.wav")
    win = pygame.mixer.Sound ("youwin.wav")




# Create game objects
background = pygame.image.load ("bg.png").convert ()
pacman = Pacman ()
ghosts = [Ghost ()]
walls = Walls.createList (Walls ())
pellets_small = Pellets.createListSmall (Pellets ())
pellets_large = Pellets.createListLarge (Pellets ())
clock = pygame.time.Clock ()
pygame.mixer.music.load ("bg_music.mp3")
pygame.mixer.music.set_volume (0.5)


# Opening screen and music
Sound.channel.play (Sound.opening)
wSurface.fill ((0, 0, 0))
wSurface.blit (background, (100, 0))
wSurface.blit (pacman.getScoreSurface (), (10, 10))
wSurface.blit (pacman.getLivesSurface (), (WINDOWSIZE [0] - 200, 10))
for p in pellets_small:
    wSurface.blit (Pellets.images [0], (p [0] + Pellets.shifts [0] [0], p [1] + Pellets.shifts [0] [1]))
for p in pellets_large:
    wSurface.blit (Pellets.images [1], (p [0] + Pellets.shifts [1] [0], p [1] + Pellets.shifts [1] [1]))
for g in ghosts:
    wSurface.blit (g.surface, g.rect)
wSurface.blit (pacman.surface, pacman.rect)
pygame.display.update ()
while True:
    if not pygame.mixer.get_busy ():
        break

# Game loop
keepGoing_game = True
while keepGoing_game:
    # Round loop
    keepGoing_round = True
    pygame.mixer.music.play (-1, 0.0)
    while keepGoing_round:
        clock.tick (FPS)

        # Event handling
        for event in pygame.event.get ():
            # Quitting
            if event.type == QUIT:
                keepGoing_game = keepGoing_round = False

            # Arrow key down
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    pacman.moveUp = True
                    pacman.moveLeft = pacman.moveDown = pacman.moveRight = False
                    pacman.direction = 0
                elif event.key == K_LEFT:
                    pacman.moveLeft = True
                    pacman.moveUp = pacman.moveDown = pacman.moveRight = False
                    pacman.direction = 1
                elif event.key == K_DOWN:
                    pacman.moveDown = True
                    pacman.moveUp = pacman.moveLeft = pacman.moveRight = False
                    pacman.direction = 2
                elif event.key == K_RIGHT:
                    pacman.moveRight = True
                    pacman.moveUp = pacman.moveLeft = pacman.moveDown = False
                    pacman.direction = 3

            # Arrow key up
            elif event.type == KEYUP:
                pacman.moveUp = pacman.moveLeft = pacman.moveDown = pacman.moveRight = False

        # Move pacman rectangle
        pacman.move (walls)

        # Check if pacman must teleport to the other side
        pacman.teleport ()

        # Animate and rotate pacman sprite
        pacman.getSurface ()

        # Check if pacman has eaten any pellets and delete them
        Pellets.check (Pellets (), pellets_small, pellets_large, pacman, ghosts)

        # Add a new ghost if necessary
        Ghost.add (Ghost (), ghosts)

        # Check if blue ghosts must return to normal
        for g in ghosts:
            if g.isBlue:
                g.checkBlue ()
        
        # Move ghosts
        for g in ghosts:
            g.move (walls, pacman)

        # Draw screen
        wSurface.fill ((0, 0, 0))
        wSurface.blit (background, (100, 0))
        wSurface.blit (pacman.getScoreSurface (), (10, 10))
        wSurface.blit (pacman.getLivesSurface (), (WINDOWSIZE [0] - 200, 10))
        for p in pellets_small:
            wSurface.blit (Pellets.images [0], (p [0] + Pellets.shifts [0] [0], p [1] + Pellets.shifts [0] [1]))
        for p in pellets_large:
            wSurface.blit (Pellets.images [1], (p [0] + Pellets.shifts [1] [0], p [1] + Pellets.shifts [1] [1]))
        for g in ghosts:
            wSurface.blit (g.surface, g.rect)
        wSurface.blit (pacman.surface, pacman.rect)
        pygame.display.update ()

        # Check if pacman collided with a ghost
        for g in ghosts [:]:
            if pacman.rect.colliderect (g.rect):
                if not g.isBlue:
                    keepGoing_round = False
                    pacman.lives -= 1
                    if pacman.lives == 0:
                        keepGoing_game = False
                    else:
                        Sound.channel.play (Sound.death)
                    break
                else:       # Ghost is blue
                    del ghosts [ghosts.index (g)]
                    pacman.score += 100
                    Sound.channel.play (Sound.eatGhost)
                    

        # Check if pacman has eaten all the pellets
        else:
            if len (pellets_small) == 0 and len (pellets_large) == 0:
                keepGoing_game = keepGoing_round = False
            

    # Reset round
    pygame.mixer.music.stop ()
    pacman.reset ()
    for g in ghosts:
        g.reset ()
    while True:
        if not pygame.mixer.get_busy ():
            break


# End of game screen
wSurface.fill ((0, 0, 0))
surface_temp = None

if pacman.lives == 0:       # Player loses
    Sound.channel.play (Sound.lose)
    surface_temp = pacman.getLosingSurface ()

elif len (pellets_small) == 0 and len (pellets_large) == 0:     # Player wins
    Sound.channel.play (Sound.win)
    surface_temp = pacman.getWinningSurface ()

if surface_temp != None:        # Player loses or wins (does not quit)
    rect_temp = surface_temp.get_rect ()
    rect_temp.center = wSurface.get_rect ().center
    wSurface.blit (surface_temp, rect_temp)
    pygame.display.update ()

while True:
    if not pygame.mixer.get_busy ():
        pygame.quit ()
        break
