#Author: Guillermo Ochoa
#Last update: 30/09/2016 dd/mm/yyyy
#Zombies mini game
#Use mouse to point and shoot, move with WASD

import math, pygame, os, sys
from random import randint
from pygame.locals import *

WIDTH = 800
HEIGHT = 500

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
		self.health = 100
		
	def update(self):
		self.rect.x += math.cos(math.radians(self.ANG)) * self.Speed
		self.rect.y += -math.sin(math.radians(self.ANG)) * self.Speed
		
class Bullet(pygame.sprite.Sprite):
	def __init__(self, init_x, init_y, angle = 0):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10, 10))
		self.image.fill((255, 255, 0))
		self.rect = self.image.get_rect()
		self.rect.x = init_x
		self.rect.y = init_y
		self.bulletSpeed = 5
		self.angle = angle
		
	def update(self):
		self.rect.x += math.cos(math.radians(self.angle)) * self.bulletSpeed
		self.rect.y += -math.sin(math.radians(self.angle)) * self.bulletSpeed


def main():
	#initialize
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT),0, 32)
	pygame.display.set_caption("Z-Blocks")
	pygame.display.flip()
	clock = pygame.time.Clock()
	spawn_time = 0
	
	#Variables
	fire = False
	next_shot = 10
	#content
	background = pygame.Surface(screen.get_size())
	background.fill((50, 50, 50))
	
	player = Human(WIDTH/2, HEIGHT/2)
	bullets = pygame.sprite.Group()
	zombies = pygame.sprite.Group() #grupo zombies creado
	player_g = pygame.sprite.Group()
	lines = pygame.sprite.Group()
	
	player_g.add(player)
	
	#loop
	while 1:
		screen.blit(background, (0, 0))
		time_passed = clock.tick(60)
		
		#Event handler
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
					
			elif event.type == MOUSEBUTTONDOWN:
				fire = True
			elif event.type == MOUSEBUTTONUP:
				fire = False
				
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				elif event.key == K_a:
					player.left = True
				elif event.key == K_d:
					player.right = True
				elif event.key == K_w:
					player.up = True
				elif event.key == K_s:
					player.down = True

			elif event.type == KEYUP:
				if event.key == K_a:
					player.left = False
				elif event.key == K_d:
					player.right = False
				elif event.key == K_w:
					player.up = False
				elif event.key == K_s:
					player.down = False
		
		if fire:
			if next_shot == 0:
				bullets.add(Bullet(player.rect.x + 10, player.rect.y + 10, player.ANG - 10))
				bullets.add(Bullet(player.rect.x + 10, player.rect.y + 10, player.ANG + 10))
				next_shot = 5
			next_shot -= 1	

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
			spawn_time = 20
		
		for z in zombies: #por cada zombie en el grupo zombiez
			dy = z.rect.y - player.rect.y
			dx = z.rect.x - player.rect.x
			z.ANG = math.atan2(-dy, dx) * (180 / math.pi) + 180
			
			if z.health <= 0:
					zombies.remove(z)
					
			for i in pygame.sprite.spritecollide(z, bullets, False): #Genera una lista de colisiones detectadas por el zombie elegido en el ciclo y el grupo de balas
				z.health -= 40 #por cada colision (i) en la lista, quitar 40 de vida al zombie elegido
					
			for i in pygame.sprite.spritecollide(z, player_g, False): #hacer lo mismo pero con colision hacia el jugador
				zombies.remove(z)
					
		for bullet in bullets:
			if bullet.rect.x > WIDTH or bullet.rect.x < 0 or bullet.rect.y > HEIGHT or bullet.rect.y < 0:
				bullets.remove(bullet)
				
			for i in pygame.sprite.spritecollide(bullet, zombies, False):
				bullets.remove(bullet)
			
		
		#Draw EEERRRRYTHING
		
		player.update()
		bullets.update()
		zombies.update()
		
		player_g.draw(screen)		
		bullets.draw(screen)
		zombies.draw(screen)
		pygame.display.update()

if __name__ == '__main__': main()