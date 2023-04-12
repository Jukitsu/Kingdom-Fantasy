
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
                self.player.render(path + str(0) + ".png")
                return 
            if self.ticks[0]//25 < duration[d]:
                self.player.render(path + str(d) + ".png")
                return

    def idle(self):
        self.changeTicks("idle")
        self.animationPhases("./resources/animations/player/idle/idle0", [8, 10, 18, 19])

    def walk(self, direction, velocity):
        self.changeTicks("walk"+direction)
        self.animationPhases("./resources/animations/player/walk/walk"+direction, [8, 16, 17] if direction == "b" or direction == "f" else [6, 12, 18, 22], velocity)
