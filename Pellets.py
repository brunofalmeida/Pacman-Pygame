import pygame

from Sound import Sound

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
