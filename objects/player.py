import pygame 
import objects.entity as entity

        



class Player(entity.Entity):
    def __init__(self, coords, screen, tilemap, FRICTION, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__(entity.EntityType.PLAYER,
                         "./resources/animations/player/idle/idle00.png",
                         coords, screen, tilemap, FRICTION, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.speed = 8
        
    def render(self, skin=pygame.image.load("./resources/animations/player/idle/idle00.png")):
        self.image = pygame.transform.scale(skin, (self.size, self.size))
        self.screen.blit(self.image, (self.SCREEN_WIDTH//2 - (self.size//2), self.SCREEN_HEIGHT//2 - (self.size//2))) # joueur toujours au millieu de l'écran, c'est le bg qui bouge
   
  

