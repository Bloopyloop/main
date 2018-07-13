import pygame
import player
import sprites

class enemy(sprites.sprites):

	def __init__(self, image, position, obstacles):
		sprites.sprites.__init__(self, image, position)
		self.speed = 1
		self.target = "" #Begins with none -- defined by main.py
		self.obstacles = obstacles
		
	def update(self, *args):
		if self.target.alive(): #Don't do anything if the target (player) is dead.
			collision = self.rect.colliderect(self.target.rect) #Check collision with target (player)
			if not collision: #If no collision, move...
				if self.rect.y<self.target.rect.y and self.inBoundsDown():
					self.rect.y+=self.speed
				elif self.rect.y>self.target.rect.y and self.inBoundsUp():
					self.rect.y-=self.speed
				if self.rect.x>self.target.rect.x and self.inBoundsLeft():
					self.rect.x-=self.speed
				elif self.rect.x<self.target.rect.x and self.inBoundsRight():
					self.rect.x+=self.speed
				#...and check we're not in a block.
			elif self.target.invinc == 0: #If collision, damage them and give them knockback, etc.
				#Following lines assume the target is a player. This code may need to be adjusted later.
				self.target.health -= 1
				self.target.invinc = 60 #How long invincibility lasts
				self.target.kb = 4 #How long knockback lasts
				#Knockback is delivered based on direction. Currently, diagonal knockback is possible.
				if self.rect.y<self.target.rect.y and self.inBoundsDown():
					self.target.kbdy = 10
				elif self.rect.y>self.target.rect.y and self.inBoundsUp():
					self.target.kbdy = -10
				if self.rect.x>self.target.rect.x and self.inBoundsLeft():
					self.target.kbdx = -10
				elif self.rect.x<self.target.rect.x and self.inBoundsRight():
					self.target.kbdx = 10

	def inBoundsDown(self):
		return self.rect.bottom < 480-16 and not self.checkTop()
	
	def inBoundsUp(self):
		return self.rect.top > 16 and not self.checkBottom()

	def inBoundsLeft(self):
		return self.rect.left > 16 and not self.checkRight()

	def inBoundsRight(self):
		return self.rect.right < 640-16 and not self.checkLeft()

	def checkLeft(self):
		hit = False
		for obstacle in self.obstacles:
			if self.rect.collidepoint(obstacle.rect.midleft) or \
					self.rect.collidepoint(obstacle.rect.topleft) or \
					self.rect.collidepoint(obstacle.rect.bottomleft):
				hit = True
		return hit

	def checkRight(self):
		hit = False
		for obstacle in self.obstacles:
			if self.rect.collidepoint(obstacle.rect.midright) or \
					self.rect.collidepoint(obstacle.rect.topright) or \
					self.rect.collidepoint(obstacle.rect.bottomright):
				hit = True
		return hit
	
	def checkTop(self):
		hit = False
		for obstacle in self.obstacles:
			if self.rect.collidepoint(obstacle.rect.midtop) or \
					self.rect.collidepoint(obstacle.rect.topleft) or \
					self.rect.collidepoint(obstacle.rect.topright):
				hit = True
		return hit

	def checkBottom(self):
		hit = False
		for obstacle in self.obstacles:
			if self.rect.collidepoint(obstacle.rect.midbottom) or \
					self.rect.collidepoint(obstacle.rect.bottomleft) or \
					self.rect.collidepoint(obstacle.rect.bottomright):
				hit = True
		return hit
