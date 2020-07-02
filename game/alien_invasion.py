import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)           #创建外星人群

    while True:
        gf.check_events(ai_settings, screen, ship, bullets)      #检查事件
        ship.update()                                            #飞船位置更新
        gf.update_bullets(bullets, aliens)
        gf.update_aliens(ai_settings, aliens)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)

run_game()