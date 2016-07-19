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
