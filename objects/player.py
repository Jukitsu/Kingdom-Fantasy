import pygame 
import objects.entity as entity

        



class Player(entity.Entity):
    def __init__(self, coords, screen, tilemap, FRICTION, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__(self, entity.EntityType.PLAYER,
                         "./resources/animations/player/idle/idle00.png",
                         coords, screen, tilemap, FRICTION, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.speed = 4
        
    def render(self, skin=pygame.image.load("./resources/animations/player/idle/idle00.png")):
        self.image = pygame.transform.scale(skin, (self.size, self.size))
        self.screen.blit(self.image, (self.SCREEN_WIDTH//2 - (self.size//2), self.SCREEN_HEIGHT//2 - (self.size//2))) # joueur toujours au millieu de l'écran, c'est le bg qui bouge
   
    def move(self, delta_time):
        self.velocity = [v + a * f * delta_time for v, a, f in zip(self.velocity, self.accel, self.friction)]

        
        self.check_collision(delta_time)
                        
              
        self.x += self.velocity[0] * delta_time * self.speed
        self.y += self.velocity[1] * delta_time * self.speed

        self.velocity = [v - min(v * f * delta_time, v, key = abs) for v, f in zip(self.velocity, self.friction)]


  

