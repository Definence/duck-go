import pygame
import random
from pygame.locals import K_DOWN, K_LEFT, K_UP, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
PLAYER_SPEED = 2

main_display = pygame.display.set_mode((WIDTH, HEIGHT)) # tuple(кортеж) immutable

playing = True
enemies = []
bonuses = []

player_size = (20, 20)
player = pygame.Surface(player_size)
player.fill(COLOR_WHITE)
player_coords = player.get_rect()

def create_enemy():
  enemy_size = (30, 30)
  enemy = pygame.Surface(enemy_size)
  enemy.fill(COLOR_BLUE)
  enemy_coords = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
  enemy_speed = random.randint(-6, -1)
  enemy_move = [enemy_speed, 0]
  return [enemy, enemy_coords, enemy_move]

def create_bonus():
  bonus_size = (20, 20)
  bonus = pygame.Surface(bonus_size)
  bonus.fill(COLOR_YELLOW)
  left, top = (random.randint(0, int(WIDTH / 2)), -bonus_size[1])
  bonus_coords = pygame.Rect(left, top, *bonus_size)
  bonus_speed = random.randint(1, 3)
  bonus_move = [0, bonus_speed]
  return [bonus, bonus_coords, bonus_move]

player_move_down = [0, PLAYER_SPEED]; player_move_right = [PLAYER_SPEED, 0]
player_move_left = [-PLAYER_SPEED, 0]; player_move_up = [0, -PLAYER_SPEED]

CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, random.randint(2000, 5000))

while playing:
  FPS.tick(144)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      playing = False
    if event.type == CREATE_ENEMY:
      enemies.append(create_enemy())
    if event.type == CREATE_BONUS:
      bonuses.append(create_bonus())

  main_display.fill(COLOR_BLACK)

  keys = pygame.key.get_pressed()
  if keys[K_DOWN] and player_coords.bottom < HEIGHT:
    player_coords = player_coords.move(player_move_down)
  elif keys[K_RIGHT] and player_coords.right < WIDTH:
    player_coords = player_coords.move(player_move_right)
  elif keys[K_LEFT] and player_coords.left > 0:
    player_coords = player_coords.move(player_move_left)
  elif keys[K_UP] and player_coords.top > 0:
    player_coords = player_coords.move(player_move_up)

  for enemy in enemies:
    enemy[1] = enemy[1].move(enemy[2])
    main_display.blit(enemy[0], enemy[1])

  for bonus in bonuses:
    bonus[1] = bonus[1].move(bonus[2])
    main_display.blit(bonus[0], bonus[1])

  main_display.blit(player, player_coords) # placement
  # pygame.display.update() # update main display
  pygame.display.flip() # update main display

  for enemy in enemies:
    if enemy[1].left < 0:
      i = enemies.index(enemy)
      enemies.pop(i)

  for bonus in bonuses:
    if bonus[1].left < 0:
      i = bonuses.index(bonus)
      bonuses.pop(i)
