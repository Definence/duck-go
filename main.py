import pygame
import random

pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT)) # tuple(кортеж) immutable

playing = True

player_size = (20, 20)
player = pygame.Surface(player_size)
player.fill(COLOR_WHITE)
player_coords = player.get_rect()
player_speed = [1, 1]

while playing:
  FPS.tick(600)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      playing = False

  main_display.fill(COLOR_BLACK)

  if player_coords.bottom >= HEIGHT:
    player_speed = random.choice(([-1, -1], [1, -1]))

  if player_coords.top <= 0:
    player_speed = random.choice(([-1, 1], [1, 1]))

  if player_coords.right >= WIDTH:
    player_speed = random.choice(([-1, -1], [-1, 1]))

  if player_coords.left <= 0:
    player_speed = random.choice(([1, -1], [1, 1]))

  main_display.blit(player, player_coords) # player placement
  player_coords = player_coords.move(player_speed) # move player coordinates
  pygame.display.update() # update main display