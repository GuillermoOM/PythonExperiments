import pygame, sys
from pygame.locals import *
from random import randint

#Tamano de la pantalla en pixeles
WIDTH = 700
HEIGHT = 600

class Bola(pygame.sprite.Sprite): #Clase de la bola (descripcion de que es una bola)
	def __init__(self, init_x, init_y): #Iniciar la Clase, es una funcion obligatoria para todas las clases
		pygame.sprite.Sprite.__init__(self) #obligatorio para sprites
		self.image = pygame.Surface((50, 50)) #crear una superficie para el dibujo del objeto
		pygame.draw.circle(self.image, (255, 0, 0), (25, 25), 25) #dibujar un circulo en la superficie nueva (superficie a dibujar, color, posicion relativa a la superficie, radio)
		pygame.draw.circle(self.image, (0,0,0), (25, 25), 10)
		self.image.set_colorkey((0, 0, 0))  #seleccionar color que sera transparente
		self.rect = self.image.get_rect() #Generar datos de tamano, posicion, etc.
		self.rect.centerx = init_x #tomar dato de entrada al crear un objeto de esta clase, y ponerlo como coordenada de x del rectangulo
		self.rect.centery = init_y
		self.vx = 3 #variable personal para la clase, la uso para la velocidad
		self.vy = 3
		
		#acciones o variables para decir hacia donde se movera la bola
		self.left = True
		self.right = False
		self.up = True
		self.down = False

	def update(self): #funcion obligatoria para las clases de sprite, tanto como la de __init__, esta hara los calculos en cada ciclo
		
		if self.rect.right >= WIDTH: #cada uno detecta si el lado de la bola "choca" con alguna pared, para cambiar su direccion con velocidad variable
			self.left = True
			self.right = False
			self.vx = randint(3,6)
		if self.rect.left <= 0:
			self.left = False
			self.right = True
			self.vx = randint(3,6)
		if self.rect.bottom >= HEIGHT:
			self.up = True
			self.down = False
			self.vy = randint(3,6)
		if self.rect.top <= 0:
			self.down = True
			self.up = False
			self.vy = randint(3,6)
		
		if self.left: #aplicar cambio de coordenada a tal velocidad (que cambie tantos pixeles por cada ciclo)
			self.rect.x -= self.vx
		if self.right:
			self.rect.x += self.vx
		if self.down:
			self.rect.y += self.vy
		if self.up:
			self.rect.y -= self.vy

def main(): #funcion principal, es donde corre el juego, puede correr cuando quieras, (por ejemplo despues de una eleccion en un menu)
	#initialize
	pygame.init() 
	screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
	pygame.display.set_caption("Pelota")
	pygame.display.flip()
	clock = pygame.time.Clock()
	
	#content
	
	#background = pygame.Surface(screen.get_size())
	#background.fill((100, 100, 100))
	
	background = pygame.image.load("images.jpg") #Generar una superficie que contenga dibujada esta imagen adentro
	background = pygame.transform.scale(background, screen.get_size()) #cambiar tamano de la superficie al tamano de la pantalla y asignar la nueva superficie a la variable anterior (es como un reemplazo)
	
	
	ball = pygame.sprite.Group() #crear un grupo que contenga los objetos creados, sirve cuando tienes muchos objetos del mismo tipo
	
	for i in range(0, 6): #crear 6 objetos de la clase Bola y meterlos al grupo de ball para su manejo facil, cambia el rango para la cantidad de pelotas
		ball.add(Bola(i+100, HEIGHT/2))
	
	#loop
	while 1:
		clock.tick(60)
		
		#Event handler
		for event in pygame.event.get(): #evento en caso de que ocurra algo
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
			elif event.type == KEYDOWN: #si se oprime una tecla
				if event.key == K_ESCAPE: #que tecla es?
					pygame.quit()
					sys.exit()
		
		#Draw EEERRRRYTHING				
		
		ball.update() #calcular coordenadas
		
		screen.blit(background, (0, 0)) #dibujar fondo primero
		ball.draw(screen) #dibujar todas las bolas
		pygame.display.update() #actualizar la pantalla, siempre va a lo ultimo de los ciclos

if __name__ == '__main__': main() #codigo para ejecutar juego (no es necesario)

#Referencia http://www.pygame.org/docs/ref/pygame.html















