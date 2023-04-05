import pygame

MAP_SIZE = 6400
class Tilemap:
    def __init__(self):
        self.map = [[0 for i in range(MAP_SIZE)] for j in range(MAP_SIZE)]

    def render(self, surface):
        # 32x32
        for x, c in enumerate(self.map[:40]):
            for y, tile in enumerate(c[:22]):
                pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(x * 32, y * 32, 32, 32))

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), 0)
        self.tilemap = Tilemap()

    def run(self):
        # Run until the user asks to quit
        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the background with white
            self.screen.fill((255, 255, 255))

            # Draw
            self.tilemap.render(self.screen)

            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()