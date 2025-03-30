import pygame
import random
from pygame.locals import K_DOWN, K_LEFT, K_UP, K_RIGHT

pygame.init()

def adjust_player_size(image):
  return pygame.transform.scale_by(image, 0.8)

def create_enemy():
  enemy_size = (30, 30)
  enemy = pygame.Surface(enemy_size)
  enemy.fill(COLOR_BLUE)
  enemy_coords = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
  enemy_speed = random.randint(-MAX_ENEMY_SPD, -MIN_ENEMY_SPD)
  enemy_move = [enemy_speed, 0]
  return [enemy, enemy_coords, enemy_move]

def create_bonus():
  bonus_size = (20, 20)
  bonus = pygame.Surface(bonus_size)
  bonus.fill(COLOR_YELLOW)
  left, top = (random.randint(0, int(WIDTH / 2)), -bonus_size[1])
  bonus_coords = pygame.Rect(left, top, *bonus_size)
  bonus_speed = random.randint(MIN_BONUS_SPD, MAX_BONUS_SPD)
  bonus_move = [0, bonus_speed]
  return [bonus, bonus_coords, bonus_move]

# enemy bonuses images
# move bonus appearing closer to center
# move enemy appearing closer to center (slight)

# system
FPS = pygame.time.Clock(); HEIGHT = 800; WIDTH = 1200; FONT = pygame.font.SysFont('Verdana', 16)
BG = pygame.transform.scale(pygame.image.load('images/background.png'), (WIDTH, HEIGHT))
# colors
COLOR_WHITE = (255, 255, 255); COLOR_YELLOW = (255, 255, 0); COLOR_BLACK = (0, 0, 0); COLOR_BLUE = (0, 0, 255)
# speed
BG_SPD = 1; PLAYER_SPD = 3 + BG_SPD;
MIN_BONUS_SPD = 1; MAX_BONUS_SPD = 3
MIN_ENEMY_SPD = 1 + BG_SPD; MAX_ENEMY_SPD = 6 + BG_SPD;
# events
CREATE_ENEMY = pygame.USEREVENT + 1; CREATE_BONUS = pygame.USEREVENT + 2

# system
pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, random.randint(2000, 5000))
main_display = pygame.display.set_mode((WIDTH, HEIGHT)) # tuple(кортеж) immutable
playing = True; enemies = []; bonuses = []; score = 0
bg_X1 = 0; bg_X2 = BG.get_width(); bg_move = BG_SPD

# player
player_image = pygame.image.load('images/player.png')
player_size = player_image.get_size()
player = adjust_player_size(player_image).convert_alpha()
player_coords = pygame.Rect(int(WIDTH * 0.1), int(HEIGHT * 0.4), *player_size)
player_move_down = [0, PLAYER_SPD]; player_move_right = [PLAYER_SPD, 0]; player_move_left = [-PLAYER_SPD, 0]; player_move_up = [0, -PLAYER_SPD]

while playing:
  FPS.tick(144)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      playing = False
    if event.type == CREATE_ENEMY:
      enemies.append(create_enemy())
    if event.type == CREATE_BONUS:
      bonuses.append(create_bonus())


  # image animation
  bg_X1 -= bg_move
  bg_X2 -= bg_move
  if bg_X1 < -BG.get_width():
    bg_X1 = BG.get_width()
  if bg_X2 < -BG.get_width():
    bg_X2 = BG.get_width()
  main_display.blit(BG, (bg_X1, 0))
  main_display.blit(BG, (bg_X2, 0))

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
  main_display.blit(FONT.render(f"Score: {score}", True, COLOR_BLACK), (WIDTH - 85, 0))

  for enemy in enemies:
    if player_coords.colliderect(enemy[1]):
      playing = False

    if enemy[1].right < 0:
      i = enemies.index(enemy)
      enemies.pop(i)

  for bonus in bonuses:
    if player_coords.colliderect(bonus[1]):
      bonuses.pop(bonuses.index(bonus))

    if bonus[1].top > HEIGHT:
      bonuses.pop(bonuses.index(bonus))

  # pygame.display.update() # update main display
  pygame.display.flip() # update main display


