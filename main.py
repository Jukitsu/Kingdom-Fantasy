import pygame, random, time, threading
from animations import PlayerAnimations
from perlin_noise import PerlinNoise
import pathlib
import pickle

StartTime=time.time()
MAP_SIZE = 6400
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720

COLORS = {
    0: (0, 0, 255), # Water
    1: (0, 255, 0), # Plains
    2: (160, 160, 160) # Mountains
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
                else:
                    self.map[i][j] = 2
        log("Terrain Generated")


    def render(self, surface, player_x, player_y):
        # 32x32
        for x, c in enumerate(self.map[player_x: player_x + 40]): # bouge en fonction du joueur. 40 = 1280 / 32, 23 = 720 / 32
            for y, tile in enumerate(c[player_y: player_y + 23]):
                pygame.draw.rect(surface, COLORS[tile], pygame.Rect(x * 32, y * 32, 32, 32))

class FPScounter:
    def __init__(self, clock, screen, player):
        self.clock = clock
        self.screen = screen
        self.player = player

    def display(self):
        font = pygame.font.SysFont(None, 30)
        img = font.render(f"{round(self.clock.get_fps())}, X: {self.player.x}, Y: {self.player.y}", True, (0, 0, 0))
        self.screen.blit(img, (2, 2))

class Player:
    def __init__(self, coords, screen):
        self.x, self.y = coords
        self.speed = 1
        self.screen = screen

    def render(self, skin="./resources/animations/player/idle/idle00.png"):
        img = pygame.transform.scale(pygame.image.load(skin), (128, 128))
        self.screen.blit(img, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)) # joueur toujours au millieu de l'écran, c'est le bg qui bouge

class EventHandler:
    def __init__(self, game):
        self.game = game # Game pointer
        self.cooldown = 0 # pour ralentir la vitesse du personnage, l'action d'avancer ne s'execute qu'une fois sur 2

    def didQuit(self):
        # Did the user click the window close button?
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False

    def ralentir(self):
        self.cooldown += 1
        if self.cooldown == 20:
            self.cooldown = 0
            return True
        return False

    def movePlayer(self, player, playerAnimations):
        keys = pygame.key.get_pressed()
        alreadyAnimated = False

        if keys[pygame.K_q]:
            playerAnimations.walk("l")
            alreadyAnimated = True
            if player.x-player.speed > 0 and self.ralentir(): 
                player.x -= player.speed
        if keys[pygame.K_d]:
            if not alreadyAnimated:
                playerAnimations.walk("r")
                alreadyAnimated = True
            if player.x+player.speed < MAP_SIZE+1 and self.ralentir():
                player.x += player.speed

        if keys[pygame.K_z]:
            if not alreadyAnimated:
                playerAnimations.walk("b")
                alreadyAnimated = True
            if player.y-player.speed > 0 and self.ralentir():
                player.y -= player.speed 

        if keys[pygame.K_s]:
            if not alreadyAnimated:
                playerAnimations.walk("f")
                alreadyAnimated = True
            if player.y+player.speed < MAP_SIZE+1 and self.ralentir():
                player.y += player.speed
        
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
            self.tilemap.render(self.screen, self.player.x, self.player.y)
            self.event_handler.movePlayer(self.player, self.playerAnimations)

            # fps
            self.clock.tick()
            self.fps_counter.display()
            self.event_handler.movePlayer(self.player, self.playerAnimations)
            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        self.save()
        pygame.quit()

    


if __name__ == "__main__":
    game = Game()
    game.run()
