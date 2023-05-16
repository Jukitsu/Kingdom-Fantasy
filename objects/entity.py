import pygame 
from objects.animations import EntitiesAnimations
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

import enum
import random

import math

def sign(x):
    return (x > 0) - (x < 0)


class ChatBox:
    def __init__(self, text, i):
        self.text = text
        self.i = i
    def render(self, screen):
        # chatbox
        chat = pygame.transform.scale(pygame.image.load("./resources/textures/parchemin.png"), (1500, 1500))
        chatRect = chat.get_rect()
        chatRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        
        # text
        font = pygame.font.Font("./resources/fonts/medieval.ttf", 32)
        text = font.render(self.text[self.i], True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        legend = font.render("E pour fermer" if self.i+1 == len(self.text) else "E pour passer", True, (0, 0, 0))
        legendRect = legend.get_rect()
        legendRect.center = (SCREEN_WIDTH//1.5, SCREEN_HEIGHT//1.5)

        screen.blit(chat, chatRect)
        screen.blit(text, textRect)
        screen.blit(legend, legendRect)
 
        
EntityType = {
    "NPC": 0,
    "MOB": 1,
    "PLAYER": 2,
    "BOSS": 3
}



class Entity(pygame.sprite.Sprite):
    def __init__(this, player, etype, skin, coords, screen, tilemap, FRICTION, SCREEN_WIDTH, SCREEN_HEIGHT, text, isMeyer):
        this.hp = 15 if skin == "slimeb" else 10000 if skin in ["tuto", "military"] else 2
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
        this.size = 128* 2 if skin=="slimeb" else 128* 1.25
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
                if this.hp != 2 or (this.hp != 15 and this.isMeyer):
                    font = pygame.font.Font("./resources/fonts/medieval.ttf", 25)
                    text = font.render(str(this.hp), True, (255, 0, 0))
                    this.screen.blit(text, (this.x * 32 - round(this.player.x * 32) + this.SCREEN_WIDTH // 2 +20, this.y * 32 - round(this.player.y * 32) + this.SCREEN_HEIGHT // 2 + 20, 32, 32)) # joueur toujours au millieu de l'écran, c'est le bg qui bouge

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
        
    def check_borders(this, delta_time):
        if this.x + this.velocity[0] * delta_time * this.speed < 0:
            this.velocity[0] = 0
        if this.y + this.velocity[1] * delta_time * this.speed < 0:
            this.velocity[1] = 0

    def tick(this, delta_time, player, dist):
        if this.skin in ["tuto", "military"]:
            this.EntitiesAnimations.spawn()
            return
        
        if not this.hp > 0 or not this.cooldownDeath < 20:
            return
        
        if this.cooldownDeath > 0:
            this.cooldownDeath+= 1
            this.EntitiesAnimations.death()
            return
        
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
                    
                    # Entity general movement physics
        
                    # v += a * f * dt
                    this.velocity = [v + a * f * delta_time for v, a, f in zip(this.velocity, this.accel, this.friction)]

                    this.check_borders(delta_time)
                
                    # d = v * dt
                    this.x += this.velocity[0] * delta_time * this.speed
                    this.y += this.velocity[1] * delta_time * this.speed

                    # v -= min(|v * f * dt|, |v|)
                    this.velocity = [v - min(v * f * delta_time, v, key = abs) for v, f in zip(this.velocity, this.friction)]
                    
 

