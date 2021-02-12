import pygame
from globals import Globals
from graphics import load_image


class LineEdit(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('lineEdit.png', -1), (300, 35))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def update(self):
        try:
            assert Globals.click
            try:
                assert self.rect.collidepoint(pygame.mouse.get_pos())
                Globals.typing = True
            except AssertionError:
                Globals.typing = False
        except AssertionError:
            pass


class Button(pygame.sprite.Sprite):
    def __init__(self, group, image, rect):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image(image, -1), (rect[2], rect[3]))
        self.rect = self.image.get_rect()
        self.rect.x = rect[0]
        self.rect.y = rect[1]


class MapButton(Button):
    def __init__(self, group, map_types, image, rect):
        super().__init__(group, image, rect)
        self.types = map_types

    def update(self):
        try:
            assert Globals.click
            try:
                assert self.rect.collidepoint(pygame.mouse.get_pos())
                Globals.params['l'] = self.types
            except AssertionError:
                pass
        except AssertionError:
            pass


class ResetButton(Button):
    def __init__(self, group, map_types, image, rect):
        super().__init__(group, image, rect)
        self.types = map_types

    def update(self):
        try:
            assert Globals.click
            try:
                assert self.rect.collidepoint(pygame.mouse.get_pos())
                Globals.params.pop('pt', None)
            except AssertionError:
                pass
        except AssertionError:
            pass
