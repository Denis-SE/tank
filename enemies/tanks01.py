import pygame
import math

import settings
import my_tank01


class Tank(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.width, self.height = 40, 20
        self.original_image = pygame.transform.scale(pygame.image.load("tank.png"), (self.width, self.height))
        self.image = self.original_image.copy()
        self.rect = pygame.Rect(*pos, self.width, self.height)
        self.angle = 0

    def update_size(self, scale_factor):
        self.rect.width = int(self.rect.width * scale_factor)
        self.rect.height = int(self.rect.height * scale_factor)

    def move(self, x, y, heights):
        if 0 < self.rect.x + x < settings.WIDTH - self.width:
            self.rect.x += x
            self.rect.y += y
            left_y = settings.HEIGHT - int(heights[self.rect.bottomleft[0] + int(self.width / 2 - 2)])
            right_y = settings.HEIGHT - int(heights[self.rect.bottomright[0] - int(self.width / 2 - 2)])
            # print(int(self.width / 2 - 1))
            # print(self.rect.bottomleft[0] + (self.width / 2 - 1), self.rect.bottomright[0] - (self.width / 2 - 1))
            print(left_y, right_y)
            if max(left_y, right_y) - min(left_y, right_y) <= my_tank01.cross:
                diff_left_y, diff_right_y = (
                    settings.HEIGHT - self.rect.bottomleft[1] - heights[self.rect.bottomleft[0]],
                    settings.HEIGHT - self.rect.bottomright[1] - heights[self.rect.bottomright[0]],
                )
                self.angle = math.degrees(math.atan((diff_left_y - diff_right_y) / self.image.get_rect().height))
                self.image = pygame.transform.rotate(self.original_image, self.angle)
            else:
                self.rect.x -= x
                self.rect.y -= y
            # print(self.rect.x, self.rect.y)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

    def have_center_collision(self, heights):
        mid_bottom_point = self.rect.midbottom
        left_y, right_y = (
            settings.HEIGHT - self.rect.bottomleft[1] - heights[self.rect.bottomleft[0]],
            settings.HEIGHT - self.rect.bottomright[1] - heights[self.rect.bottomright[0]],
        )
        # print(abs(left_y - right_y) // 2)
        return (
            mid_bottom_point[1] + abs(left_y - right_y) // 2 >= settings.HEIGHT - heights[mid_bottom_point[0]],
            settings.HEIGHT - mid_bottom_point[1] - abs(left_y - right_y) // 2 - heights[mid_bottom_point[0]],
        )

    def have_collision(self, heights):
        left_bottom_point, right_bottom_point = self.rect.bottomleft, self.rect.bottomright
        return (
            left_bottom_point[1] >= settings.HEIGHT - heights[left_bottom_point[0]],
            right_bottom_point[1] >= settings.HEIGHT - heights[right_bottom_point[0]],
        )

    def tank_center(self):
        return int(self.rect.x + self.width / 2), int(self.rect.y + self.height / 2)
