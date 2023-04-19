
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
        }  
        self.STATUS = {
            "idle": 0,
            "walkf": 1,
            "walkb": 2,
            "walkr": 3,
            "walkl": 4
        }
        self.player = player
        self.ticks = [0, self.STATUS["idle"]]


    def changeTicks(self, status):
        if self.ticks[1] != self.STATUS[status]:
            self.ticks = [0, self.STATUS[status]]


    def animationPhases(self, path, duration, velocity=[0,0]): 
        velocityNorm = math.sqrt(velocity[0]**2 + velocity[1]**2)
        numberOfPhases = len(duration) 
        self.ticks[0] += velocityNorm +1

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
        self.animationPhases("walk"+direction, [1, 4, 7], velocity)
