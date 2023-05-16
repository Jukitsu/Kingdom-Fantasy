import pygame 
from objects.animations import EntitiesAnimations

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
        
EntityType = {
    "NPC": 0,
    "MOB": 1,
    "PLAYER": 2,
    "BOSS": 3
}



class Entity(pygame.sprite.Sprite):
    def __init__(this, player, etype, skin, coords, screen, tilemap, FRICTION, SCREEN_WIDTH, SCREEN_HEIGHT, text, isMeyer):
        this.hp = 10000 if skin in ["tuto", "military"] else 2
        this.x, this.y = coords
        this.player = player
        this.velocity = [0, 0]
        this.accel = [0, 0]
        this.friction = FRICTION
        this.speed = 6
        this.screen = screen
        this.type = etype
        this.chat = (text, None)
        super().__init__()
        this.tilemap = tilemap
        this.skin = skin
        this.rigidBody = pygame.Rect(this.x, this.y, 16, 16)
        this.isAttacking = [False, 0, "r"]
        this.size = 128* 1.25
        this.SCREEN_WIDTH = SCREEN_WIDTH
        this.SCREEN_HEIGHT = SCREEN_HEIGHT
        this.target = None
        this.fleeing = False
        this.discovered = False
        this.cooldownDeath = 0 # set on 3
        this.cooldownSpawn = 0
        this.EntitiesAnimations = EntitiesAnimations(this.player, this)
        this.isAttacked = True
        this.cooldownAttack = 0
        this.isMeyer = isMeyer
        
    def render(this, skin=None):
        if abs(this.x - this.player.x) < 44 and abs(this.y - this.player.y) < 26:
            if skin:
                if this.hp == 1:
                    rayon = 5  # Rayon du cercle
                    cercle_surface = pygame.Surface((rayon * 2, rayon * 2), pygame.SRCALPHA)
                    couleur_cercle = (255, 0, 0)  # Exemple : Rouge (RVB)
                    centre_cercle = (rayon, rayon)  # Centre du cercle
                    pygame.draw.circle(cercle_surface, couleur_cercle, centre_cercle, rayon)

                    skin.blit(cercle_surface, (10, 10))
                this.screen.blit(pygame.transform.scale(skin, (this.size, this.size)), (this.x * 32 - round(this.player.x * 32) + this.SCREEN_WIDTH // 2, this.y * 32 - round(this.player.y * 32) + this.SCREEN_HEIGHT // 2, 32, 32)) # joueur toujours au millieu de l'écran, c'est le bg qui bouge
                if this.isMeyer:
                    this.displayMeyer()
                    
    def displayMeyer(this):
        font = pygame.font.Font("./resources/fonts/whoask.ttf", 32)
        text = font.render('M.Meyer', True, (0, 0, 0))
        this.screen.blit(text, (this.x * 32 - round(this.player.x * 32) + this.SCREEN_WIDTH // 2 + 30, this.y * 32 - round(this.player.y * 32) + this.SCREEN_HEIGHT // 2 -20, 32, 32))


    def check_collision(this, delta_time):
        """Only use between friction modifications"""
        def isCollider(i, j):
            tile = this.tilemap.map[int(i)][int(j)]

            return tile in [11, 12]
                
        if isCollider(this.x + this.velocity[0] * delta_time * this.speed, this.y + this.velocity[1] * delta_time * this.speed):
            this.velocity = [0, 0]
                
                
    def hurt(this, damage):
        this.hp -= damage
        if this.hp <= 0:
            this.EntitiesAnimations.death()
            
    def attackPlayer(this):
        this.player.hurt(1)

    def chase(this):
        norm = math.sqrt((this.player.x - this.x) ** 2 + (this.player.y - this.y) ** 2)
        this.accel = [(this.player.x - this.x) / norm, (this.player.y - this.y) / norm]
        this.EntitiesAnimations.walk("l" if this.velocity[0] < 0 else "r", this.velocity)

    def move(this, delta_time, player, dist):
        if this.skin in ["tuto", "military"]:
            this.EntitiesAnimations.spawn()
        else:
            if this.hp > 0 and this.cooldownDeath < 20:
                if this.cooldownDeath > 0:
                    this.cooldownDeath+= 1
                    this.EntitiesAnimations.death()
                else:
                    if dist((this.x, this.y), (player.x, player.y)) <= 10:
                        if not this.discovered:
                            this.cooldownSpawn = 1
                            this.discovered = True
                            this.EntitiesAnimations.spawn()
                    if this.discovered:
                        if this.cooldownSpawn > 0 and this.cooldownSpawn < 50:
                            this.cooldownSpawn += 1
                            this.EntitiesAnimations.spawn()

                        else:
                            this.cooldownSpawn = 0

                            if dist((this.x, this.y), (player.x, player.y)) <= 3:
                                this.EntitiesAnimations.attack("l" if this.velocity[0] < 0 else "r")
                                this.cooldownAttack += 1
                                if this.cooldownAttack > 30:
                                    this.attackPlayer()
                                    this.cooldownAttack = 0
                            else:
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

