from constants import *
from perlin_noise import PerlinNoise
from objects.utils import log
import random

class Tilemap:
    """Map generator and map rendering. Used Perlin Noise algorithm"""
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

    def generateMap(self):
        self.map = [[0 for j in range(MAP_SIZE)] for i in range(MAP_SIZE)] # First launch
        noise = PerlinNoise(octaves = 50, seed = random.randint(400, 600))

        log("Generating Terrain")
        
        for i in range(500):
            for j in range(500):
                height = abs(noise((i / 2500, j / 2500))) * 255 # Using this algorithm, all is about the theorical height of the map (between 0 and 100)
                
                if height < 5:
                    self.map[i][j] = self.random(0, 1, 2) # generate water
                elif height < 10:
                    self.map[i][j] = 2 # generate sand 
                elif height < 40:
                    if 30 < height < 40:
                        self.map[i][j] = self.randomStructure(self.randomStructure(self.random(4,3, 3), [15,28,27,16,17,18,19,21,22,23,25] , 1000), [21,22,23,25], 2500) # Multiple functional expression: generate random house -> then generate random trees and rocks -> then generate grass
                    else:
                        self.map[i][j] = self.random(3, 4, 4) # generate different grass types

                elif height < 60:
                    if 40 < height < 45:
                        self.map[i][j] = self.randomStructure(self.randomStructure(self.randomStructure(5, [6, 7, 8, 9], 5), [15,28,27,16,17,18,19], 1000), [21,22,23,25], 2500) # Multiple functional expression: generate random house -> then generate random trees and rocks -> then generate grass
                    else:
                        self.map[i][j] = self.randomStructure(5, [6, 7, 8, 9], 15) # generate different grass types

                elif height < 80:
                    self.map[i][j] = self.random(11, 29, 25) # generate mountains
                else:
                    self.map[i][j] = self.random(12, 30, 2) # generate snow in top of mountains

        log("Terrain Generated")


    def render(self, surface, player):
        # 32x32
        textures = []
        tile_entities = []
        for x in range(round(player.x - 44), round(player.x + 44)):
            for y in range(round(player.y - 26), round(player.y + 26)): # CLIPPING VALUES.
                tile = self.map[x][y]
                
                if tile < 31:
                    if len(COLORS[tile]) == 3:
                        # render rgb tiles
                        pygame.draw.rect(surface, COLORS[tile] , pygame.Rect(x * 32 - round(player.x * 32) + SCREEN_WIDTH // 2, y * 32 - round(player.y * 32) + SCREEN_HEIGHT // 2, 32, 32))

                    else:
                        # render images tiles
                        correction = [0, 0]
                        size = 0
                        name = COLORS[tile].split(".")[0]
                        idx = int(COLORS[tile].split(".")[1])
                        if name in ["house", "tree", "rocks"]:
                            if name == "house":
                                correction = [90, 128]
                                size = 256
                            elif name == "tree":
                                correction = [40, 40]
                                size = 128
                            elif name == "rocks":
                                size = 128
                                if idx == 2:
                                    correction = [45, 45]
                                elif idx == 1:
                                    correction = [45, 95]
                            tile_entities.append((pygame.transform.scale(STRUCTURES[COLORS[tile].split(".")[0]][int(COLORS[tile].split(".")[1])], (size, size)), (x * 32 - correction[0] - round(player.x * 32)  + (SCREEN_WIDTH // 2 ), y * 32 -correction[1]- round(player.y * 32)  + (SCREEN_HEIGHT // 2)))) # joueur toujours au millieu de l'écran, c'est le bg qui bouge                
                        else:
                            textures.append((pygame.transform.scale(STRUCTURES[COLORS[tile].split(".")[0]][int(COLORS[tile].split(".")[1])], (32, 32)), (x * 32  - round(player.x * 32)  + (SCREEN_WIDTH // 2 ), y * 32 - round(player.y * 32)  + (SCREEN_HEIGHT // 2)))) # joueur toujours au millieu de l'écran, c'est le bg qui bouge                
        for t in textures:
            surface.blit(t[0], t[1]) # render grounded tiles before special structures tiles
        for e in tile_entities:
            surface.blit(e[0], e[1])


