import pygame, sys, math
from store import Store

pygame.init()

width = 352 * 2
height = 800

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("sans", 16)

area = pygame.Rect(16, 16, 352 - 16, height - 32)
color = (63, 81, 181)  # (255, 0, 0)
clicks = 0

store = Store()

while True:
    delta = clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Shouldn't be under a specific type.
            store.event(event)

            x, y = event.pos
            print("down (" + str(x) + ", " + str(y) + ") " + str(event.button))
            if area.collidepoint(x, y):
                color = (48,63,159)
            else:
                color = (63, 81, 181)

        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            print("up   (" + str(x) + ", " + str(y) + ")")
            if color == (48,63,159):
                color = (63, 81, 181)
                clicks += 1
                store.bank += 1

    store.update(delta)
    screen.fill((238, 238, 238))

    pygame.draw.rect(screen, color, area)

    # screen.fill((0, 0, 0), (0, 0, width, 80))
    # clicks_text = font.render("clicks: " + "{0:.1f}".format(clicks), False, (255, 255, 255))
    # screen.blit(clicks_text, (80, 20))
    bank_text = font.render("bank: " + str(store.bank), True, (255, 255, 255))
    screen.blit(bank_text, (32, 32))
    screen.blit(font.render("cps: " + "{0:.1f}".format(store.get_total_cps()), True, (255, 255, 255)), (32, 48))

    store.draw(screen)

    pygame.display.flip()
    clock.tick(60)
