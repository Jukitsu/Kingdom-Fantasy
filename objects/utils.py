import pygame, math

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
    def __init__(self, polePos, position, screen):
        self.polePos = polePos
        self.indicator = pygame.transform.scale(pygame.image.load('./resources/textures/indicator.png'), (128, 128))
        self.position = position
        self.screen = screen
    def getAngleFromCoordinates(self, coords):
        radians = math.atan2(coords[1], coords[0])
        angle_deg = math.degrees(radians)
        return (-(angle_deg -270) + 360) % 360

    def render(self, objPos):

        
        direction = (self.polePos[0] - objPos[0], self.polePos[1] - objPos[1]) # x, y
        rect = self.indicator.get_rect()
        rotated_image = pygame.Surface(rect.size, pygame.SRCALPHA)
        center = rect.center 

        rotated_image = pygame.transform.rotate(self.indicator, self.getAngleFromCoordinates(direction))
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = center

        # background
        self.screen.blit(pygame.transform.scale(pygame.image.load('./resources/textures/compass.png'), (128, 128)), (-0.5, 5))
        # indicator
        indicator = self.screen.blit(rotated_image, rotated_rect)
