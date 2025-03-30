import pygame
import random
import os
from pygame.locals import K_DOWN, K_LEFT, K_UP, K_RIGHT

pygame.init()

def get_player_image(image):
  # .convert_alpha()
  return pygame.transform.scale_by(pygame.image.load(image), 0.8)

def create_enemy():
  enemy = pygame.image.load('images/enemy.png').convert_alpha()
  enemy_size = enemy.get_size()
  top = random.randint(int(enemy_size[0] / 2), int(HEIGHT - enemy_size[0] / 2))
  enemy_coords = pygame.Rect(WIDTH, top, *enemy_size)
  enemy_speed = random.randint(-MAX_ENEMY_SPD, -MIN_ENEMY_SPD)
  enemy_move = [enemy_speed, 0]
  return [enemy, enemy_coords, enemy_move]

def create_bonus():
  bonus = pygame.image.load('images/bonus.png').convert_alpha()
  bonus_size = bonus.get_size()
  left, top = (random.randint(0, int(WIDTH * 0.7)), -bonus_size[1])
  bonus_coords = pygame.Rect(left, top, *bonus_size)
  bonus_speed = random.randint(MIN_BONUS_SPD, MAX_BONUS_SPD)
  bonus_move = [0, bonus_speed]
  return [bonus, bonus_coords, bonus_move]

# system
DEBUG_MODE = False  # Add debug mode flag
FPS = pygame.time.Clock(); FPS_LOCK = 60; HEIGHT = 800; WIDTH = 1200; FONT = pygame.font.SysFont('Verdana', 16)
BG = pygame.transform.scale(pygame.image.load('images/background.png'), (WIDTH, HEIGHT))
# colors
COLOR_WHITE = (255, 255, 255); COLOR_YELLOW = (255, 255, 0); COLOR_BLACK = (0, 0, 0);
COLOR_BLUE = (0, 0, 255); COLOR_RED = (255, 0, 0)
# speed
BG_SPD = 1; PLAYER_SPD = 4 + BG_SPD
MIN_BONUS_SPD = 1; MAX_BONUS_SPD = 3
MIN_ENEMY_SPD = 1 + BG_SPD; MAX_ENEMY_SPD = 6 + BG_SPD
# events
CREATE_ENEMY = pygame.USEREVENT + 1; CREATE_BONUS = pygame.USEREVENT + 2; CHANGE_PLAYER_IMG = pygame.USEREVENT + 3
# player
PLAYER_IMG_DIR = 'images/goose'; PLAYER_IMAGES = os.listdir(PLAYER_IMG_DIR)

# system
pygame.time.set_timer(CREATE_ENEMY, FPS_LOCK * 25)
pygame.time.set_timer(CREATE_BONUS, random.randint(FPS_LOCK * 30, FPS_LOCK * 80))
pygame.time.set_timer(CHANGE_PLAYER_IMG, 80)
main_display = pygame.display.set_mode((WIDTH, HEIGHT)) # tuple(кортеж) immutable
playing = True; enemies = []; bonuses = []; score = 0; lost = False
bg_X1 = 0; bg_X2 = BG.get_width(); bg_move = BG_SPD

# player
player_image = get_player_image('images/player.png')
player_size = player_image.get_size(); player = player_image
# player_size = (20, 20); player = pygame.Surface(player_size)
player_img_i = 0
player_img_i_prev = len(PLAYER_IMAGES) - 1
player_coords = pygame.Rect(int(WIDTH * 0.1), int(HEIGHT * 0.4), *player_size)
player_move_down = [0, PLAYER_SPD]; player_move_right = [PLAYER_SPD, 0];
player_move_left = [-PLAYER_SPD, 0]; player_move_up = [0, -PLAYER_SPD]

while playing:
  FPS.tick(FPS_LOCK)
  for event in pygame.event.get():
    if event.type == CHANGE_PLAYER_IMG:
      new_pl_image = get_player_image(os.path.join(PLAYER_IMG_DIR, PLAYER_IMAGES[player_img_i]))
      prev_pl_image = get_player_image(os.path.join(PLAYER_IMG_DIR, PLAYER_IMAGES[player_img_i_prev]))

      s_curr = new_pl_image.get_size(); s_prev = prev_pl_image.get_size()
      w_diff = s_curr[0] - s_prev[0]; h_diff = s_curr[1] - s_prev[1]
      player_coords = player_coords.move([-w_diff, -h_diff])

      player = new_pl_image
      player_img_i_prev = player_img_i
      player_img_i += 1

      if player_img_i >= len(PLAYER_IMAGES):
        player_img_i = 0
    if event.type == CREATE_ENEMY:
      enemies.append(create_enemy())
    elif event.type == CREATE_BONUS:
      bonuses.append(create_bonus())
    elif event.type == pygame.QUIT:
      playing = False

  # image animation
  bg_X1 -= bg_move
  bg_X2 -= bg_move
  if bg_X1 < -BG.get_width():
    bg_X1 = BG.get_width()
  if bg_X2 < -BG.get_width():
    bg_X2 = BG.get_width()
  main_display.blit(BG, (bg_X1, 0))
  main_display.blit(BG, (bg_X2, 0))

  # key binding
  keys = pygame.key.get_pressed()
  if keys[K_DOWN] and player_coords.bottom < HEIGHT:
    player_coords = player_coords.move(player_move_down)
  elif keys[K_RIGHT] and player_coords.right < WIDTH:
    player_coords = player_coords.move(player_move_right)
  elif keys[K_LEFT] and player_coords.left > 0:
    player_coords = player_coords.move(player_move_left)
  elif keys[K_UP] and player_coords.top > 0:
    player_coords = player_coords.move(player_move_up)

  # movement should be processed before render
  main_display.blit(player, player_coords) # placement
  main_display.blit(FONT.render(f"Score: {score}", True, COLOR_BLACK), (WIDTH - 85, 0))

  # Draw collision boxes in debug mode
  if DEBUG_MODE:
    pygame.draw.rect(main_display, COLOR_RED, player_coords, 1)

  for enemy in enemies:
    enemy[1] = enemy[1].move(enemy[2])
    main_display.blit(enemy[0], enemy[1])
    if DEBUG_MODE:
      pygame.draw.rect(main_display, COLOR_RED, enemy[1], 1)

  for bonus in bonuses:
    bonus[1] = bonus[1].move(bonus[2])
    main_display.blit(bonus[0], bonus[1])
    if DEBUG_MODE:
      pygame.draw.rect(main_display, COLOR_RED, bonus[1], 1)

  # render
  if not lost:
    # pygame.display.update()  # update main display
    pygame.display.flip()

  # collision and items removal should be processed after render
  for enemy in enemies:
    # Add a small threshold to make collision detection more forgiving
    if DEBUG_MODE:
      collision_threshold_x = 0; collision_threshold_y = 0
    else:
      collision_threshold_x = 20; collision_threshold_y = 20

    adjusted_player_rect = player_coords.inflate(-collision_threshold_x, -collision_threshold_y)
    adjusted_enemy_rect = enemy[1].inflate(-collision_threshold_x, -collision_threshold_y)

    if adjusted_player_rect.colliderect(adjusted_enemy_rect):
      lost = True
      pygame.time.wait(2000)
      playing = False
    if enemy[1].right < 0:
      i = enemies.index(enemy)
      enemies.pop(i)

  for bonus in bonuses:
    bonus[1] = bonus[1].move(bonus[2])
    main_display.blit(bonus[0], bonus[1])
    if player_coords.colliderect(bonus[1]):
      bonuses.pop(bonuses.index(bonus))
      score += 1
    if bonus[1].top > HEIGHT:
      bonuses.pop(bonuses.index(bonus))

