import sys
from time import sleep
import pygame

from alien import Alien
from Bullet import Bullet
from ship import Ship
from settings import Settings
from GameStats import GameStats

#发射子弹
def fire_bullet(ai_settings: Settings, screen: pygame.SurfaceType, ship: Ship, bullets: pygame.sprite.Group):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


#检查按键按下事件
def check_keydown_events(event, ai_settings: Settings, screen: pygame.SurfaceType, ship: Ship, bullets: pygame.sprite.Group):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


#检查相应事件
def check_events(ai_settings, screen, states, play_button, ship: Ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(states, play_button, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False


def check_play_button(states, play_button, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        states.game_active = True


#更新子弹
def update_bullets(ai_settings, screen, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_aliens_collisions(ai_settings, screen, ship, aliens, bullets)


#检查外星人是否被完全消灭
def check_bullet_aliens_collisions(ai_settings, screen, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


#更新外星人
def update_aliens(ai_settings: Settings, stats: GameStats, screen, ship: Ship, aliens: pygame.sprite.Group, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


#更新屏幕
def update_screen(ai_settings, screen, states, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    for bullet in bullets:
        bullet.draw_bullet()

    if not states.game_active:
        play_button.draw_button()
    pygame.display.flip()


#获取水平外形人数量
def get_number_aliens_x(ai_settings: Settings, alien_width: int):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    alien_number = int(available_space_x / (2 * alien_width))
    return alien_number


#获取竖直外星人数量
def get_number_rows(ai_settings: Settings, ship_height: int, alien_height: int):
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


#根据位置创建外星人
def create_alien(ai_settings: Settings, screen: pygame.SurfaceType, aliens: pygame.sprite.Group, alien_number: int, row_number: int):
    alien = Alien(ai_settings, screen)
    alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


#创建外星人群
def create_fleet(ai_settings: Settings, screen: pygame.SurfaceType, ship: Ship, aliens: pygame.sprite.Group):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


#改变外星人方向
def change_fleet_direction(ai_settings: Settings, aliens: pygame.sprite.Group):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_factor
    ai_settings.fleet_direction *= -1


#检查是否有外星人到达边缘
def check_fleet_edges(ai_settings: Settings, aliens: pygame.sprite.Group):
    for alien in aliens:
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    if stats.ship_left > 0:
        stats.ship_left -= 1
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break