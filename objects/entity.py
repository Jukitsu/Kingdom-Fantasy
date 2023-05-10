import pygame 

import enum
import random
def collide(c1, c2, velocity):
    # self: the dynamic collider, which moves
    # collider: the static collider, which stays put
    
    c1x1, c1y1, c1x2, c1y2 = c1
    c2x1, c2y1, c2x2, c2y2 = c2
    
    no_collision = 1, None

    # find entry & exit times for each axis

    vx, vy = velocity

    time = lambda x, y: x / y if y else float('-' * (x > 0) + "inf")

    x_entry = time(c2x1 - c1x2 if vx > 0 else c2x2 - c1x1, vx)
    x_exit  = time(c2x2 - c1x1 if vx > 0 else c2x1 - c1x2, vx)

    y_entry = time(c2y1 - c1y2 if vy > 0 else c2y2 - c1y1, vy)
    y_exit  = time(c2y2 - c1y1 if vy > 0 else c2y1 - c1y2, vy)

    # make sure we actually got a collision

    if x_entry < 0 and y_entry < 0:
        return no_collision

    if x_entry > 1 or y_entry > 1:
        return no_collision
    
    # on which axis did we collide first?

    entry = max(x_entry, y_entry)
    exit_ = min(x_exit,  y_exit)

    if entry > exit_:
        return no_collision
    
    # find normal of surface we collided with

    nx = (0, -1 if vx > 0 else 1)[entry == x_entry]
    ny = (0, -1 if vy > 0 else 1)[entry == y_entry]


    return entry, (nx, ny)     
        

class EntityType(enum.Enum):
    NPC = 0
    MOB = 1
    PLAYER = 2

class Entity(pygame.sprite.Sprite):
    def __init__(self, etype, image, coords, screen, tilemap, FRICTION, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.x, self.y = coords
        self.velocity = [0, 0]
        self.accel = [0, 0]
        self.friction = FRICTION
        self.speed = 16
        self.screen = screen
        self.type = etype
        self.chat = ("", None)
        super().__init__()
        self.tilemap = tilemap
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rigidBody = pygame.Rect(self.x, self.y, 16, 16)
        self.isAttacking = [False, 0, "r"]
        self.size = 128* 1.25
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        
    def render(self, skin):
        self.image = pygame.transform.scale(skin, (self.size, self.size))
        self.screen.blit(self.image, (self.SCREEN_WIDTH//2 - (self.size//2), self.SCREEN_HEIGHT//2 - (self.size//2))) # joueur toujours au millieu de l'écran, c'est le bg qui bouge
        
    def check_collision(self, delta_time):
        """Only use between friction modifications"""
        for _ in range(2):
            adjusted_velocity = [v * delta_time for v in self.velocity]
            vx, vy = adjusted_velocity

            # find all the blocks we could potentially be colliding with
            # this step is known as "broad-phasing"

            step_x = 1 if vx > 0 else -1
            step_y = 1 if vy > 0 else -1

            steps_xz = 1
            steps_y  = 1

            x, y = int(self.x), int(self.y)
            cx, cy = [int(x + v) for x, v in zip((self.x, self.y), adjusted_velocity)]

            potential_collisions = []

            for i in range(x - step_x * (steps_xz + 2), cx + step_x * (steps_xz + 2), step_x):
                for j in range(y - step_y * (steps_y + 2), cy + step_y * (steps_y + 2), step_y):
                    pos = (i, j)
                    
                    if i < 0 and j < 0:
                        continue
                    tile = self.tilemap.map[i][j]

                    if not tile in [8, 9]:
                        continue
                    
                    entry_time, normal = collide((self.x, self.y, self.x + 2, self.y + 2), (i, j, i+1, j+1), adjusted_velocity)

                    if normal is None:
                        continue

                    potential_collisions.append((entry_time, normal))

            # get first collision

            if not potential_collisions:
                break

            entry_time, normal = min(potential_collisions, key = lambda x: x[0])
            entry_time -= 0.001

            if normal[0]:
                self.velocity[0] = 0
                self.x += vx * entry_time
            
            if normal[1]:
                self.velocity[1] = 0
                self.y += vy * entry_time
   
    def move(self, delta_time):
        self.accel = [random.randint(-1, 1), random.randint(-1, 1)]
        self.velocity = [v + a * f * delta_time for v, a, f in zip(self.velocity, self.accel, self.friction)]
      
        self.x += self.velocity[0] * delta_time * self.speed
        self.y += self.velocity[1] * delta_time * self.speed         

        
        self.velocity = [v - min(v * f * delta_time, v, key = abs) for v, f in zip(self.velocity, self.friction)]