import json
import math
import pygame


class Store(object):
    def __init__(self):
        self.bank = 200000000000000000
        self.items = []
        self.area = pygame.Rect(352, 0, 352, 800)
        self.scroll = 0

        with open("store-items.json") as file:
            items = json.loads(file.read())

            i = 0
            for item in items:
                self.items.append(StoreItem(item["cost"], item["cps"], 16, 16 + i))
                i += 96

        self.surface = pygame.Surface((self.area.width, len(items) * (80 + 16) + 16))

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                for item in self.items:
                    if item.area.collidepoint(x - self.area.x, y + self.scroll) and item.cost <= self.bank:
                        self.bank -= item.buy()

            elif event.button == 4:
                if self.scroll - 16 >= 0:
                    self.scroll -= 16

            elif event.button == 5:
                if self.scroll + 16 + self.area.height <= self.surface.get_height():
                    self.scroll += 16

    def draw(self):
        self.surface.fill((238, 238, 238))

        y = 16
        for item in self.items:
            item.affordable(self.bank)
            self.surface.blit(item.draw(), (item.area.x, item.area.y))
            y += 96

        return self.surface

    def get_area(self):
        return 0, self.scroll, self.area.width, self.area.height

    def get_position(self):
        return self.area.x, self.area.y

    def update(self, delta):
        for item in self.items:
            self.bank = item.update(delta, self.bank)

    def get_total_cps(self):
        return sum(item.get_total_cps() for item in self.items)


class StoreItem(object):
    def __init__(self, cost, cps, x, y):
        self.cost = cost
        self.cps = cps
        self.amount = 0
        self.elapsed = 0
        self.bank = 0
        self.area = pygame.Rect(x, y, 320, 80)
        self.font = pygame.font.SysFont("sans", 16)
        self.background = (136, 14, 79)
        self.surface = pygame.Surface((self.area.width, self.area.height))

    def get_total_cps(self):
        return self.cps * self.amount

    def buy(self):
        current_cost = self.cost

        self.amount += 1
        self.cost = math.floor(self.cost * 1.15)

        return current_cost

    def affordable(self, bank):
        if self.cost <= bank:
            self.background = (233, 30, 99)
        else:
            self.background = (136, 14, 79)

    def draw(self):
        self.surface.fill(self.background)
        color = (255, 255, 255)
        self.surface.blit(self.font.render("cost: " + str(self.cost), True, color), (16, 16))
        self.surface.blit(self.font.render("cps: " + str(self.cps), True, color), (16, self.surface.get_height() / 2 - 8))
        self.surface.blit(self.font.render("x" + str(self.amount), True, color), (16, self.surface.get_height() - 32))

        return self.surface

    def update(self, delta, bank):
        self.elapsed += delta
        if self.elapsed >= 1000:
            self.elapsed = 0
            self.bank += self.get_total_cps()

        if self.bank >= 1:
            bank += math.floor(self.bank)
            self.bank -= math.floor(self.bank)

        return bank
