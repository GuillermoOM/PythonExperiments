#The purpose of this program is to learn the friendship between pygame and nxt python!
#Author: Guillermo Ochoa

import pygame, sys
from pygame.locals import *
import nxt.locator
from nxt.motor import *

pygame.init()
b = nxt.locator.find_one_brick()
m_b = Motor(b, PORT_B)
m_a = Motor(b, PORT_A)
m_c = Motor(b, PORT_C)

#Window Set up.
pygame.display.set_mode((1, 1), NOFRAME)

#Write the variables..

while True:
    
    for event in pygame.event.get(KEYDOWN):

        if event.key == (K_UP):
            m_b.run(-50, True)
            m_a.run(-50, True)
            m_c.run(-50, True)

        elif event.key == (K_ESCAPE):
            pygame.quit()
            sys.exit()

    for event in pygame.event.get(KEYUP):
        
        if event.key == (K_UP):
            m_b.idle()
            m_c.idle()
            m_a.idle()
            
