import pygame


class Clicker(object):
    def __init__(self, store):
        self.store = store
        self.area = pygame.Rect(16, 16, 352 - 16, 800 - 32)
        self.surface = pygame.Surface((self.area.width, self.area.height))
        self.font = pygame.font.SysFont("sans", 16)
        self.background = (63, 81, 181)

    def draw(self):
        self.surface.fill(self.background)
        bank_text = self.font.render("bank: " + str(self.store.bank), True, (255, 255, 255))
        self.surface.blit(bank_text, (16, 16))
        cps_text = self.font.render("cps: " + "{0:.1f}".format(self.store.get_total_cps()), True, (255, 255, 255))
        self.surface.blit(cps_text, (16, 32))

        return self.surface

    def get_area(self):
        return self.area

    def get_position(self):
        return self.area.x, self.area.y

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # FIXME: Keep color definition to one location
            if self.area.collidepoint(x, y):
                self.background = (48, 63, 159)
            else:
                self.background = (63, 81, 181)

        elif event.type == pygame.MOUSEBUTTONUP:
            # FIXME: Validation by color is really poor design.
            if self.background == (48, 63, 159):
                self.background = (63, 81, 181)
                self.store.bank += 1
