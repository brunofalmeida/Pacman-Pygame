import pygame

class Sound (object):
    channel = pygame.mixer.Channel (2)
    opening = pygame.mixer.Sound ("opening_song.wav")
    pickUp_small = pygame.mixer.Sound ("waka_waka.wav")
    pickUp_large = pygame.mixer.Sound ("eating_cherry.wav")
    eatGhost = pygame.mixer.Sound ("eating_ghost.wav")
    death = pygame.mixer.Sound ("pacmandies.wav")
    lose = pygame.mixer.Sound ("gameover.wav")
    win = pygame.mixer.Sound ("youwin.wav")
