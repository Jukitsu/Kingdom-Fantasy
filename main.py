import pygame, random, time, threading
from objects.animations import PlayerAnimations
from perlin_noise import PerlinNoise
import pathlib, cv2, pickle, math # cv2 = opencv-python


from objects.player import Player
from objects.entity import Entity
from objects.utils import FPScounter, log
from objects.animations import PlayerAnimations

StartTime=time.time()
MAP_SIZE = 1000
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720

FRICTION = ( 16,  16,  16)

COLORS = {
    0: (0,197,214), # Water
    1: "water.0", # Water texture
    2: "beach.0", # Beach
    3: (139,195,74), # Plain
    4: "grass.1", # Plain texture
    5: (69,193,0), # Plains higher
    6: "grass.0", # Plain texture
    7: "grass.2",
    8: "grass.3",
    9: "grass.4",
    10: (85, 86, 87), # rocks
    11:(139, 137, 137), # Mountains
    12: (255, 250, 250), # Snowy Mountains,
    13: (100, 100, 100), # villages
    14: (100, 100, 100), # village center
    15: "tree.0",
    16: "tree.1",
    17: "tree.2",
    18: "tree.3",
    19: "tree.4",
    20: "tree.5",
    21: "house.0",
    22: "house.1",
    23: "house.2",
    24: "house.3",
    25: "house.4",
    26: "rocks.0",
    27: "rocks.1",
    28: "rocks.2"
}

STRUCTURES = {
    "tree": [
    pygame.image.load("./resources/textures/tree0.png"),
    pygame.image.load("./resources/textures/tree1.png"),
    pygame.image.load("./resources/textures/tree2.png"),
    pygame.image.load("./resources/textures/tree3.png"),
    pygame.image.load("./resources/textures/tree4.png"),
    pygame.image.load("./resources/textures/tree5.png"),
    ],
    "house":[
        pygame.image.load("./resources/textures/house0.png"),
        pygame.image.load("./resources/textures/house1.png"),
        pygame.image.load("./resources/textures/house2.png"),
        pygame.image.load("./resources/textures/house3.png"),
        pygame.image.load("./resources/textures/house4.png")
    ],
    "grass":[
        pygame.image.load("./resources/textures/grass0.png"),
        pygame.image.load("./resources/textures/grass1.png"),
        pygame.image.load("./resources/textures/grass2.png"),
        pygame.image.load("./resources/textures/grass3.png"),
        pygame.image.load("./resources/textures/grass4.png"),
    ],
    "water":[
        pygame.image.load("./resources/textures/water0.png")
    ],
    "rocks": [
        pygame.image.load("./resources/textures/chemin.png"),
        pygame.image.load("./resources/textures/rocks0.png"),
        pygame.image.load("./resources/textures/rocks1.png")
    ],
    "beach": [
        pygame.image.load("./resources/textures/sand.png")
    ],
}

class Level:
    def __init__(self):
        self.tilemap = None
        self.player_coords = (0, 0)
        self.entities = []
        
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
        if radius < coords[0] < MAP_SIZE- radius and radius < coords[1] < MAP_SIZE-radius:
            for i in range(coords[0] - radius, coords[0] + radius):
                for j in range(coords[1] - radius, coords[1] + radius):
                    if self.map[i][j] in type:
                        return True 
            return False
    def generateMap(self): # fonction a modifier c'est pour tester les couleurs
        self.map = [[0 for j in range(MAP_SIZE)] for i in range(MAP_SIZE)] # First launch
        noise = PerlinNoise(octaves = 50, seed = 500)

        log("Generating Terrain")
        # Generating Terrain
        for i in range(100):
            for j in range(100):
                height = abs(noise((i / 2500, j / 2500))) * 255
                if  10 < height < 50 and self.searchAround((i,j), 10, [14]):
                    self.map[i][j] = self.randomStructure(self.randomStructure(10, [11,13], 3), [21,22,23,24,25],500) 
                else:
                
                    if height < 5:
                        self.map[i][j] = self.random(0, 1, 2)
                    elif height < 10:
                        self.map[i][j] = 2
                    elif height < 40:
                        if 20 < height < 25:
                            self.map[i][j] = self.randomStructure(self.random(4,3, 3), [15,28,27,16,17,18,19] , 500) if self.random(2, 14, 2500) == 2 else 14
                        else:
                            self.map[i][j] = self.random(4, 3, 3)

                    elif height < 60:
                        if 45 < height < 50:
                            self.map[i][j] = self.randomStructure(self.randomStructure(5, [6, 7, 8, 9], 5), [15,28,27,16,17,18,19], 500) if self.random(2, 14, 2500) == 2 else 14 
                        else:
                            self.map[i][j] = self.randomStructure(5, [6, 7, 8, 9], 5)

                    elif height < 80:
                        self.map[i][j] = 11
                    else:
                        self.map[i][j] = 12

        log("Terrain Generated")


    def render(self, surface, player):
        # 32x32
        textures = []
        entities = []
        for x in range(round(player.x - 44), round(player.x + 44)):
            for y in range(round(player.y - 26), round(player.y + 26)): # CLIPPING VALUES. TO CHANGE
                tile = self.map[x][y]
                if tile < 28 :
                    if tile < 28 and len(COLORS[tile]) == 3:
                        pygame.draw.rect(surface, COLORS[tile] if (x != round(player.x) or y != round(player.y)) else (255, 0, 0), pygame.Rect(x * 32 - round(player.x * 32) + SCREEN_WIDTH // 2, y * 32 - round(player.y * 32) + SCREEN_HEIGHT // 2, 32, 32))
                    else:
                        correction = [0, 0]
                        name = COLORS[tile].split(".")[0]
                        idx = int(COLORS[tile].split(".")[1])
                        if name in ["house", "tree", "rocks"]:
                            if name == "house":
                                correction = [90, 128]
                            elif name == "tree":
                                correction = [40, 40]
                            elif name == "rocks":
                                if idx == 2:
                                    correction = [45, 45]
                                elif idx == 1:
                                    correction = [45, 95]
                            entities.append((pygame.transform.scale(STRUCTURES[COLORS[tile].split(".")[0]][int(COLORS[tile].split(".")[1])], (128, 128)), (x * 32 - correction[0] - round(player.x * 32)  + (SCREEN_WIDTH // 2 ), y * 32 -correction[1]- round(player.y * 32)  + (SCREEN_HEIGHT // 2)))) # joueur toujours au millieu de l'écran, c'est le bg qui bouge                
                        else:
                            textures.append((pygame.transform.scale(STRUCTURES[COLORS[tile].split(".")[0]][int(COLORS[tile].split(".")[1])], (32, 32)), (x * 32  - round(player.x * 32)  + (SCREEN_WIDTH // 2 ), y * 32 - round(player.y * 32)  + (SCREEN_HEIGHT // 2)))) # joueur toujours au millieu de l'écran, c'est le bg qui bouge                
        for t in textures:
            surface.blit(t[0], t[1])
        for e in entities:
            surface.blit(e[0], e[1])


class ChatBox:
    def __init__(self, text):
        self.text = text
    def render(self, screen):
        # chatbox
        chat = pygame.image.load("./resources/textures/parchemin.png")
        self.screen.blit(pygame.transform.scale(chat), (0, 0))
        # text
        font = pygame.font.Font(None, 32)
        text = font.render(self.text, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, textRect)
        
        

class EventHandler:
    def __init__(self, game):
        self.game = game # Game pointer

    def didQuit(self):
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
    def dist(self, A, B):
        return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)
    def playerActions(self, player, level):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_e]:
            for e in level.entities:
                if self.dist((e.x, e.y), (player.x, player.y)) <= 20:
                    ChatBox(e.chat[0]).render()
    def movePlayer(self, player, playerAnimations, level):
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
            toAttack = False
            for e in level.entities:
                if self.dist((e.x, e.y), (player.x, player.y)) <= 5:
                    toAttack = e
            if toAttack:
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
        # self.level.entities.append(Entity((40, 23), self.screen))
        self.fps_counter = FPScounter(self.clock, self.screen, self.player)
        self.playerAnimations = PlayerAnimations(self.player)
        self.loading = False
        self.running = True

    
    def load(self):
        with open("save/level.dat", "rb") as f:
            log("Loading level")
            self.level = pickle.load(f)
            self.tilemap = self.level.tilemap
            self.level.player_coords = self.level.player_coords
            log("Level loaded")

    def save(self):
        with open("save/level.dat", "wb") as f:
            log("Saving level")
            self.level.entities = []
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
            self.event_handler.playerActions(self.player,self.level)
            self.event_handler.movePlayer(self.player, self.playerAnimations, self.level)

            # fps
            self.clock.tick()
            self.fps_counter.display()
            self.player.move(1 / (self.clock.get_fps() + 0.00000000000001))
            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        self.save()
        pygame.quit()

    


if __name__ == "__main__":
    game = Game()
    game.run()
