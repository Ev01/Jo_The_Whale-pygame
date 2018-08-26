#created on 2.1.2018

import pygame, random, math 
from data2 import *

def text(word, x, y, size, colour = WHITE, centre = True):
	font = pygame.font.SysFont('droidsans', size, True, False)
	text = font.render(word, True, colour)
	size = font.size(word)
	if centre:
		g.screen.blit(text, (x - size[0] / 2, y - size[1] / 2))
	elif not centre:
		g.screen.blit(text, (x, y))

class Spritesheet():
	#class for reading spritesheets
	def __init__(self, fname):
		self.spritesheet = pygame.image.load(fname)
	
	def get_image(self, x, y, width, height, twidth = 70, theight = 50):
		self.image = pygame.Surface((width, height)).convert_alpha()
		self.image.fill(0)
		self.image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		self.image = pygame.transform.scale(self.image, (twidth, theight))
		return self.image

class Player(pygame.sprite.Sprite):
	_layer = 1
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.sprite = Spritesheet('images/whale.png')
		self.image = self.sprite.get_image(0, 0, 7, 5)
		self.rect = self.image.get_rect()
		#self.image.fill(BLUE)
		
		self.rect.center = (s_width / 2, s_height / 2)
		self.radius = 25
		
		
		self.speed = 10
		self.animspeed = 2
		self.animcount = 0
		self.pic = 0
		self.flip = 'l'
		
		
	def rotate(self):
		self.orgxy = (self.rect.center[0], self.rect.center[1])
		mouse = pygame.mouse.get_pos()
		self.angle = 360-math.atan2(mouse[1] - self.rect.center[1],mouse[0] - self.rect.center[0])*180 / math.pi
		self.image = pygame.transform.rotate(self.image, self.angle)
		
		self.rect.center = self.orgxy
			
	def move(self):
		#move
		self.mouse = pygame.mouse.get_pos()
		self.a = self.rect.center[0] - self.mouse[0]
		self.b = self.rect.center[1] - self.mouse[1]
		
		self.achange = True
		self.bchange = True
		
		if self.b < 0:
			self.b *= -1
			self.bchange = False
		if self.a < 0:
			self.a *= -1
			self.achange = False
		
		if self.a != 0 and self.b != 0:
			self.xc = float(self.a) / float(self.a + self.b) * self.speed #x speed
			self.yc = float(self.b) / float(self.a + self.b) * self.speed #y speed
		else:
			self.xc = 0
			self.yc = 0
			
		self.xc = int(self.xc)
		self.yc = int(self.yc)
			
		if self.achange == True:
			self.rect.x += -self.xc
		else:
			self.rect.x += self.xc
		if self.bchange == True:
			self.rect.y += -self.yc
		else:
			self.rect.y += self.yc
			
			

		
	def animate(self):
		if self.animcount == self.animspeed:
			self.animcount = 0
			self.pic += 1
			self.pic %= 3
			self.image = self.sprite.get_image(self.pic * 7, 0, 7, 5)
			
		self.animcount += 1
			
	def foodcol(self):
		self.col = pygame.sprite.spritecollide(self, g.foodspr, True)
		
		if self.col:
			for i in range(len(self.col)):
				
				if self.col[i].colour == GREEN or self.col[i].colour == LGREEN:
					g.score += 1
				if self.col[i].colour == RED:
					g.score += 5
					
				if self.speed < MAX_SPEED:
					self.speed += SPEED_BONUS
			
		
	def enemcol(self):
		self.col = pygame.sprite.spritecollide(self, g.enemyspr, False, pygame.sprite.collide_circle)
		
		if self.col:
			
			
			g.playing = False
				
	def update(self):
		self.move()
		
		if self.rect.right > s_width * CAM_MOVE: #hits right area
			#print(g.cam)
			g.cam[0] += self.rect.right - s_width * CAM_MOVE 
			self.rect.x -= self.rect.right - s_width * CAM_MOVE 
			
		if self.rect.x < s_width * (1 - CAM_MOVE): #hits left area
			#print(g.cam)
			g.cam[0] -= s_width * (1 - CAM_MOVE) - self.rect.x 
			self.rect.x += s_width * (1 - CAM_MOVE) - self.rect.x
			
		if self.rect.y < s_height * (1 - CAM_MOVE): #hits top area
			#print(g.cam)
			g.cam[1] -= s_height * (1 - CAM_MOVE) - self.rect.y
			self.rect.y += s_height * (1 - CAM_MOVE) - self.rect.y
			
		if self.rect.bottom > s_height * CAM_MOVE: #hits bottom area
			#print(g.cam)
			g.cam[1] += self.rect.bottom - s_height * CAM_MOVE 
			self.rect.y -= self.rect.bottom - s_height * CAM_MOVE 
			
		self.animate()
		self.foodcol()
		self.enemcol()
		#self.rotate()
		
	def draw(self):
		g.screen.blit(self.image, self.rect)
					
class Food(pygame.sprite.Sprite):
	_layer = 0
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.colour = random.choice((GREEN, LGREEN, RED))
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((FOOD_SIZE, FOOD_SIZE))
		self.rect = self.image.get_rect()
		self.image.fill(self.colour)
		self.rect.center = (self.x, self.y)
		
		self.spreadtimer = SPREAD_TIME
		
		
	def update(self):
		self.rect.center = (self.x - g.cam[0], self.y - g.cam[1])
		
		if self.spreadtimer == 0:
			#spread
			
			self.f = (Food(random.randrange(int(self.rect.x - SPREAD_RANGE + g.cam[0]), int(self.rect.x + SPREAD_RANGE + g.cam[0])), random.randrange(int(self.rect.y - SPREAD_RANGE+ g.cam[1]), int(self.rect.y + SPREAD_RANGE + g.cam[1]))))
			
			#self.f = Food(self.rect.x-10 + g.cam[0], self.rect.y-10 + g.cam[1])
			
			g.foodspr.add(self.f)
			g.all_sprites.add(self.f)
				
			self.spreadtimer = SPREAD_TIME
			
		self.spreadtimer -= 1
		
		
		
	def draw(self):
		g.screen.blit(self.image, self.rect)
		
class Enemy(pygame.sprite.Sprite):
	_layer = 2
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.sprite = Spritesheet('images/shark.png')
		self.sprite 
		self.image = self.sprite.get_image(0, 0, 17, 8)
		self.rect = self.image.get_rect()
		#self.image.fill(RED)
		self.rect.center = (x, y)
		self.radius = 25
		
		
		
		self.anim_speed = 2
		self.anim_count = 0
		self.pic = 0
		
		#the position without camera movement
		self.x = x
		self.y = y
		
		self.speed = ENEMY_SPEED
		
	def angle(self):
		self.a = self.rect.x - g.p.rect.x
		self.b = self.rect.y - g.p.rect.y
		
		#self.achange = True
		#self.bchange = True
		
		#if self.b < 0:
			#self.b *= -1
			#self.bchange = False
		#if self.a < 0:
			#self.a *= -1
			#self.achange = False
		
		if float(self.a) != 0 or float(self.b) != 0:
			self.a1 = float(self.a) / float(self.a + self.b) * 360
			self.a2 = float(self.b) / float(self.a + self.b)
		else:
			self.a1 = 0
			self.a2 = 0
			
		self.angle1 = int(self.a1)
		return self.angle1
		
	def follow(self):
		self.a = self.rect.x - g.p.rect.x
		self.b = self.rect.y - g.p.rect.y
		
		self.achange = True
		self.bchange = True
		
		if self.b < 0:
			self.b *= -1
			self.bchange = False
		if self.a < 0:
			self.a *= -1
			self.achange = False
		
		if self.a != 0 and self.b != 0:
			self.xc = float(self.a) / float(self.a + self.b) * self.speed #x speed
			self.yc = float(self.b) / float(self.a + self.b) * self.speed #y speed
		else:
			self.xc = 0
			self.yc = 0
			
		self.xc = int(self.xc)
		self.yc = int(self.yc)
			
		if self.achange == True:
			self.x += -self.xc
		else:
			self.x += self.xc
		if self.bchange == True:
			self.y += -self.yc
		else:
			self.y += self.yc
			
	def animate(self):
		if self.anim_count == self.anim_speed:
			self.anim_count = 0
			self.pic += 1
			self.pic %= 3
			self.image = self.sprite.get_image(self.pic * 17, 0, 17, 8)
			
			#self.angle1 = self.angle()
			
			#self.image = pygame.transform.rotate(self.image, self.angle1)
			
		self.anim_count += 1
			
	def update(self):
		if self.rect.x > g.p.rect.x - ENEMY_RANGE2 and self.rect.x < g.p.rect.x +ENEMY_RANGE2:
			if self.rect.y > g.p.rect.y - ENEMY_RANGE2 and self.rect.y < g.p.rect.y + ENEMY_RANGE2:
				self.follow()
		
		self.rect.center = (self.x - g.cam[0], self.y - g.cam[1])
		self.animate()
		
	def draw(self):
		g.screen.blit(self.image, self.rect)

class Game():
	def __init__(self):
		pygame.init()
		pygame.font.init()
		pygame.mixer.init()
		
		pygame.mixer.music.load('sounds/song.mp3')

		self.screen = pygame.display.set_mode((s_width, s_height))
		pygame.display.set_caption('Jo')

		
		self.clock = pygame.time.Clock()
		self.running = True
		
		print(pygame.font.get_fonts())
		self.font = pygame.font.SysFont('freemono', 25, True, False)
		
		self.startimg = pygame.image.load('images/startscreen.png').convert()
		self.background = pygame.image.load('images/background.png').convert()
		self.startimg = pygame.transform.scale(self.startimg, (s_width, s_height))
		self.background = pygame.transform.scale(self.background, (s_width, s_height))
		
			
						
	def run(self):
		self.playing = True
		
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()
			
					
	def new(self):
		
		pygame.mixer.music.rewind()
		pygame.mixer.music.play(-1)
		self.bg_colour = [0, 0, 40]
		self.time = 'd'
		self.dn_timer = 0 #how many frames it stays night or day (timer)
		
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.foodspr = pygame.sprite.Group()
		self.enemyspr = pygame.sprite.Group()
		
		self.p = Player()
		self.f = 0
		self.wordcol = BLACK
		
		
		
		for food in range(FOOD_AMOUNT):
			self.f = Food(random.randrange(-FOOD_RANGE, FOOD_RANGE), random.randrange(-FOOD_RANGE, FOOD_RANGE))
			self.all_sprites.add(self.f)
			self.foodspr.add(self.f)
		

		for enemy in range(ENEMY_AMOUNT):
			self.ex = 0
			self.ey = 0
			#while self.ex < ENEMY_RANGE2 + self.p.rect.x and self.ex > self.p.rect.x -  ENEMY_RANGE2:
			self.ex = random.randrange(-ENEMY_RANGE, ENEMY_RANGE)
				
			#while self.ey < ENEMY_RANGE2 and self.ey > -ENEMY_RANGE2:
			self.ey = random.randrange(-ENEMY_RANGE, ENEMY_RANGE)
				
				
			
			
			if self.ex < ENEMY_RANGE2 + self.p.rect.x and self.ex > self.p.rect.x - ENEMY_RANGE2:
				self.ex = random.randrange(-ENEMY_RANGE, ENEMY_RANGE)
				
			if self.ey < ENEMY_RANGE2 + self.p.rect.y and self.ey > self.p.rect.y - ENEMY_RANGE2:
				self.ey = random.randrange(-ENEMY_RANGE, ENEMY_RANGE)
			
			
			
			self.e = Enemy(self.ex, self.ey)
			self.all_sprites.add(self.e)
			self.enemyspr.add(self.e)
			
		
		
		self.all_sprites.add(self.p)
		
		
		self.cam = [0, 0]
		self.score = 0
		
			
	def update(self):
		print(len(self.foodspr))
	
		if self.bg_colour[2] >= 200:
			self.time = 'd'
			if self.dn_timer == 0:
				self.dn_timer = DN_STAY
			
		if self.bg_colour[2] <= 40:
			self.time = 'n'
			if self.dn_timer == 0:
				self.dn_timer = DN_STAY
		
		if self.dn_timer <= 1:
			if self.time == 'd':
				self.bg_colour[2] -= DAYPASS
			if self.time == 'n':
				self.bg_colour[2] += DAYPASS
			
		if self.dn_timer != 0:
			self.dn_timer -= 1
			
		if len(self.foodspr) == 0:
			self.playing = False
			
		if len(self.foodspr) > 4000:
			self.playing = False
			
		#print(self.bg_colour)
		
		
			
		self.all_sprites.update()
		
		
	def draw(self):
		#self.screen.fill(self.bg_colour)
		self.screen.blit(self.background, (0, 0))
		
		#self.all_sprites.draw(self.screen)
		amount = 0
		for sprite in self.all_sprites:
			if sprite.rect.right > 0 and sprite.rect.x < s_width:
				if sprite.rect.bottom > 0 and sprite.rect.y < s_height:
					sprite.draw()
					amount += 1
					
		self.wordcol = BLACK
		if self.bg_colour[2] > 175:
			self.wordcol = WHITE
		else:
			self.wordcol = BLACK
			
		s = pygame.Surface((s_width, s_height), pygame.SRCALPHA)
		s.fill((0, 0, 0, self.bg_colour[2]))
		self.screen.blit(s, (0, 0))
		
		text('Score:' + str(self.score), 0, 0, 25, self.wordcol, False)
		text('speed: ' + str(self.p.speed), 0, 20, 20, self.wordcol, False)
		
		pygame.display.update()
		
		
	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					
					self.pause()
				
		
	def startscreen(self):
		#self.screen.fill((0, 0, 125))
		self.screen.blit(self.startimg, (0, 0))
		#text("JO THE WHALE", s_width / 2, s_height / 2, 80, WHITE)
		text('press any key to start', s_width / 2 - 50, s_height * 2 / 20, 30, WHITE)

		pygame.display.update()
		self.waiting = True
		while self.waiting:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.waiting = False
					self.running = False
				if event.type == pygame.KEYUP:
					self.waiting = False
		
		
	def goscreen(self):
		pygame.mixer.music.stop()
		self.screen.fill(BLACK)
		text("Game Over", s_width / 2, s_height / 2, 100, WHITE)
		text('press any key to continue', s_width / 2, s_height * 13 / 20, 20, WHITE)
		text('Final Score: '+str(self.score), 30, 35, 30, WHITE, False)
		pygame.display.update()
		self.waiting = True
		while self.waiting and self.running:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.waiting = False
					self.running = False
				if event.type == pygame.KEYUP:
					self.waiting = False
			
					
	def pause(self):
		s = pygame.Surface((s_width, s_height), pygame.SRCALPHA)
		s.fill((0, 0, 0, 150))
		self.screen.blit(s, (0, 0))
		text("paused", s_width / 2, s_height / 2, 50, WHITE)
		pygame.display.update()
		self.waiting = True
		while self.waiting:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.waiting = False
					self.playing = False
					self.running = False				
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p: 
						self.waiting = False
	
	

g = Game()
g.startscreen()
#g.new()

while g.running:
	g.new()
	
	g.run()
	g.goscreen()
	
pygame.quit()

