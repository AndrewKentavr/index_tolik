import os
import sys
import pygame
import requests
from globals import Globals


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def picture_setup(screen):
    Globals.params['spn'] = f'{Globals.delta},{Globals.delta}'
    Globals.params['ll'] = f'{Globals.longitude},{Globals.latitude}'
    try:
        response = requests.get(Globals.map_request, params=Globals.params)
        assert response
        with open("map.png", "wb") as file:
            file.write(response.content)
        try:
            screen.blit(pygame.image.load("map.png"), (0, 0))
        except pygame.error:
            pass
    except AssertionError:
        print("Ошибка выполнения запроса:")
        print(Globals.map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)


def geocoder_response(text):
    req = 'https://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                       'geocode': text,
                       'format': 'json'}
    response = requests.get(req, params=geocoder_params)
    try:
        assert response
        json_response = response.json()
        root = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return [float(element) for element in root["Point"]["pos"].split()]
    except AssertionError:
        pass
