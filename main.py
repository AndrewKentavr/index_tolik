from graphics import *
from UI import *

pygame.init()
clock = pygame.time.Clock()
tick = 0
screen = pygame.display.set_mode((600, 450))
all_sprites = pygame.sprite.Group()

search_font = pygame.font.Font(None, 18)
LineEdit(all_sprites)
MapButton(all_sprites, 'sat', 'sat_icon.png', [310, 10, 30, 30])
MapButton(all_sprites, 'sat,skl', 'hybrid_icon.png', [340, 10, 30, 30])
MapButton(all_sprites, 'map', 'map_icon.png', [370, 10, 30, 30])
ResetButton(all_sprites, 'map', 'reset_icon.png', [565, 10, 30, 30])

picture_setup(screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os.remove("map.png")
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Globals.click = True
        if event.type == pygame.KEYDOWN and Globals.typing:
            if event.key == pygame.K_BACKSPACE:
                Globals.search_text = Globals.search_text[:-1]
            elif len(Globals.search_text) <= 40 and event.key != pygame.K_RETURN:
                Globals.search_text += event.unicode

    if pygame.key.get_pressed():
        keys = pygame.key.get_pressed()
        if not Globals.typing:
            if keys[pygame.K_PAGEDOWN]:
                Globals.delta /= 10
            if Globals.delta < 0.001:
                Globals.delta = 0.001
            elif keys[pygame.K_PAGEUP]:
                Globals.delta *= 10
            if Globals.delta > 10.0:
                Globals.delta = 10.0

            if not -180 < Globals.longitude < 180:
                Globals.longitude = -Globals.longitude
            if Globals.latitude > 84:
                Globals.latitude = -(83 + Globals.latitude % 1)
            elif Globals.latitude < -84:
                Globals.latitude = 83 + Globals.latitude % 1
            if keys[pygame.K_LEFT]:
                Globals.longitude -= 1
            elif keys[pygame.K_RIGHT]:
                Globals.longitude += 1
            elif keys[pygame.K_UP]:
                Globals.latitude += 1
            elif keys[pygame.K_DOWN]:
                Globals.latitude -= 1
        else:
            if keys[pygame.K_RETURN]:
                Globals.longitude, Globals.latitude = geocoder_response(Globals.search_text.lower())
                Globals.params['pt'] = f'{Globals.longitude},{Globals.latitude},pm2orl'
                Globals.typing = False
        picture_setup(screen)

    all_sprites.update()
    all_sprites.draw(screen)

    search_text = search_font.render(Globals.search_text, True, (0, 0, 0))
    if Globals.typing and tick <= Globals.FPS // 10:
        search_text = search_font.render(Globals.search_text + '|', True, (0, 0, 0))
    screen.blit(search_text, (17, 20))

    Globals.click = False
    clock.tick(Globals.FPS)
    if tick >= Globals.FPS // 5:
        tick = 0
    tick += 1
    pygame.display.flip()
