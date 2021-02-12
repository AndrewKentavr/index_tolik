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
