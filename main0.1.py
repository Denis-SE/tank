import pygame
import numpy as np

from enemies.tanks01 import Tank
import settings
import my_tank01

# Инициализация Pygame
pygame.init()

# Размеры окна
width, height = settings.WIDTH, settings.HEIGHT

FPS = settings.FPS

clock = pygame.time.Clock()
dt = clock.tick(FPS)
tank_speed = my_tank01.speed

# Создание окна
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))
pygame.display.set_caption("Tank Game")

# Создание поверхности
surface = pygame.Surface((screen.get_width(), screen.get_height()))
surface.fill((255, 255, 255))

# Создание танка
tank = Tank((620, 400))

# Скорость движения танка

# Создание массива для хранения высот поверхности
surface_heights = np.zeros((width,))

# Заполнение массива синусоидными значениями
amplitude = settings.AMPLITUDE  # Амплитуда синусоиды
frequency = settings.FREQUENCY  # Частота синусоиды

for i in range(width):
    surface_heights[i] = amplitude * np.sin(frequency * i) + amplitude

all_sprites = pygame.sprite.Group()
all_sprites.add(tank)


def shot():
    print('space')
    # bullet =
    # При выстреле деформируем поверхность
    mx, my = tank.tank_center()
    print(mx, my)
    pygame.draw.circle(surface, 'red', (mx, my), 20)
    surface_heights[mx - 10:mx + 10] -= 10


running = True
while running:
    for event in pygame.event.get():  # обработка нажатия на крестик (выход)
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shot()
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        tank.move(tank_speed, 0, surface_heights)
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        tank.move(-tank_speed, 0, surface_heights)

    collision = tank.have_center_collision(surface_heights)
    if collision[0]:
        tank.move(
            0,
            collision[1] if collision[1] < -1 else 0,
            surface_heights
        )
    else:
        tank.move(0, collision[1], surface_heights)

    surface.fill((255, 255, 255))

    all_sprites.update()
    all_sprites.draw(surface)
    # tank.draw(surface)

    for x in range(width):
        y = int(surface_heights[x])
        pygame.draw.line(surface, (0, 0, 0), (x, height), (x, height - y))

    screen.blit(surface, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)
# Завершение работы Pygame
pygame.quit()
