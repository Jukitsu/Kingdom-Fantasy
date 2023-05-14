import pygame

def log(*args, **kw): # Debug
    print(*args, **kw)

class FPScounter:
    def __init__(self, clock, screen, player):
        self.clock = clock
        self.screen = screen
        self.player = player

    def display(self):
        font = pygame.font.SysFont(None, 30)
        img = font.render(f"{round(self.clock.get_fps())}, X: {round(self.player.x, 2)}, Y: {round(self.player.y, 2)}", True, (0, 0, 0))
        self.screen.blit(img, (2, 2))

class Compass:
    def __init__(self, objPos, polePos):
        self.objPos = objPos
        self.polePos = polePos

    def render(self, screen):
        direction = (self.polePos[0] - objPos[0], self.polePos[1] - objPos[1])

        pygame.draw.line(screen, BLACK, (self.objPos[0], objPos[1]), (objPos[0] + direction[0], objPos[1] + direction[1]))
