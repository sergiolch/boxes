import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

PLAYER_COLOR = (242, 197, 114)
BACKGROUND_COLOR = (28, 97, 140)
ENEMY_COLOR = (217, 134, 61)
SCORE_COLOR = (242, 242, 242)


screen = pygame.display.set_mode((WIDTH, HEIGHT))




clock = pygame.time.Clock()

myFont = pygame.font.SysFont("couriernewttf", 35)

#print(pygame.font.get_fonts())

def set_level(score, SPEED):
	# if score < 10:
	# 	SPEED = 5
	# elif score < 20:
	# 	SPEED = 8
	# elif score < 40:
	# 	SPEED = 11
	# elif score < 60:
	# 	SPEED = 14
	# elif score < 80:
	# 	SPEED = 17
	# else:
	# 	SPEED = 23
	SPEED = score/5
	if SPEED<8:
		SPEED = 8
	if SPEED>23:
		SPEED = 23
	return SPEED

def drop_enemies(enemy_list, enemy_size):
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0, WIDTH-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list, enemy_size):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, ENEMY_COLOR, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score, SPEED):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += SPEED
		else:
			enemy_list.pop(idx)
			score += 1
	return score

def collision_check(enemy_list, player_pos, player_size, enemy_size):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos, player_size, enemy_size):
			return True
	return False

def detect_collision(player_pos, enemy_pos, player_size, enemy_size):
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < p_x + player_size) or (p_x >= e_x and p_x < e_x + enemy_size):
		if (e_y >= p_y and e_y < p_y + player_size) or (p_y >= e_y and p_y < e_y + enemy_size):
			return True
	return False

def play_game():
	player_size = 50
	player_pos = [WIDTH/2, HEIGHT-(player_size*2)]
	player_speed = 10
	key_mode_left = False
	key_mode_right = False

	enemy_size = 50
	enemy_pos = [random.randint(0, WIDTH-enemy_size), 0]
	enemy_list = [enemy_pos]

	score = 0

	SPEED = 10

	game_over = False
	while not game_over:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				game_over = True

			if event.type == pygame.KEYDOWN:

				x = player_pos[0]
				y = player_pos[1]

				if event.key == pygame.K_LEFT:
					key_mode_left = True

				elif event.key == pygame.K_RIGHT:
					key_mode_right = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					key_mode_left = False
				elif event.key == pygame.K_RIGHT:
					key_mode_right = False

		if key_mode_left:
			x -= player_speed
			if x < 0:
				x = 0
			player_pos = [x,y]
		if key_mode_right:
			x += player_speed
			if x + player_size > WIDTH:
				x = WIDTH - player_size
			player_pos = [x,y]






		screen.fill(BACKGROUND_COLOR)


		drop_enemies(enemy_list, enemy_size)
		score = update_enemy_positions(enemy_list, score, SPEED)
		SPEED = set_level(score, SPEED)
		player_speed = SPEED

		text = "Score: " + str(score)
		label = myFont.render(text, 1, SCORE_COLOR)
		screen.blit(label, (20, HEIGHT-40))

		if collision_check(enemy_list, player_pos, player_size, enemy_size):
			game_over = True
		draw_enemies(enemy_list, enemy_size)

		pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0], player_pos[1], player_size, player_size))

		clock.tick(30)
		pygame.display.update()

	score_screen()

def score_screen():

	game_over = False
	restart_game = False
	while not game_over:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				game_over = True

			if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				restart_game = True

		label = myFont.render("Press R to restart game", 1, SCORE_COLOR)
		screen.blit(label, (WIDTH/4, HEIGHT/2))
		clock.tick(30)
		pygame.display.update()

		if restart_game:
			break

	if restart_game:
		play_game()

play_game()
print("Score: " + str(score))

