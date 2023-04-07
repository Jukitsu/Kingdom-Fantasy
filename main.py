import pygame, random, time, threading
from animations import PlayerAnimations

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
        for i in range(MAP_SIZE):
            for j in range(200):
                self.map[i][j] = random.randint(0, 2)



    def render(self, surface, player_x, player_y):
        # 32x32
        for x, c in enumerate(self.map[player_x:player_x+40]): # bouge en fonction du joueur
            for y, tile in enumerate(c[player_y:player_y+23]):
                pygame.draw.rect(surface, COLORS[tile], pygame.Rect(x * 32, y * 32, 32, 32))

class FPS_counter:
    def __init__(self, clock, screen):
        self.clock = clock
        self.screen = screen

    def display(self):
        font = pygame.font.SysFont(None, 30)
        img = font.render(str(round(self.clock.get_fps())), True, (0, 0, 0))
        self.screen.blit(img, (2, 2))

class Player:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.speed = 1
        self.screen = screen

    def render(self, skin="./resources/animations/player/idle/idle00.png"):
        img = pygame.transform.scale(pygame.image.load(skin), (128, 128))
        self.screen.blit(img, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)) # joueur toujours au millieu de l'écran, c'est le bg qui bouge

class EventHandler:
    def __init__(self):
        self.cooldown = 0 # pour ralentir la vitesse du personnage, l'action d'avancer ne s'execute qu'une fois sur 2

    def didQuit(self):
        # Did the user click the window close button?
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    def ralentir(self):
        self.cooldown += 1
        if self.cooldown == 2:
            self.cooldown = 0
            return False
        return True

    def movePlayer(self, player, playerAnimations):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]: # verif pour pas que le personnage ne sorte de la map
            playerAnimations.walk("b")
            if player.y-player.speed > 20 and self.ralentir():
                player.y -= player.speed 
        if keys[pygame.K_q]:
            if player.x-player.speed > 12 and self.ralentir(): 
                player.x -= player.speed
        if keys[pygame.K_s]:
            playerAnimations.walk("f")
            if player.y+player.speed < MAP_SIZE-20 and self.ralentir():
                player.y += player.speed
        if keys[pygame.K_d]:
            if player.x+player.speed < MAP_SIZE-12 and self.ralentir():
                player.x += player.speed
        
        if not (keys[pygame.K_z] or keys[pygame.K_q] or keys[pygame.K_s] or keys[pygame.K_d]):
            playerAnimations.idle()

            
            
class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
        self.tilemap = Tilemap()
        self.clock = pygame.time.Clock()
        self.fps_counter = FPS_counter(self.clock, self.screen)
        self.player = Player(10, 10, self.screen)
        self.playerAnimations = PlayerAnimations(self.player)
        self.EventHandler = EventHandler()

    def run(self):
        # Run until the user asks to quit
        running = True

        while running:
            self.EventHandler.didQuit()
            time.sleep(0.01)
            # Fill the background with white
            self.screen.fill((255, 255, 255))

            # Draw
            self.tilemap.render(self.screen, self.player.x, self.player.y)

            # fps
            self.clock.tick()
            self.fps_counter.display()
            self.EventHandler.movePlayer(self.player, self.playerAnimations)
            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()