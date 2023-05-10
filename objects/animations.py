
import pygame, threading, math

def set_interval(func, sec):
   def func_wrapper():
       set_interval(func, sec) 
       func()  
   t = threading.Timer(sec, func_wrapper)
   t.start()
   return t



class PlayerAnimations:
    def __init__(self, player):
        self.skins = {
            "idle":[
                pygame.image.load("./resources/animations/player/idle/idle00.png")
            ],
            "walkf": [
                pygame.image.load("./resources/animations/player/walk/walkf0.png"),
                pygame.image.load("./resources/animations/player/walk/walkf1.png"),
                pygame.image.load("./resources/animations/player/walk/walkf2.png")
            ],   
            "walkb": [
                pygame.image.load("./resources/animations/player/walk/walkb0.png"),
                pygame.image.load("./resources/animations/player/walk/walkb1.png"),
                pygame.image.load("./resources/animations/player/walk/walkb2.png")
            ],
            "walkl": [
                pygame.image.load("./resources/animations/player/walk/walkl0.png"),
                pygame.image.load("./resources/animations/player/walk/walkl1.png"),
                pygame.image.load("./resources/animations/player/walk/walkl2.png")
            ],
            "walkr": [
                pygame.image.load("./resources/animations/player/walk/walkr0.png"),
                pygame.image.load("./resources/animations/player/walk/walkr1.png"),
                pygame.image.load("./resources/animations/player/walk/walkr2.png")
            ],
            "attackl": [
                pygame.image.load("./resources/animations/player/attack/attackl0.png"),
                pygame.image.load("./resources/animations/player/attack/attackl1.png"),
                pygame.image.load("./resources/animations/player/attack/attackl2.png"),
                pygame.image.load("./resources/animations/player/attack/attackl3.png")
            ],
            "attackr": [
                pygame.image.load("./resources/animations/player/attack/attackr0.png"),
                pygame.image.load("./resources/animations/player/attack/attackr1.png"),
                pygame.image.load("./resources/animations/player/attack/attackr2.png"),
                pygame.image.load("./resources/animations/player/attack/attackr3.png")
            ],
            "attacksr": [
                pygame.image.load("./resources/animations/player/attack/attacksr0.png"),
                pygame.image.load("./resources/animations/player/attack/attacksr1.png"),
                pygame.image.load("./resources/animations/player/attack/attacksr2.png"),
                pygame.image.load("./resources/animations/player/attack/attacksr3.png")
            ],
            "attacksl": [
                pygame.image.load("./resources/animations/player/attack/attacksl0.png"),
                pygame.image.load("./resources/animations/player/attack/attacksl1.png"),
                pygame.image.load("./resources/animations/player/attack/attacksl2.png"),
                pygame.image.load("./resources/animations/player/attack/attacksl3.png")
            ],
        }  
        self.STATUS = {
            "idle": 0,
            "walkf": 1,
            "walkb": 2,
            "walkr": 3,
            "walkl": 4,
            "attackr": 5,
            "attackl": 6
        }
        self.player = player
        self.ticks = [0, self.STATUS["idle"]]


    def changeTicks(self, status):
        if self.ticks[1] != self.STATUS[status]:
            self.ticks = [0, self.STATUS[status]]


    def animationPhases(self, path, duration, velocity=[0,0]): 
        velocityNorm = math.sqrt(velocity[0]**2 + velocity[1]**2)
        numberOfPhases = len(duration) 
        self.ticks[0] += velocityNorm +1 *3

        for d in range(numberOfPhases):
            if d == numberOfPhases-1 and duration[d] <= self.ticks[0]//25:
                self.ticks[0] = 0
                self.player.render(self.skins[path][0])
                return 
            if self.ticks[0]//25 < duration[d]:
                self.player.render(self.skins[path][d])
                return


    def idle(self):
        self.changeTicks("idle")
        self.animationPhases("idle", [8]) #, 10, 18, 19])

    def walk(self, direction, velocity):
        self.changeTicks(f"walk{direction}")
        self.animationPhases("walk"+direction, [1, 6, 11], velocity)

    def attack(self, direction):
        self.changeTicks(f"attack{direction}")
        self.animationPhases("attack"+direction, [1, 2, 3, 4])
        
        
        
class EntitysAnimations:
    def __init__(self, player):
        self.skins = {
            
            "idle": [
                pygame.image.load("./resources/animations/entities/sime/slimel.png"),
                pygame.image.load("./resources/animations/entities/sime/slimer.png")
            ],
            "attackr":[
                pygame.image.load("./resources/animations/entities/sime/slimeattackr0.png"),
                pygame.image.load("./resources/animations/entities/sime/slimeattackr1.png")
            ],
            "attackr":[
                pygame.image.load("./resources/animations/entities/sime/slimeattackl0.png"),
                pygame.image.load("./resources/animations/entities/sime/slimeattackl1.png")
            ],
        }  
        self.STATUS = {
            "idle": 0,
            "attackr": 1,
            "attackl": 2
        }
        self.player = player
        self.ticks = [0, self.STATUS["idle"]]


    def changeTicks(self, status):
        if self.ticks[1] != self.STATUS[status]:
            self.ticks = [0, self.STATUS[status]]


    def animationPhases(self, path, duration, velocity=[0,0]): 
        velocityNorm = math.sqrt(velocity[0]**2 + velocity[1]**2)
        numberOfPhases = len(duration) 
        self.ticks[0] += velocityNorm +1 *3

        for d in range(numberOfPhases):
            if d == numberOfPhases-1 and duration[d] <= self.ticks[0]//25:
                self.ticks[0] = 0
                self.player.render(self.skins[path][0])
                return 
            if self.ticks[0]//25 < duration[d]:
                self.player.render(self.skins[path][d])
                return


    def idle(self):
        self.changeTicks("idle")
        self.animationPhases("idle", [8]) #, 10, 18, 19])

    def walk(self, direction, velocity):
        self.changeTicks(f"walk{direction}")
        self.animationPhases("walk"+direction, [1, 6, 11], velocity)

    def attack(self, direction):
        self.changeTicks(f"attack{direction}")
        self.animationPhases("attack"+direction, [1, 2, 3, 4])

