import os
import sys

import pygame
import requests

delta = 0.001
longitude, latitude = 37.530887, 55.703118
zoom_count = 0
map_file = "map.png"
map_request = "http://static-maps.yandex.ru/1.x/"
params = {'l': 'map'}


def picture_setup():
    params['spn'] = f'{delta},{delta}'
    params['ll'] = f'{longitude},{latitude}'
    try:
        response = requests.get(map_request, params=params)
        assert response
        with open(map_file, "wb") as file:
            file.write(response.content)
        try:
            screen.blit(pygame.image.load(map_file), (0, 0))
        except pygame.error:
            pass
    except AssertionError:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 450))
picture_setup()
while pygame.event.wait().type != pygame.QUIT:
    if pygame.key.get_pressed():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_PAGEDOWN]:
            delta /= 10
            if delta < 0.001:
                delta = 0.001
        elif keys[pygame.K_PAGEUP]:
            delta *= 10
            if delta > 10.0:
                delta = 10.0

        if not -180 < longitude < 180:
            longitude = -longitude
        if latitude > 84:
            latitude = -(83 + latitude % 1)
        elif latitude < -84:
            latitude = 83 + latitude % 1
        if keys[pygame.K_LEFT]:
            longitude -= 1
        elif keys[pygame.K_RIGHT]:
            longitude += 1
        elif keys[pygame.K_UP]:
            latitude += 1
        elif keys[pygame.K_DOWN]:
            latitude -= 1

        print(latitude)
        picture_setup()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
os.remove(map_file)
