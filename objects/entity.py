import pygame 

import enum
import random

import math

def sign(x):
    return (x > 0) - (x < 0)

def collide(c1, c2, velocity):
    # this: the dynamic collider, which moves
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
    def __init__(this, player, etype, image, coords, screen, tilemap, FRICTION, SCREEN_WIDTH, SCREEN_HEIGHT):
        this.hp = 100
        this.x, this.y = coords
        this.player = player
        this.velocity = [0, 0]
        this.accel = [0, 0]
        this.friction = FRICTION
        this.speed = 6
        this.screen = screen
        this.type = etype
        this.chat = ("", None)
        super().__init__()
        this.tilemap = tilemap
        this.image = pygame.image.load(image)
        this.rect = this.image.get_rect()
        this.rigidBody = pygame.Rect(this.x, this.y, 16, 16)
        this.isAttacking = [False, 0, "r"]
        this.size = 128* 1.25
        this.SCREEN_WIDTH = SCREEN_WIDTH
        this.SCREEN_HEIGHT = SCREEN_HEIGHT
        this.target = None
        this.fleeing = False
        
    def render(this, skin=None):
        if abs(this.x - this.player.x) < 44 and abs(this.y - this.player.y) < 26:
            if skin:
                this.image = pygame.transform.scale(skin, (this.size, this.size))
            this.screen.blit(this.image, (this.x * 32 - round(this.player.x * 32) + this.SCREEN_WIDTH // 2, this.y * 32 - round(this.player.y * 32) + this.SCREEN_HEIGHT // 2, 32, 32)) # joueur toujours au millieu de l'écran, c'est le bg qui bouge
        
    def check_collision(this, delta_time):
        """Only use between friction modifications"""
        for _ in range(2):
            adjusted_velocity = [v * delta_time for v in this.velocity]
            vx, vy = adjusted_velocity

            # find all the blocks we could potentially be colliding with
            # this step is known as "broad-phasing"

            step_x = 1 if vx > 0 else -1
            step_y = 1 if vy > 0 else -1

            steps_xz = 1
            steps_y  = 1

            x, y = int(this.x), int(this.y)
            cx, cy = [int(x + v) for x, v in zip((this.x, this.y), adjusted_velocity)]

            potential_collisions = []

            for i in range(x - step_x * (steps_xz + 2), cx + step_x * (steps_xz + 2), step_x):
                for j in range(y - step_y * (steps_y + 2), cy + step_y * (steps_y + 2), step_y):
                    pos = (i, j)
                    
                    if i < 0 and j < 0:
                        continue
                    tile = this.tilemap.map[i][j]

                    if not tile in [11, 12]:
                        continue
                    
                    entry_time, normal = collide((this.x, this.y, this.x + 2, this.y + 2), (i, j, i+1, j+1), adjusted_velocity)

                    if normal is None:
                        continue

                    potential_collisions.append((entry_time, normal))

            # get first collision

            if not potential_collisions:
                break

            entry_time, normal = min(potential_collisions, key = lambda x: x[0])
            entry_time -= 0.001

            if normal[0]:
                this.velocity[0] = 0
                this.x += vx * entry_time
            
            if normal[1]:
                this.velocity[1] = 0
                this.y += vy * entry_time
                
    def hurt(this, damage):
        this.hp -= damage
        this.flee()
    
    def idle(this, delta_time):
        if not random.randint(0, int(3 / delta_time)) and this.target is None: # change target every 3 seconds on average
            this.fleeing = False 
            target_tile = [i + random.randint(-20, 20) for i in (this.x, this.y)]
            if math.dist((this.player.x, this.player.y), (this.x, this.y)) < 10:
                this.target = this.player
            norm = math.sqrt((target_tile[0] - this.x) ** 2 + (target_tile[1] - this.y) ** 2)
            this.accel = [(target_tile[0] - this.x) / norm, (target_tile[1] - this.y) / norm]
    def flee(this):
        this.accel = [-a for a in this.accel]
        this.fleeing = True
        this.target = None
        
    def chase(this):
        if this.target:
            norm = math.sqrt((this.player.x - this.x) ** 2 + (this.player.y - this.y) ** 2)
            this.accel = [(this.player.x - this.x) / norm, (this.player.y - this.y) / norm]
   
    def move(this, delta_time):
        this.idle(delta_time)
        this.chase()
        
        this.velocity = [v + a * f * delta_time for v, a, f in zip(this.velocity, this.accel, this.friction)]
        
        if this.x + this.velocity[0] * delta_time * this.speed < 0:
            this.velocity[0] = 0
        if this.y + this.velocity[1] * delta_time * this.speed < 0:
            this.velocity[1] = 0
            
        #SOUTHEAST
            
        this.x += this.velocity[0] * delta_time * this.speed
        this.y += this.velocity[1] * delta_time * this.speed

        
        this.velocity = [v - min(v * f * delta_time, v, key = abs) for v, f in zip(this.velocity, this.friction)]