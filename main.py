import pygame, random
import time, threading

StartTime=time.time()
MAP_SIZE = 6400
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720

COLORS = {
    0: (0, 255, 0),
    1: (0, 0, 255),
    2: (160, 160, 160)
}


class Tilemap:
    def __init__(self):
        self.map = []
        self.generateMap()

    def generateMap(self): # fonction a modifier c'est pour tester les couleurs 
        # plains
        self.map = [[0 for i in range(MAP_SIZE)] for j in range(MAP_SIZE)]
        
        # mountains
        for i in range(100):
            for j in range(100):
                self.map[i][j] = 2


    def render(self, surface, player_x, player_y):
        # 32x32
        for x, c in enumerate(self.map[player_x: player_x + 40]): # bouge en fonction du joueur. 40 = 1280 / 32, 23 = 720 / 32
            for y, tile in enumerate(c[player_y: player_y + 23]):
                pygame.draw.rect(surface, COLORS[tile], pygame.Rect(x * 32, y * 32, 32, 32))

class FPSCounter:
    def __init__(self, clock, screen):
        self.clock = clock
        self.screen = screen

    def display(self):
        font = pygame.font.SysFont(None, 30)
        img = font.render(str(round(self.clock.get_fps())), True, (0, 0, 0))
        self.screen.blit(img, (2, 2))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 32, 32)) # joueur toujours au millieu de l'écran, c'est le bg qui bouge

class EventHandler:
    def __init__(self, game):
        self.game = game # Game pointer
        self.cooldown = 0 # pour ralentir la vitesse du personnage, l'action d'avancer ne s'execute qu'une fois sur 2

    def didQuit(self):
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                    
    def movePlayer(self, player):
        keys = pygame.key.get_pressed()
        self.cooldown += 1
        if self.cooldown >= 2:
            self.cooldown = 0
            return
        if keys[pygame.K_z] and player.y-1 > 20: # verif pour pas que le personnage ne sorte de la map
            player.y -= player.speed 
        if keys[pygame.K_q] and player.x-1 > 12:
            player.x -= player.speed
        if keys[pygame.K_s] and player.y+1 < MAP_SIZE-20:
            player.y += player.speed
        if keys[pygame.K_d] and player.x+1 < MAP_SIZE-12:
            player.x += player.speed
        
class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
        self.tilemap = Tilemap()
        self.clock = pygame.time.Clock()
        self.fps_counter = FPSCounter(self.clock, self.screen)
        self.player = Player(10, 10)
        self.event_handler = EventHandler(self)
        self.running = True
        
    def run(self):
        # Run until the user asks to quit
        

        while self.running:

            self.event_handler.didQuit()
            self.event_handler.movePlayer(self.player)

            # Fill the background with white
            self.screen.fill((255, 255, 255))

            # Draw
            self.tilemap.render(self.screen, self.player.x, self.player.y)
            self.player.render(self.screen)

            # fps
            self.clock.tick()
            self.fps_counter.display()

            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
