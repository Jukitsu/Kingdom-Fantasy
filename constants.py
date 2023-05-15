import pygame

MAP_SIZE = 1000
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720

FRICTION = ( 16,  16,  16)

ENDGAME_COORDINATES = (100, 100)

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
    11:"mountains.0",
    12:"snow.0",
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
    28: "rocks.2",
    29: "mountains.1",
    30: (235,244,251)
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
    "mountains": [
        pygame.image.load("./resources/textures/stone_mountain0.png"),
        pygame.image.load("./resources/textures/stone_mountain2.png")
    ],
    "snow": [
        pygame.image.load("./resources/textures/snow.png"),
    ],
}

PNJ = [
    {
        "skin":  "tuto",
        "text": ["Bien le bonjour jeune aventurier!", "Pour te déplacer tu dois utiliser tes touches ZQSD.","Prends garde à toi, ce monde regorge de monstres!",
                 "Tu dois utiliser ton clic gauche pour te défendre des slimes!", "Je ne reste pas plus longtemps ! Bon jeu à toi !"],
        "position": (100, 100)
    }
]

COMPASS_POSITION = (50, 50)