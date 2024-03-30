import pygame
import time

pm = pygame.mixer
pm.init()

# Load the sound
sound = pm.Sound('./included_sounds/UNLICENSED_piano.wav')

def loop(s, cfade):
    while True:
        c1 = pm.Channel(1)
        c1.play(s)
        slen = s.get_length() - cfade
        print(slen)
        time.sleep(slen)
        print('wake1')
        c2 = pm.Channel(2)
        c2.play(s)
        print(slen)
        time.sleep(slen)
        print('wake2')

loop(sound, 3.5)
