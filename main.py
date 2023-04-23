import pygame, random, time, threading
from objects.animations import PlayerAnimations
from perlin_noise import PerlinNoise
import pathlib, cv2, pickle


from objects.player import Player
from objects.utils import FPScounter, log
from objects.animations import PlayerAnimations

StartTime=time.time()
MAP_SIZE = 6400
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720

FRICTION = ( 16,  16,  16)

COLORS = {
    0: (65,105,225), # Water
    1: (238, 214, 175), # Beach
    2: (34,139,34), # Plains
    3: (85, 86, 87), # rocks
    4: (34, 107, 34), # Plains higher
    5: (139, 137, 137), # Mountains
    6: (255, 250, 250), # Snowy Mountains,
    7: (100, 100, 100), # villages
    8: "tree.0",
    9: "tree.1",
    10: "tree.2",
    11: "tree.3",
    12: "tree.4",
    13: "tree.5",
    14: "house.0",
    15: "house.1",
    16: "house.2",
    17: "house.3",
    18: (100, 100, 100) # village center
}

STRUCTURES = {
    "tree": [
    pygame.image.load("./resources/assets/tree0.png"),
    pygame.image.load("./resources/assets/tree1.png"),
    pygame.image.load("./resources/assets/tree2.png"),
    pygame.image.load("./resources/assets/tree3.png"),
    pygame.image.load("./resources/assets/tree4.png"),
    pygame.image.load("./resources/assets/tree5.png"),
    ],
    "house":[
        pygame.image.load("./resources/assets/house0.png"),
        pygame.image.load("./resources/assets/house1.png"),
        pygame.image.load("./resources/assets/house2.png"),
        pygame.image.load("./resources/assets/house3.png"),
        pygame.image.load("./resources/assets/house4.png")
    ]
}

class Level:
    def __init__(self):
        self.tilemap = None
        self.player_coords = (0, 0)
        
class Tilemap:
    def __init__(self):
        self.map = []
        self.view_offset = [0, 0]
    def random(self, default, structure, chance):
        return structure if random.randint(1, chance) == chance else default
    def randomStructure(self, default, StructureArray, chance):
        for i in range(len(StructureArray)):
            if self.random(default, StructureArray[i], chance) == StructureArray[i]:
                return StructureArray[i]
        return default
    
    def searchAround(self, coords, radius, type):
        for i in range(coords[0] - radius, coords[0] + radius):
            for j in range(coords[1] - radius, coords[1] + radius):
                if self.map[i][j] in type:
                    log(True)
                    return True 
        return False
    def generateMap(self): # fonction a modifier c'est pour tester les couleurs
        self.map = [[0 for j in range(MAP_SIZE//4)] for i in range(MAP_SIZE//4)] # First launch
        noise = PerlinNoise(octaves = 50, seed = 500)

        log("Generating Terrain")
        # Generating Terrain
        for i in range(500):
            for j in range(500):
                height = abs(noise((i / MAP_SIZE, j / MAP_SIZE))) * 255

                if  10 < height < 50 and self.searchAround((i,j), 25, [18]):
                    self.map[i][j] = self.randomStructure(self.random(7, 3, 3), [14, 15, 16, 17], 10 if not self.searchAround((i,j), 10, [14, 15, 16, 17]) else 1000)
                else:
                
                    if height < 5:
                        self.map[i][j] = 0
                    elif height < 7:
                        self.map[i][j] = 1
                    elif height < 40:
                        if 20 < height < 25:
                            self.map[i][j] = self.randomStructure(2, [ 8, 9, 10, 11, 12], 1000) if self.random(2, 18, 2500) == 2 else 18
                        else:
                            self.map[i][j] = self.random(2, 3, 400)

                    elif height < 60:
                        if 45 < height < 50:
                            self.map[i][j] = self.randomStructure(4, [7, 8, 9, 10, 11, 12], 2500) if self.random(2, 18, 2500) == 2 else 18
                        else:
                            self.map[i][j] = self.random(4, 3, 100)

                    elif height < 80:
                        self.map[i][j] = 5
                    else:
                        self.map[i][j] = 6

        log("Terrain Generated")


    def render(self, surface, player):
        # 32x32
        entities = []
        for x in range(round(player.x - 44), round(player.x + 44)):
            for y in range(round(player.y - 26), round(player.y + 26)): # CLIPPING VALUES. TO CHANGE
                tile = self.map[x][y]
                if tile < 8 or tile == 18:
                    pygame.draw.rect(surface, COLORS[tile] if (x != round(player.x) or y != round(player.y)) else (255, 0, 0), pygame.Rect(x * 16 - round(player.x * 16) + SCREEN_WIDTH // 2, y * 16 - round(player.y * 16) + SCREEN_HEIGHT // 2, 32, 32))
                else:
                    pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(x * 16 - round(player.x * 16) + SCREEN_WIDTH // 2, y * 16 - round(player.y * 16) + SCREEN_HEIGHT // 2, 32, 32))
                    entities.append((pygame.transform.scale(STRUCTURES[COLORS[tile].split(".")[0]][int(COLORS[tile].split(".")[1])], (128, 128)), (x * 16 - 45 - round(player.x * 16)  + (SCREEN_WIDTH // 2 ), y * 16 -64 - round(player.y * 16)  + (SCREEN_HEIGHT // 2)))) # joueur toujours au millieu de l'écran, c'est le bg qui bouge                
        for e in entities:
            surface.blit(e[0], e[1])

class Entity:
    def __init__(self, coords, screen):
        self.x, self.y = coords
        self.velocity = [0, 0]
        self.accel = [0, 0]
        self.friction = FRICTION
        self.speed = 16
        self.screen = screen
        self.TYPE = {
            0: "mob",
            1: "pnj"
        }

class EventHandler:
    def __init__(self, game):
        self.game = game # Game pointer

    def didQuit(self):
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False


    def movePlayer(self, player, playerAnimations):
        if player.isAttacking[0]: 
            if player.isAttacking[1] == 75:
                player.isAttacking = [False, 0, "r"]
            else:
                player.isAttacking[1] += 1
                playerAnimations.attack(player.isAttacking[2])
                return
        keys = pygame.key.get_pressed()
        clicks = pygame.mouse.get_pressed(num_buttons=3)
        # keyboard events managment
        keyPriority = [
            (pygame.K_q, "l", (0, -1), player.x > 41),
            (pygame.K_d, "r", (0, 1), player.x < MAP_SIZE - 40),
            (pygame.K_z, "b", (1, -1), player.y > 24),
            (pygame.K_s, "f", (1, 1), player.y < MAP_SIZE - 23)
        ]

        player_input = [0, 0]
        alreadyAnimated = False

        for k in keyPriority:
            # animation de marcher du personnage 
            if keys[k[0]]:
                if not alreadyAnimated:
                    playerAnimations.walk(k[1], player.velocity)
                    alreadyAnimated = True
                
                if k[3]:
                    player_input[k[2][0]] += k[2][1]

        player.accel[0], player.accel[1] = player_input[0], player_input[1]

        # mouse events managment
        if clicks[0]:
            direction = "l" if player_input[0] <= -1 else "r"
            player.isAttacking[0], player.isAttacking[2]  = True, direction
            playerAnimations.attack(direction)
            alreadyAnimated = False
            player.accel = [0, 0]
        if not alreadyAnimated:
            playerAnimations.idle() # si l'animation de marcher ne s'est pas déclenché, idle

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = None
        self.level = Level()
        self.tilemap = None
        self.loading = True
        self.clock = pygame.time.Clock()
        self.event_handler = EventHandler(self)

        if not pathlib.Path("save/level.dat").exists():
            self.loadingText()
            self.tilemap = Tilemap()
            self.tilemap.generateMap()
            self.level.tilemap = self.tilemap
            # self.cinematique()

        else:
            self.load()
            
                        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
        self.player = Player(self.level.player_coords, self.screen, self.tilemap, FRICTION, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fps_counter = FPScounter(self.clock, self.screen, self.player)
        self.playerAnimations = PlayerAnimations(self.player)
        self.loading = False
        self.running = True

    
    def load(self):
        with open("save/level.dat", "rb") as f:
            log("Loading level")
            self.level = pickle.load(f)
            self.tilemap = self.level.tilemap
            self.level.player_coords = (100, 100)
            log("Level loaded")

    def save(self):
        with open("save/level.dat", "wb") as f:
            log("Saving level")
            self.level.player_coords = (self.player.x, self.player.y)
            pickle.dump(self.level, f)
            log("Level saved")

    def loadingText(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
        font = pygame.font.Font(None, 32)
        text = font.render('Chargement...', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, textRect)
        pygame.display.flip()

    def cinematique(self):
        video = cv2.VideoCapture("./resources/video/Annim_nuages_sans_narration.mp4")
        success, video_image = video.read()
        fps = video.get(cv2.CAP_PROP_FPS)
        self.screen = pygame.display.set_mode(video_image.shape[1::-1], 0)
        
        soundObj = pygame.mixer.Sound('./resources/video/piste_audio.mp3')
        soundObj.play()
        while self.loading:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loading = False

            success, video_image = video.read()
            if success:
                video_surf = pygame.image.frombuffer(
                    video_image.tobytes(), video_image.shape[1::-1], "BGR")
            else:
                self.loading = False
            self.screen.blit(video_surf, (0, 0))
            pygame.display.flip()

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
