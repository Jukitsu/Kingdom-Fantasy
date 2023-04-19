import pygame, random, time, threading
from animations import PlayerAnimations
from perlin_noise import PerlinNoise
import pathlib
import pickle

StartTime=time.time()
MAP_SIZE = 6400
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720

FRICTION = ( 16,  16,  16)

COLORS = {
    0: (0, 0, 255), # Water
    1: (0, 255, 0), # Plains
    2: (160, 160, 160), # Mountains
    3: (255, 255, 255) # Snowy Mountains
}

def log(*args, **kw): # Debug
    print(*args, **kw)

class Level:
    def __init__(self):
        self.tilemap = None
        self.player_coords = (0, 0)
        
class Tilemap:
    def __init__(self):
        self.map = []
        self.view_offset = [0, 0]

    def generateMap(self): # fonction a modifier c'est pour tester les couleurs
        self.map = [[0 for j in range(MAP_SIZE)] for i in range(MAP_SIZE)] # First launch
        noise = PerlinNoise(octaves = 50, seed = 500)

        log("Generating Terrain")

        # Generating Terrain
        for i in range(1000):
            for j in range(1000):
                height = abs(noise((i / MAP_SIZE, j / MAP_SIZE))) * 255
                if height < 10:
                    self.map[i][j] = 0
                elif height < 60:
                    self.map[i][j] = 1
                elif height < 80:
                    self.map[i][j] = 2
                else:
                    self.map[i][j] = 3
        log("Terrain Generated")


    def render(self, surface, player):
        # 32x32
        for x in range(round(player.x - 44), round(player.x + 44)):
            for y in range(round(player.y - 26), round(player.y + 26)): # CLIPPING VALUES. TO CHANGE
                tile = self.map[x][y]
                pygame.draw.rect(surface, COLORS[tile] if x != round(player.x) or y != round(player.y) else (255, 0, 0), pygame.Rect(x * 16 - round(player.x * 16) + SCREEN_WIDTH // 2, y * 16 - round(player.y * 16) + SCREEN_HEIGHT // 2, 16, 16))

class FPScounter:
    def __init__(self, clock, screen, player):
        self.clock = clock
        self.screen = screen
        self.player = player

    def display(self):
        font = pygame.font.SysFont(None, 30)
        img = font.render(f"{round(self.clock.get_fps())}, X: {round(self.player.x, 2)}, Y: {round(self.player.y, 2)}", True, (0, 0, 0))
        self.screen.blit(img, (2, 2))
        
class Entity:
    def __init__(self, coords, screen):
        self.x, self.y = coords
        self.velocity = [0, 0]
        self.accel = [0, 0]
        self.friction = FRICTION
        self.speed = 16
        self.screen = screen


class Player(pygame.sprite.Sprite):
    def __init__(self, coords, screen):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("./resources/animations/player/idle/idle00.png"), (128, 128))
        self.rect = self.image.get_rect()
        self.x, self.y = coords
        self.velocity = [0, 0]
        self.accel = [0, 0]
        self.friction = FRICTION
        self.speed = 16
        self.screen = screen
        self.rigidBody = pygame.Rect(self.x, self.y, 16, 16)
        
    def render(self, skin="./resources/animations/player/idle/idle00.png"):
        self.image = pygame.transform.scale(pygame.image.load(skin), (128, 128))
        self.screen.blit(self.image, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)) # joueur toujours au millieu de l'écran, c'est le bg qui bouge
   
    def move(self, delta_time):
        self.velocity = [v + a * f * delta_time for v, a, f in zip(self.velocity, self.accel, self.friction)]
        
        self.x += self.velocity[0] * delta_time * self.speed
        self.y += self.velocity[1] * delta_time * self.speed
        
        self.velocity = [v - min(v * f * delta_time, v, key = abs) for v, f in zip(self.velocity, self.friction)]
        

class EventHandler:
    def __init__(self, game):
        self.game = game # Game pointer
        self.cooldown = 0 # pour ralentir la vitesse du personnage, l'action d'avancer ne s'execute qu'une fois sur 2

    def didQuit(self):
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False


    def movePlayer(self, player, playerAnimations):
        keys = pygame.key.get_pressed()
        alreadyAnimated = False
        
        player_input = [0, 0]

        if keys[pygame.K_q]:
            playerAnimations.walk("l", player.velocity)
            alreadyAnimated = True
            
            if player.x-player.speed > 40: 
                player_input[0] -= 1
                
        if keys[pygame.K_d]:
            if not alreadyAnimated:
                playerAnimations.walk("r", player.velocity)
                alreadyAnimated = True
            if player.x+player.speed < MAP_SIZE - 39:
               player_input[0] += 1

        if keys[pygame.K_z]:
            if not alreadyAnimated:
                playerAnimations.walk("b", player.velocity)
                alreadyAnimated = True
            if player.y-player.speed > 23:
                player_input[1] -= 1

        if keys[pygame.K_s]:
            if not alreadyAnimated:
                playerAnimations.walk("f", player.velocity)
                alreadyAnimated = True
            if player.y+player.speed < MAP_SIZE - 22:
                player_input[1] += 1
                
            
        player.accel[0], player.accel[1] = player_input[0], player_input[1]
        
        if not (keys[pygame.K_z] or keys[pygame.K_q] or keys[pygame.K_s] or keys[pygame.K_d]):
            playerAnimations.idle()

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
        self.level = Level()
        self.tilemap = None
        
        if not pathlib.Path("save/level.dat").exists():
            self.tilemap = Tilemap()
            self.tilemap.generateMap()
            self.level.tilemap = self.tilemap
        else:
            self.load()
                        
        self.clock = pygame.time.Clock()
        self.player = Player(self.level.player_coords, self.screen)
        self.fps_counter = FPScounter(self.clock, self.screen, self.player)
        self.playerAnimations = PlayerAnimations(self.player)
        self.event_handler = EventHandler(self)
        self.running = True

    def load(self):
        with open("save/level.dat", "rb") as f:
            log("Loading level")
            self.level = pickle.load(f)
            self.tilemap = self.level.tilemap
            log("Level loaded")

    def save(self):
        with open("save/level.dat", "wb") as f:
            log("Saving level")
            self.level.player_coords = (self.player.x, self.player.y)
            pickle.dump(self.level, f)
            log("Level saved")

    def run(self):
        # Run until the user asks to quit

        while self.running:
            self.event_handler.didQuit()
            # Fill the background with white
            self.screen.fill((255, 255, 255))

            # Draw
            self.tilemap.render(self.screen, self.player)
            self.event_handler.movePlayer(self.player, self.playerAnimations)

            # fps
            self.clock.tick()
            self.fps_counter.display()
            self.event_handler.movePlayer(self.player, self.playerAnimations)
            self.player.move(1 / (self.clock.get_fps() + 0.00000000000001))
            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        self.save()
        pygame.quit()

    


if __name__ == "__main__":
    game = Game()
    game.run()
