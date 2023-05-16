from constants import *

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
        for i in range(500):
            for j in range(500):
                height = abs(noise((i / 2500, j / 2500))) * 255
                if  10 < height < 50 and self.searchAround((i,j), 10, [14]):
                    self.map[i][j] = self.randomStructure(self.randomStructure(self.random(self.random(4,3, 3), 10 , 10), [11,13], 3), [21,22,23,24,25],500) 
                else:
                
                    if height < 5:
                        self.map[i][j] = self.random(0, 1, 2)
                    elif height < 10:
                        self.map[i][j] = 2
                    elif height < 40:
                        if 20 < height < 25:
                            self.map[i][j] = self.randomStructure(self.random(4,3, 3), [15,28,27,16,17,18,19] , 500) # if self.random(2, 14, 2500) == 2 else 14 villages désactivés
                        else:
                            self.map[i][j] = self.random(3, 4, 4)

                    elif height < 60:
                        if 45 < height < 50:
                            self.map[i][j] = self.randomStructure(self.randomStructure(5, [6, 7, 8, 9], 5), [15,28,27,16,17,18,19], 500) # if self.random(2, 14, 2500) == 2 else 14 villages désactivés
                        else:
                            self.map[i][j] = self.randomStructure(5, [6, 7, 8, 9], 15)

                    elif height < 80:
                        self.map[i][j] = self.random(11, 29, 25)
                    else:
                        self.map[i][j] = self.random(12, 30, 2)

        log("Terrain Generated")


    def render(self, surface, player):
        # 32x32
        textures = []
        tile_entities = []
        for x in range(round(player.x - 44), round(player.x + 44)):
            for y in range(round(player.y - 26), round(player.y + 26)): # CLIPPING VALUES. TO CHANGE
                tile = self.map[x][y]
                
                if tile < 31:
                    if len(COLORS[tile]) == 3:
                        pygame.draw.rect(surface, COLORS[tile] , pygame.Rect(x * 32 - round(player.x * 32) + SCREEN_WIDTH // 2, y * 32 - round(player.y * 32) + SCREEN_HEIGHT // 2, 32, 32))

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
                            tile_entities.append((pygame.transform.scale(STRUCTURES[COLORS[tile].split(".")[0]][int(COLORS[tile].split(".")[1])], (128, 128)), (x * 32 - correction[0] - round(player.x * 32)  + (SCREEN_WIDTH // 2 ), y * 32 -correction[1]- round(player.y * 32)  + (SCREEN_HEIGHT // 2)))) # joueur toujours au millieu de l'écran, c'est le bg qui bouge                
                        else:
                            textures.append((pygame.transform.scale(STRUCTURES[COLORS[tile].split(".")[0]][int(COLORS[tile].split(".")[1])], (32, 32)), (x * 32  - round(player.x * 32)  + (SCREEN_WIDTH // 2 ), y * 32 - round(player.y * 32)  + (SCREEN_HEIGHT // 2)))) # joueur toujours au millieu de l'écran, c'est le bg qui bouge                
        for t in textures:
            surface.blit(t[0], t[1])
        for e in tile_entities:
            surface.blit(e[0], e[1])


