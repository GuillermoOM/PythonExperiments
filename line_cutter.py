#Author: Guillermo Ochoa
#Last update: 27/09/2016 dd/mm/yyyy
#Move with Arrow Keys, snap throught lines

import math, pygame, os, sys
from random import randint
from pygame.locals import *

WIDTH = 1000
HEIGHT = 700

class Human(pygame.sprite.Sprite):
	def __init__(self, init_x, init_y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((30, 30))
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.x = init_x
		self.rect.y = init_y
		self.ANG = 0
		self.vel = 6

		#actions
		self.left = False
		self.right = False
		self.up = False
		self.down = False

	def update(self):
		
		if self.rect.x > 0:
			if self.left:
				self.rect.x -= self.vel
		if self.rect.x < WIDTH - 30:
			if self.right:
				self.rect.x += self.vel
		if self.rect.y < HEIGHT - 30:
			if self.down:
				self.rect.y += self.vel
		if self.rect.y > 0:
			if self.up:
				self.rect.y -= self.vel
		
		mouse_pos = pygame.mouse.get_pos()
		dy = self.rect.y - mouse_pos[1]
		dx = self.rect.x - mouse_pos[0]
		self.ANG = math.atan2(-dy, dx) * (180 / math.pi) + 180
			
class Zombie(pygame.sprite.Sprite):
	def __init__(self, init_x, init_y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((30, 30))
		self.image.fill((0, 200, 0))
		self.rect = self.image.get_rect()
		self.rect.x = init_x
		self.rect.y = init_y
		self.ANG = 0
		self.Speed = randint(2, 3)
		
	def update(self):
		self.rect.x += math.cos(math.radians(self.ANG)) * self.Speed
		self.rect.y += -math.sin(math.radians(self.ANG)) * self.Speed
		
def main():
	#initialize
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT),0, 32)
	pygame.display.set_caption("Z-Blocks")
	pygame.display.flip()
	clock = pygame.time.Clock()
	spawn_time = 0
	pausa = False
	#content
	background = pygame.Surface(screen.get_size())
	background.fill((50, 50, 50))
	
	player = Human(WIDTH/2, HEIGHT/2)
	zombies = pygame.sprite.Group()
	player_g = pygame.sprite.Group()
	lines = pygame.sprite.Group()
	
	player_g.add(player)
	
	#loop
	while 1:
		if not pausa:
			screen.blit(background, (0, 0))
			time_passed = clock.tick(60)
			
			#Event handler
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
					
				elif event.type == KEYDOWN:
					if event.key == K_p:
						pausa = True
					elif event.key == K_a:
						player.left = True
					elif event.key == K_d:
						player.right = True
					elif event.key == K_w:
						player.up = True
					elif event.key == K_s:
						player.down = True
					elif event.key == K_SPACE:
						zombies.empty()
				elif event.type == KEYUP:
					if event.key == K_a:
						player.left = False
					elif event.key == K_d:
						player.right = False
					elif event.key == K_w:
						player.up = False
					elif event.key == K_s:
						player.down = False

			#Handle Sprites
			spawn_time -= 1
			if spawn_time <= 0:
				switch = randint(1, 4)
				if switch == 1:
					zombies.add(Zombie(randint(1, WIDTH),-40))
				elif switch == 2:
					zombies.add(Zombie(randint(1, WIDTH),HEIGHT+40))
				elif switch == 3:
					zombies.add(Zombie(-40,randint(1, HEIGHT)))
				elif switch == 4:
					zombies.add(Zombie(WIDTH+40,randint(1, HEIGHT)))
				spawn_time = 100
			
			for z in zombies:
				dy = z.rect.y - player.rect.y
				dx = z.rect.x - player.rect.x
				z.ANG = math.atan2(-dy, dx) * (180 / math.pi) + 180
				
				for n in zombies:
					if 200 <= math.sqrt(abs(n.rect.x - z.rect.x)**2 + abs(n.rect.y - z.rect.y)**2) <= 300:
						linea = pygame.draw.line(screen, (255, 255, 255), (n.rect.centerx, n.rect.centery), (z.rect.centerx, z.rect.centery), 3)
						if player.rect.colliderect(linea):
							zombies.remove(z)
							zombies.remove(n)
						
				if pygame.sprite.collide_rect(z, player):
					zombies.remove(z)
				
			for l in lines:
				if l.long <= 300 or l.long >= 450:
					line.remove(l)
			
			
			#Draw EEERRRRYTHING
			
			player.update()
			zombies.update()
			player_g.draw(screen)	
			zombies.draw(screen)
			pygame.display.update()
			
		else:
			background.fill((0, 0, 0))
			screen.blit(background, (0, 0))
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_RETURN:
						pausa = False
						background.fill((50, 50, 50))
					elif event.key == K_ESCAPE:
						pygame.quit()
						sys.exit()
			pygame.display.update()

if __name__ == '__main__': main()