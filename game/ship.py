import pygame
from settings import Settings

class Ship():
    def __init__(self, ai_settings: Settings, screen: pygame.SurfaceType):
        self.screen = screen                                   #所在屏幕
        self.ai_settings = ai_settings                         #设置

        self.image = pygame.image.load('image/ship.bmp')       #加载图片
        self.rect = self.image.get_rect()                      #飞船矩形
        self.screen_rect = screen.get_rect()                   #屏幕矩形

        self.rect.centerx = self.screen_rect.centerx           #飞船矩形x轴中间位置
        self.rect.bottom = self.screen_rect.bottom             #飞船矩形底下位置
        self.center = float(self.rect.centerx)

        self.moving_right = False                              #向左移动标志
        self.moving_left = False

    def blitme(self):                                          #更新飞船
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center