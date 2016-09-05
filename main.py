import pygame
import sys
from clicker import Clicker
from store import Store

pygame.init()
pygame.display.set_caption("clicker")

width = 352 * 2
height = 800

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

store = Store()
clicker = Clicker(store)

while True:
    delta = clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        else:
            store.event(event)
            clicker.event(event)

    store.update(delta)
    screen.fill((238, 238, 238))

    screen.blit(store.draw(), store.get_position(), store.get_area())
    screen.blit(clicker.draw(), clicker.get_position(), clicker.get_area())

    pygame.display.flip()
    clock.tick(60)
