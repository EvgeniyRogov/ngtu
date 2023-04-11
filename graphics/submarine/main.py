import pygame
import math
import matplotlib.pyplot as plt

FPS = 60
SIZE = (WEIGHT, HEIGHT) = (640, 480)
RED = (255, 0, 0)

WATER_SURFACE = 117
WATER_BOTTOM = 376
g = 9.81
k = 0.1 # сопротивление воды
DENSITY_WATER = 1000
CHANGE_DENSITY = 10
SUB_WEIGHT = 128
SUB_HEIGHT = 104

pygame.init()

class Submarine():

	def __init__(self, h, speed, density):
		self.h = h
		self.speed = speed
		self.density = density

		self.x = 0
		self.x_trans = self.x
		self.y = h
		self.image = pygame.image.load('submarine.png')
		self.i = 0
		self.start_ticks = 0
		self.change = False

		self.x_gr = []
		self.y_gr = []

	def set_x(self, t):

		self.x = self.speed * t
		self.x_gr.append(self.x)

		if self.x > (self.i + 1) * WEIGHT:
			self.i += 1

		self.x_trans = self.x - self.i * WEIGHT

	def set_y(self, t):

		if self.change == True:
			t = (pygame.time.get_ticks() - self.start_ticks) / 1000

		y = g * (self.density - DENSITY_WATER) / (k * self.density) * (t + math.exp(-k * t) / k - 1 / k) + self.h
		self.y_gr.append(self.y)

		if y >= WATER_SURFACE and y <= WATER_BOTTOM:
			self.y = y

	def set_density(self, density):
		if density >= 300 and density <= 2000:
			self.h = self.y
			self.density = density
			self.change = True
			self.start_ticks = pygame.time.get_ticks()

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_density(self):
		return self.density

	def get_image(self):
		return self.image

	def get_rect(self):
		return (self.x_trans, self.y, SUB_WEIGHT, SUB_HEIGHT)

	def graphic(self):
		plt.plot(self.x_gr, self.y_gr)
		plt.title('График движения')
		plt.xlabel('x')
		plt.ylabel('y')
		plt.grid()
		plt.show()

def main():
	clock = pygame.time.Clock()
	pygame.display.set_caption('Submarine')
	screen = pygame.display.set_mode(SIZE)

	fon = pygame.image.load('fon.png')
	f = pygame.font.Font(None, 24)

	h = 200 
	speed = 15
	density = 1000

	submarine = Submarine(h, speed, density)
	image_submarine = submarine.get_image()

	t = 0

	start_ticks = pygame.time.get_ticks()

	while True:

		screen.blit(fon, (0, 0, WEIGHT, HEIGHT))
		text_time = f.render('time: ' + str(t), 1, RED)
		text_density = f.render('density: ' + str(submarine.get_density()), 1, RED)
		text_x = f.render('x: ' + str(submarine.get_x()), 1, RED)
		text_y = f.render('y: ' + str(submarine.get_y()), 1, RED)

		screen.blit(text_time, (5, 5))
		screen.blit(text_density, (5, 25))
		screen.blit(text_x, (5, 45))
		screen.blit(text_y, (5, 65))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				submarine.graphic()
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					density -= CHANGE_DENSITY
					submarine.set_density(density)
				elif event.key == pygame.K_DOWN:
					density += CHANGE_DENSITY
					submarine.set_density(density)

		screen.blit(image_submarine, submarine.get_rect())

		submarine.set_x(t)
		submarine.set_y(t)

		t = (pygame.time.get_ticks() - start_ticks) / 1000

		pygame.display.update()

		clock.tick(FPS)

if __name__ == "__main__":
	main()