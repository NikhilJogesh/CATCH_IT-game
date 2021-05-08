import pygame, random, os, json
pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 700
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("CATCH IT!")
CLOCK = pygame.time.Clock()

GAMESTATES = ["main_screen", "main_game", "retry", "info_screen", "end_screen"]

YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINKISH_RED = (236, 28, 36)
WHITE = (255, 255, 255)
GREY = (35, 35, 35)
BG = GREY

MAIN_FONT_30 = pygame.font.SysFont('Showcard Gothic', size=30)
MAIN_FONT_50 = pygame.font.SysFont('Showcard Gothic', size=50)
TITLE_FONT = pygame.font.SysFont('Showcard Gothic', size=100)

LIVES_IMG = pygame.image.load(os.path.join('Assets','life.png'))
LIVES_IMG = pygame.transform.smoothscale(LIVES_IMG, (30, 25))

MAX_LIVES = 3
score = 0
lives = 0

class Button:
    padding = 25
    outline = 2

    def __init__(self, surface, font, text, x=None, y=None):
        self.hovered = False
        self.surface = surface
        self.font = font

        self.text = self.font.render(text, 1, PINKISH_RED)
        if x == None:
        	self.x = (self.surface.get_width() - self.text.get_width())/2
        else:
        	self.x = x 
        if y == None:
        	self.y = (self.surface.get_height() - self.text.get_height())/2
        else:
        	self.y = y 
        self.width = self.text.get_width()
        self.height = self.text.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
        self.hovered_text = self.font.render(text, 1 , GREY)
        self.hovered_x = self.x - self.padding/2 
        self.hovered_y = self.y - self.padding/2 
        self.hovered_width = self.text.get_width() + self.padding
        self.hovered_height = self.text.get_height() + self.padding
        self.hovered_rect = pygame.Rect(self.hovered_x, self.hovered_y, self.hovered_width, self.hovered_height)
 
    def render(self):
        if self.hovered:
            pygame.draw.rect(self.surface, PINKISH_RED, self.hovered_rect)    
            self.surface.blit(self.hovered_text, (self.hovered_x + (self.hovered_width - self.hovered_text.get_width())/2, self.hovered_y + (self.hovered_height - self.hovered_text.get_height())/2 ))
        else:
        	pygame.draw.rect(self.surface, PINKISH_RED, self.hovered_rect)
        	pygame.draw.rect(self.surface, GREY, (self.hovered_x + self.outline, self.hovered_y + self.outline, self.hovered_width - self.outline*2, self.hovered_height - self.outline*2))
        	self.surface.blit(self.text, (self.x + (self.width - self.text.get_width())/2, self.y + (self.height - self.text.get_height())/2 ))


class Target:
	def __init__(self, radius, x, colour, vel):
		self.radius = radius
		self.x = x
		self.y = 0 - self.radius
		self.colour = colour
		self.vel = vel
		self.pos = (self.x, self.y)

	def descend(self, vel):
		self.y += vel
		self.pos = (self.x, self.y)

def create_target():
	target_colours = [YELLOW, RED, GREEN]

	x_pos = random.randrange(75, WIN_WIDTH - 75)
	colour = PINKISH_RED
	vel = random.randrange(5, 9)
	radius = random.randrange(7, 45)

	target = Target(radius, x_pos, colour, vel)
	return target

def render_target(target):
	#pygame.draw.circle(WIN, BLACK, target.pos, target.radius + 4)
	pygame.draw.circle(WIN, target.colour, target.pos, target.radius)

def main_screen():
	global game_state

	title = TITLE_FONT.render('Catch It!', 1, PINKISH_RED)
	credit = MAIN_FONT_30.render('by NIKHIL', 1, PINKISH_RED)

	buttons = []
	button_texts = ['PLAY', 'INFO','QUIT']
	start_y = 42/100 * WIN_HEIGHT
	spacing = 20
	for button_text in button_texts:
		button = Button(WIN, MAIN_FONT_50, button_text, y=start_y)
		buttons.append(button)
		start_y += button.hovered_height + spacing

	while game_state == GAMESTATES[0]:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEMOTION:
				mouse_pos = event.pos
				for button in buttons:
					if button.rect.collidepoint(mouse_pos):
						button.hovered = True
					else:
						button.hovered = False
			if event.type == pygame.MOUSEBUTTONUP:
				mouse_pos = event.pos
				for button in buttons:
					if button.rect.collidepoint(mouse_pos):
						if button is buttons[0]:
							game_state = GAMESTATES[1]
						elif button is buttons[1]:
							game_state = GAMESTATES[3]
						elif button is buttons[2]:
							pygame.quit()
							quit()
				
		def render_screen():
			WIN.fill(GREY)
			WIN.blit(title, ((WIN_WIDTH - title.get_width())/2, 13/100*WIN_HEIGHT))
			WIN.blit(credit, (65/100*WIN_WIDTH, 30/100*WIN_HEIGHT))
			for button in buttons:
				button.render()
			pygame.display.update()

		render_screen()

def info_screen():
	global game_state

	title = TITLE_FONT.render('Catch It!', 1, PINKISH_RED)
	underline = pygame.Rect((WIN_WIDTH - title.get_width())/2, 13/100*WIN_HEIGHT + title.get_height() + 5, title.get_width(), 5)
	content_text =[ 
	'Hi!, I am Nikhil, the "creator" of this "game".',
	'I Hope you did not get bored playing it',
	'This is just a little project that I made for', 
	'my coding practice using a python module', 
	'called pygame.',
	'THANK YOU !'
	]
	content = []
	for line_text in content_text:
		line = MAIN_FONT_30.render(line_text, 1, PINKISH_RED)
		content.append(line)

	main_menu_button = Button(WIN, MAIN_FONT_30, 'MAIN MENU', x=78/100*WIN_WIDTH, y=93/100*WIN_HEIGHT)

	while game_state == GAMESTATES[3]:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEMOTION:
				mouse_pos = event.pos
				if main_menu_button.rect.collidepoint(mouse_pos):
					main_menu_button.hovered = True
				else:
					main_menu_button.hovered = False 

			if event.type == pygame.MOUSEBUTTONUP:
				mouse_pos = event.pos
				if main_menu_button.rect.collidepoint(mouse_pos):
					game_state = GAMESTATES[0] 

		def render_screen():
			WIN.fill(GREY)
			WIN.blit(title, ((WIN_WIDTH - title.get_width())/2, 13/100*WIN_HEIGHT))
			pygame.draw.rect(WIN, PINKISH_RED, underline)
			start_y = 35/100*WIN_HEIGHT
			for line in content:	
				WIN.blit(line, ((WIN_WIDTH - line.get_width())/2, start_y))
				start_y += line.get_height() + 10
			main_menu_button.render()
			pygame.display.update()

		render_screen()	

def pause_screen():
	global game_state
	global paused
	global score, lives

	button_texts = ['RESUME', 'RETRY', 'MAIN MENU']
	buttons = []
	start_y = 35/100 * WIN_HEIGHT
	spacing = 20
	for button_text in button_texts:
		button = Button(WIN, MAIN_FONT_30, button_text, y=start_y)
		buttons.append(button)
		start_y += button.hovered_height + spacing

	while paused:
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEMOTION:
				mouse_pos = event.pos
				for button in buttons:
					if button.rect.collidepoint(mouse_pos):
						button.hovered = True
					else:
						button.hovered = False	
			if event.type == pygame.MOUSEBUTTONUP:
				mouse_pos = event.pos
				for button in buttons:
					if button.rect.collidepoint(mouse_pos):
						if button is buttons[0]:
							paused = False
						elif button is buttons[1]:
							game_state = GAMESTATES[2]
						elif button is buttons[2]:
							game_state = GAMESTATES[0]
						paused = False
			if event.type == pygame.KEYUP:
				if keys[pygame.K_ESCAPE]:
					paused = False
		
		def render_screen():
			for button in buttons:
				button.render()
			pygame.display.update()

		render_screen()

def end_screen():
	global game_state
	global score, lives

	end_screen_text = MAIN_FONT_50.render("GAME OVER", 1, PINKISH_RED)
	score_text = MAIN_FONT_30.render(f"SCORE : {score}", 1, PINKISH_RED)

	start_y = 200
	buttons = [
		Button(WIN, MAIN_FONT_30, "RETRY", y=53/100*WIN_HEIGHT),
		Button(WIN, MAIN_FONT_30, "MAIN MENU", x = 78/100*WIN_WIDTH, y=93/100*WIN_HEIGHT)
	]
	while game_state == GAMESTATES[4]:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.MOUSEMOTION:
				mouse_pos = event.pos
				for button in buttons:
					if button.rect.collidepoint(mouse_pos):
						button.hovered = True
					else:
						button.hovered = False

			if event.type == pygame.MOUSEBUTTONUP:
				mouse_pos = event.pos 
				for button in buttons:
					if button.rect.collidepoint(mouse_pos):
						if button is buttons[0]:
							game_state = GAMESTATES[1]
						elif button is buttons[1]:
							game_state = GAMESTATES[0]

		def render_screen():
			WIN.fill(GREY)
			WIN.blit(end_screen_text, ((WIN_WIDTH - end_screen_text.get_width())/2, start_y))
			WIN.blit(score_text, ((WIN_WIDTH - score_text.get_width())/2, start_y + end_screen_text.get_height() + 60))
			for button in buttons:
				button.render()
			pygame.display.update()

		render_screen()

def retry():
	global game_state
	game_state = GAMESTATES[1]

def game():
	global game_state
	global run
	global score, lives
	global paused

	score = 0
	lives = MAX_LIVES

	basket = pygame.Rect(WIN_WIDTH/2 - 100/2, WIN_HEIGHT - 30, 100, 20)
	BASKET_VEL = 10
	basket_left = True
	basket_right = True
	
	INFO_BAR = pygame.Rect(0, 77, WIN_WIDTH, 5)

	target_rendered = False
	paused = False
	while game_state == GAMESTATES[1]:
		CLOCK.tick(60)
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				paused = True
				pause_screen()

			if event.type == pygame.KEYUP:
				if keys[pygame.K_ESCAPE]:
					paused = True
					pause_screen()

		if keys[pygame.K_RIGHT] and basket_right:
			basket.x += BASKET_VEL
		if keys[pygame.K_LEFT] and basket_left:
			basket.x -= BASKET_VEL

		if basket.x <= 10:
			basket_left = False
		elif basket.x + basket.width >= 800 - 10:
			basket_right = False
		else:
			basket_left = True
			basket_right = True

		if not(target_rendered):
			target = create_target()
			target_rendered = True
		
		target_collider = pygame.Rect(target.x - target.radius ,target.y, target.radius*2,  target.radius )
		
		if basket.colliderect(target_collider):
			score += 100
			target_rendered = False
		elif target.y - target.radius >= WIN_HEIGHT:
			lives -= 1
			target_rendered = False

		if lives == 0:
			game_state = GAMESTATES[4]

		def render_game():
			WIN.fill(BG)

			render_target(target)
			target.descend(target.vel)

			pygame.draw.rect(WIN, PINKISH_RED, INFO_BAR)
			pygame.draw.rect(WIN, GREY, (0, 0, WIN_WIDTH, INFO_BAR.y))

			score_text = MAIN_FONT_30.render(f"SCORE:\n {score}", 1, PINKISH_RED)
			WIN.blit(score_text, ((WIN_WIDTH -  score_text.get_width())/2, 30))

			WIN.blit(MAIN_FONT_30.render("LIVES:", 1, PINKISH_RED), (687, 10))
			lives_x = 750
			for _ in range(lives):
				WIN.blit(LIVES_IMG, (lives_x, 40))
				lives_x -= LIVES_IMG.get_width() + 5

			pygame.draw.rect(WIN, BLACK, basket)
			pygame.display.update()

		render_game()

def main():
	global game_state
	game_state = GAMESTATES[0]
	
	while True:
		if game_state == GAMESTATES[0]:
			main_screen()
		elif game_state == GAMESTATES[1]:
			game()
		elif game_state == GAMESTATES[2]:
			retry() 
		elif game_state == GAMESTATES[3]:
			info_screen()
		elif game_state == GAMESTATES[4]:
			end_screen()

if __name__ == "__main__":
	main()