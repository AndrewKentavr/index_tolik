import os
import sys

import pygame
import requests

delta = 0.001
zoom_count = 0
map_file = "map.png"
map_request = "http://static-maps.yandex.ru/1.x/"
params = {'ll': '37.530887,55.703118',
          'l': 'map'
          }


def picture_setup():
    params['spn'] = f'{delta},{delta}'
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
screen = pygame.display.set_mode((600, 450))
picture_setup()
while pygame.event.wait().type != pygame.QUIT:
    if pygame.key.get_pressed():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_PAGEDOWN]:
            delta /= 10
            if delta >= 0.001:
                picture_setup()
            else:
                delta = 0.001
        elif keys[pygame.K_PAGEUP]:
            delta *= 10
            if delta < 100.0:
                picture_setup()
            else:
                delta = 100.0
    pygame.display.flip()

pygame.quit()
os.remove(map_file)
