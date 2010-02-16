import time
import random
import pygame
import sys
import math

from fast.physics import Vec2d, Particle, World as PhysicsWorld

class World(PhysicsWorld):
	def __init__(self, size, settings):
		PhysicsWorld.__init__(self);
		self.size = Vec2d(*size)
		self.norender = not settings['render']
		self.draw_fps = settings['draw_fps']
		self.timestep = settings['timestep']
				
		self.units = [];
		self.obstacles = [];
		self.clock = pygame.time.Clock()
		self.iterations = 0
		self.runtime = 0
		self.callbacks = []
		self.settings = settings
		
	def addunit(self, unit):
		self.units.append(unit)
		self.bind(unit);
	
	def removeunit(self, unit):
		self.units.remove(unit)
		self.unbind(unit)

	def add_obstacle(self, obstacle):
		self.obstacles.append(obstacle)
		self.bind(obstacle)
		
	def remove_obstacle(self, obstacle):
		self.obstacles.remove(obstacle)
		self.unbind(obstacle)
		
	def addcallback(self, where):
		self.callbacks.append(where)
		
	def run(self):
		pygame.init()
		pygame.display.set_caption("Crowd Navigation")
		self.screen = pygame.display.set_mode(map(int, self.size))
		
		self.update(0) #so we have no initial collisions
		self.runtime = 0
		self.iterations = 0
		
		while 1:
			if self.timestep == 0:
				dt = self.clock.tick()/1000.0
			else:
				self.clock.tick()
				dt = self.timestep
				
			self.runtime += dt
			self.iterations += 1
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
			
			self.update(dt)
			for u in self.units:
				if u.view_range != 0:
					view = self.particles_in_range(u, u.view_range)
				else:
					view = ()
				u.think(dt, view)
					
			if self.draw_fps:
				sys.stdout.write("%f fps           \r"%self.clock.get_fps())
				sys.stdout.flush()
			if not self.norender:
				self.render(self.screen)
			for o in self.callbacks:
				o.update(dt)
				if o.request_stop():
					return
			
	def render(self, screen):
		screen.fill((0,0,0))
		for o in self.obstacles:
			o.render(screen)
		for u in self.units:
			u.render(screen)
		pygame.display.flip()
		if self.settings["capture"]:
			frame_filename = "video/capture_%05d.bmp"%self.iterations
			#print "Would print image " + frame_filename
			pygame.image.save(screen, frame_filename)