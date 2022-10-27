import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))


screen.fill((255,255,255))

circle(screen, (255,255,0), (200,200), 100)
circle(screen, (255,0,0), (150,185), 30)
circle(screen, (0,0,0), (150,185), 14)
circle(screen, (255,0,0), (250,185), 17)
circle(screen, (0,0,0), (250,185), 7)

circle(screen, (0,0,0), (200,200), 100, 2)
circle(screen, (0,0,0), (150,185), 30, 2)
circle(screen, (0,0,0), (250,185), 17, 2)

rect(screen, (0,0,0), (160,250, 80,17), 0)

polygon(screen, (0,0,0), ((101,120),(192,172),(187,183),(94,142)))
polygon(screen, (0,0,0), ((294,135),(219,175),(224,185),(300,152)))




pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()