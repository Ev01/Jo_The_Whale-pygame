import pygame, random, math 
from data2 import *



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
		
		self.rect.center = (s_width / 4, s_height / 2)
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
		for food in g.foodspr:
			food.rect.center = (food.x - g.cam[0], food.y - g.cam[1])
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
		for enemy in g.enemyspr:
			enemy.rect.center = (enemy.xy[0] - g.cam[0], enemy.xy[1] - g.cam[1])
		self.col = pygame.sprite.spritecollide(self, g.enemyspr, False, pygame.sprite.collide_circle)
		
		if self.col:
			g.playing = False
				
	def update(self):
		self.move()
		
		if self.rect.right > s_width / 2 * CAM_MOVE: #hits right area
			#print(g.cam)
			g.cam[0] += self.rect.right - s_width / 2 * CAM_MOVE 
			self.rect.x -= self.rect.right - s_width / 2 * CAM_MOVE 
			
		if self.rect.x < s_width / 2 * (1 - CAM_MOVE): #hits left area
			#print(g.cam)
			g.cam[0] -= s_width / 2 * (1 - CAM_MOVE) - self.rect.x 
			self.rect.x += s_width / 2 * (1 - CAM_MOVE) - self.rect.x
			
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
		self.oldrect = self.rect.center
		g.screen1.blit(self.image, self.rect)
		#print(self.rect.center)
		self.rect.center = (self.rect.center[0] + g.cam[0] - g.cam2[0], self.rect.center[1] + g.cam[1] - g.cam2[1])
		
		g.screen2.blit(self.image, self.rect)
		self.rect.center = self.oldrect
		
class Player2(pygame.sprite.Sprite):
	_layer = 1
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.tailsprite = Spritesheet('images/puffertail.png')
		self.blowsprite = Spritesheet('images/pufferfish1.png')
		self.fish = pygame.image.load('images/pufferfish.png')
		self.fish = pygame.transform.scale(self.fish, (70, 50))
		self.image = self.fish
		
		self.tail = self.tailsprite.get_image(0, 0, 6, 4, 20, 20)
		
		self.rect = self.image.get_rect()
		#self.rect.height += 20
		#self.image.fill(BLUE)
		
		self.rect.center = (s_width / 4, s_height / 2)
		self.radius = 25
		
		
		self.speed = 10
		self.animspeed = 2
		self.animcount = 0
		self.pic = 0
		self.flip = 'l'
		self.blow = 0
		
		self.tailoffset = [45, 12]
		
		#if pygame.joystick.get_count() > 0:
		self.joy = pygame.joystick.Joystick(0)
		self.joy.init()
		
		
	def rotate(self):
		self.orgxy = (self.rect.center[0], self.rect.center[1])
		mouse = pygame.mouse.get_pos()
		self.angle = 360-math.atan2(mouse[1] - self.rect.center[1],mouse[0] - self.rect.center[0])*180 / math.pi
		self.image = pygame.transform.rotate(self.image, self.angle)
		
		self.rect.center = self.orgxy
			
	def move(self):
		#move
		self.axis = (self.joy.get_axis(0), self.joy.get_axis(1))
		self.rect.x += self.axis[0] * self.speed
		self.rect.y += self.axis[1] * self.speed
		
			
	def animate(self):
		if self.blow == 0:
			
			self.radius = 25
			self.rect.width = 70
			self.rect.height = 50
			
			self.tail = self.tailsprite.get_image(self.pic * 6, 0, 6, 4, 50, 50)
			self.image = self.fish
			self.tailoffset = [45, 12]
			if self.animcount == self.animspeed:
				self.animcount = 0
				self.pic += 1
				self.pic %= 7
				
			self.animcount += 1
	
		if self.blow > 0:
			
			if self.blow < FPS / 4:
				self.tail = self.tailsprite.get_image(self.pic * 6, 0, 6, 4, 30, 30)
				self.tailoffset = [50, 30]
				self.image = self.blowsprite.get_image(0, 9, 11, 11, 70, 70)
				
				self.radius = 35
				self.rect.width = 70
				self.rect.height = 70
			
			
			self.blow += 1
			if self.blow > FPS / 4:
				self.tailoffset = [260, 90]
				self.image = self.blowsprite.get_image(11, 0, 20, 20, 280, 280)
				
				self.radius = 140
				self.rect.width = 280
				self.rect.height = 280
				
				self.blow += 1
				
			
				
			
				
				
		
			
		#self.image.blit(self.tail, (0, 0))
			
		
			
	def foodcol(self):
		for food in g.foodspr:
			food.rect.center = (food.x - g.cam2[0], food.y - g.cam2[1])
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
		for enemy in g.enemyspr:
			enemy.rect.center = (enemy.xy[0] - g.cam2[0], enemy.xy[1] - g.cam2[1])
		if self.blow == 0:
			self.col = pygame.sprite.spritecollide(self, g.enemyspr, False, pygame.sprite.collide_circle)
			
			if self.col:
				g.playing = False
		else:
			self.col = pygame.sprite.spritecollide(self, g.enemyspr, True, pygame.sprite.collide_circle)
				
	def update(self):
		if self.blow == 0:
			self.move()
		
		if self.rect.right > g.s2rect.width * CAM_MOVE: #hits right area
			#print(g.cam)
			g.cam2[0] += self.rect.right - g.s2rect.width * CAM_MOVE
			self.rect.x -= self.rect.right - g.s2rect.width * CAM_MOVE
			
		if self.rect.x < g.s2rect.width * (1 - CAM_MOVE): #hits left area
			#print(g.cam)
			g.cam2[0] -= g.s2rect.width * (1 - CAM_MOVE) - self.rect.x 
			self.rect.x += g.s2rect.width * (1 - CAM_MOVE) - self.rect.x
			
		if self.rect.y < g.s2rect.height * (1 - CAM_MOVE): #hits top area
			#print(g.cam)
			g.cam2[1] -= g.s2rect.height * (1 - CAM_MOVE) - self.rect.y
			self.rect.y += g.s2rect.height * (1 - CAM_MOVE) - self.rect.y
			
		if self.rect.bottom > g.s2rect.height * CAM_MOVE: #hits bottom area
			#print(g.cam)
			g.cam2[1] += self.rect.bottom - g.s2rect.height * CAM_MOVE
			self.rect.y -= self.rect.bottom - g.s2rect.height * CAM_MOVE
			
		
		if self.joy.get_button(1) == True:
			if self.blow == 0:
				self.blow = 1
		else:
			self.blow = 0
			 
			
			
		self.animate()
		self.foodcol()
		self.enemcol()
		#self.rotate()
		
	def draw(self):
		self.oldrect = self.rect.center
		g.screen2.blit(self.image, (self.rect.x, self.rect.y))
		g.screen2.blit(self.tail, (self.rect.x + self.tailoffset[0], self.rect.y + self.tailoffset[1]))
		
		self.rect.center = (self.rect.center[0] - g.cam[0] + g.cam2[0], self.rect.center[1] - g.cam[1] + g.cam2[1])
		
		
		g.screen1.blit(self.image, self.rect)
		g.screen1.blit(self.tail, (self.rect.x + self.tailoffset[0], self.rect.y + self.tailoffset[1]))
		
		self.rect.center = self.oldrect
		
		
		
					
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
		
		#self.xy1 = (0, 0) #x and y on screen 1
		#self.xy2 = (0, 0) #x and y on screen 2
		
		
	def update(self):
		
		if self.spreadtimer == 0:
			#spread
			
			self.f = (Food(random.randrange(int(self.x - SPREAD_RANGE), int(self.x + SPREAD_RANGE)), random.randrange(int(self.y - SPREAD_RANGE), int(self.y + SPREAD_RANGE))))
			
			#self.f = Food(self.rect.x-10 + g.cam[0], self.rect.y-10 + g.cam[1])
			
			g.foodspr.add(self.f)
			g.all_sprites.add(self.f)
				
			self.spreadtimer = SPREAD_TIME
			
		self.spreadtimer -= 1
		
		
	def draw(self):
		self.rect.center = (self.x - g.cam[0], self.y - g.cam[1])
		g.screen1.blit(self.image, self.rect)
		
		self.rect.center = (self.x - g.cam2[0], self.y - g.cam2[1])
		g.screen2.blit(self.image, self.rect)
		
class Enemy(pygame.sprite.Sprite):
	_layer = 2
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.sprite = Spritesheet('images/shark.png') 
		self.image = self.sprite.get_image(0, 0, 17, 8)
		self.rect = self.image.get_rect()
		#self.image.fill(RED)
		self.rect.center = (x, y)
		self.radius = 25
		
		
		
		self.anim_speed = 2
		self.anim_count = 0
		self.pic = 0
		
		#the position without camera movement
		self.xy = [0, 0]
		
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
		
	def follow(self, player):
		self.a = (self.xy[0] - g.cam[0]) - player.rect.x
		self.b = (self.xy[1] - g.cam[1]) - player.rect.y
		
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
			self.xy[0] += -self.xc
		else:
			self.xy[0] += self.xc
		if self.bchange == True:
			self.xy[1] += -self.yc
		else:
			self.xy[1] += self.yc
			
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
		if self.xy[0] - g.cam[0] > g.p.rect.x - ENEMY_RANGE2 and self.xy[0] - g.cam[0] < g.p.rect.x +ENEMY_RANGE2:
			if self.xy[1] - g.cam[1] > g.p.rect.y - ENEMY_RANGE2 and self.xy[1] - g.cam[1] < g.p.rect.y + ENEMY_RANGE2:
				self.follow(g.p)
		
		
		self.animate()
		
	def draw(self):
		self.rect.center = (self.xy[0] - g.cam2[0], self.xy[1] - g.cam2[1])
		g.screen2.blit(self.image, self.rect)
		self.rect.center = (self.xy[0] - g.cam[0], self.xy[1] - g.cam[1])
		g.screen1.blit(self.image, self.rect)

class Game():
	def __init__(self):
		pygame.init()
		pygame.font.init()
		pygame.mixer.init()
		pygame.joystick.init()
		
		pygame.mixer.music.load('sounds/song.mp3')

		self.screen = pygame.display.set_mode((s_width, s_height))
		pygame.display.set_caption('Jo and Bob')
		
		self.screen1 = pygame.Surface((int(s_width / 2), s_height))
		self.s1rect = self.screen1.get_rect()
		
		self.screen2 = pygame.Surface((int(s_width / 2), s_height))
		self.s2rect = self.screen2.get_rect()
		
		
		
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
		self.p2 = Player2()
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
			self.e = Enemy(self.ex, self.ey)
			self.enemyspr.add(self.e)
				
				
			
			
			if self.ex < ENEMY_RANGE2 + self.p.rect.x and self.ex > self.p.rect.x - ENEMY_RANGE2:
				self.ex = random.randrange(-ENEMY_RANGE, ENEMY_RANGE)
				
			if self.ey < ENEMY_RANGE2 + self.p.rect.y and self.ey > self.p.rect.y - ENEMY_RANGE2:
				self.ey = random.randrange(-ENEMY_RANGE, ENEMY_RANGE)
			
			
			
			
			self.all_sprites.add(self.e)
			
			
		
		
		self.all_sprites.add(self.p)
		self.all_sprites.add(self.p2)
		
		
		self.cam = [0, 0]
		self.cam2 = [0, 0]
		self.score = 0
		
			
	def update(self):
		#print(self.s2rect.width * CAM_MOVE, self.s2rect.width, 'ye')
	
		if self.bg_colour[2] >= 200:
			self.time = 'd'
			if self.dn_timer == 0:
				self.dn_timer = DN_STAY
			
		if self.bg_colour[2] <= 70:
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
		#print(self.e.xy[0], self.e.xy[1])
		
		
			
		self.all_sprites.update()
		
		
	def draw(self):
		#self.screen1.fill(self.bg_colour)
		#self.screen2.fill(self.bg_colour)
		self.screen1.blit(self.background, (0, 0))
		self.screen2.blit(self.background, (0, 0))
		
		#self.all_sprites.draw(self.screen)
		
		#amount = 0
		for sprite in self.all_sprites:
			#if sprite.rect.right > 0 and sprite.rect.x < s_width:
				#if sprite.rect.bottom > 0 and sprite.rect.y < s_height:
					sprite.draw()
					#amount += 1
					
		self.wordcol = BLACK
		if self.bg_colour[2] > 175:
			self.wordcol = WHITE
		else:
			self.wordcol = BLACK
		
		
		
		pygame.draw.rect(self.screen2, WHITE, [0, 0, 10, s_height])
		
		
		self.screen.blit(self.screen1, (0, 0))
		self.screen.blit(self.screen2, (s_width / 2, 0))
		
		text('Score:' + str(self.score), 0, 0, 25, self.wordcol, False, self.screen)
		text('speed: ' + str(self.p.speed), 0, 20, 20, self.wordcol, False, self.screen)
		
		s = pygame.Surface((s_width, s_height), pygame.SRCALPHA)
		s.fill((0, 0, 0, self.bg_colour[2]))
		self.screen.blit(s, (0, 0))
		
		
		
		
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
		text("Game Over", s_width / 2, s_height / 2, 100, WHITE, True, self.screen)
		text('press any key to continue', s_width / 2, s_height * 13 / 20, 20, WHITE, True, self.screen)
		text('Final Score: '+str(self.score), 30, 35, 30, WHITE, False, self.screen)
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
def text(word, x, y, size, colour = WHITE, centre = True, screen = g.screen1):
	font = pygame.font.SysFont('droidsans', size, True, False)
	text = font.render(word, True, colour)
	size = font.size(word)
	if centre:
		screen.blit(text, (x - size[0] / 2, y - size[1] / 2))
	elif not centre:
		screen.blit(text, (x, y))
g.startscreen()
#g.new()

while g.running:
	g.new()
	
	g.run()
	g.goscreen()
	
pygame.quit()

