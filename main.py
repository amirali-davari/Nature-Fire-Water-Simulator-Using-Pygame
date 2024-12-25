import pygame
import sys
from random import randint
from math import sin as sinr
from math import cos as cosr
from math import radians

# Setting
RPS = False
STAT_BAR = True
OBJ_NUMBER = 20

def sin(x):
    return sinr(radians(x))

def cos(x):
    return cosr(radians(x))

class Object:
    def __init__(self, start_x_pos, start_y_pos, angle, surface=None):
        self.pos = pygame.Vector2(start_x_pos, start_y_pos)
        self.angle = angle
        self.move_vector = pygame.Vector2(cos(self.angle), -sin(self.angle))
        if surface == None:
            self.surf = pygame.Surface((40, 40))
        else:
            self.surf = surface
        self.rect = self.surf.get_rect(center=(start_x_pos, start_y_pos))
    
    def move(self, amount=1):
        self.pos += self.move_vector * amount
        self.rect.center = self.pos

    def change_angle(self, new_angle):
        self.angle = new_angle
        self.move_vector = pygame.Vector2(cos(self.angle), -sin(self.angle))
    
    def set_surface(self, surface):
        self.surf = surface
    
    def display(self, surface):
        surface.blit(self.surf, self.rect)

SCREEN_COLOR = '#0984ff'
BORDER_COLOR = '#ffa909'
NAT_COLOR = '#7f8e94' if RPS else '#538a00'
FIR_COLOR = '#ffbc48' if RPS else '#e72300'
WAT_COLOR = '#ff6c6c' if RPS else '#15a6c3'

DEBUG_ZONE = False
DEBUG_HIT = False
START_SIM = False

pygame.init()
HEIGHT = 674 # Do NOT put this lower than 610 unless you have arranged everything manually
STAT_BAR_WIDTH = 150 if STAT_BAR else 0
WIDTH = HEIGHT + STAT_BAR_WIDTH
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('NFW Simulator')
clock = pygame.time.Clock()

nat_surf = pygame.image.load('resource/roc.png' if RPS else 'resource/nat.png').convert_alpha()
fir_surf = pygame.image.load('resource/pap.png' if RPS else 'resource/fir.png').convert_alpha()
wat_surf = pygame.image.load('resource/sci.png' if RPS else 'resource/wat.png').convert_alpha()

nat_surf = pygame.transform.scale(nat_surf, (40, 40))
fir_surf = pygame.transform.scale(fir_surf, (40, 40))
wat_surf = pygame.transform.scale(wat_surf, (40, 40))

x, y = HEIGHT//2, HEIGHT//2
nat = []
fir = []
wat = []
for i in range(OBJ_NUMBER):
    nat.append(Object(randint(x-50, x+50), randint(y-300, y-200), randint(1, 360), nat_surf))
    fir.append(Object(randint(x+167, x+267), randint(y+75, y+175), randint(1, 360), fir_surf))
    wat.append(Object(randint(x-267, x-167), randint(y+75, y+175), randint(1, 360), wat_surf))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                DEBUG_ZONE = not DEBUG_ZONE
            elif event.key == pygame.K_x:
                DEBUG_HIT = not DEBUG_HIT
            elif event.key == pygame.K_SPACE:
                START_SIM = not START_SIM
            elif event.key == pygame.K_RETURN:
                START_SIM = False
                nat = []
                fir = []
                wat = []
                for i in range(OBJ_NUMBER):
                    nat.append(Object(randint(x-50, x+50), randint(y-300, y-200), randint(1, 360), nat_surf))
                    fir.append(Object(randint(x+167, x+267), randint(y+75, y+175), randint(1, 360), fir_surf))
                    wat.append(Object(randint(x-267, x-167), randint(y+75, y+175), randint(1, 360), wat_surf))
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Draw basic screen
    scr.fill(SCREEN_COLOR)
    pygame.draw.rect(scr, BORDER_COLOR, (0, 0, HEIGHT, 5))
    pygame.draw.rect(scr, BORDER_COLOR, (WIDTH-5-STAT_BAR_WIDTH, 5, 5, HEIGHT-5))
    pygame.draw.rect(scr, BORDER_COLOR, (0, HEIGHT-5, HEIGHT, 5))
    pygame.draw.rect(scr, BORDER_COLOR, (0, 5, 5, HEIGHT-5))

    if DEBUG_ZONE:
        pygame.draw.circle(scr, '#0000ff', (x, y), 5)

        pygame.draw.rect(scr, '#00ff00', (x-50, y-300, 100, 100))
        pygame.draw.circle(scr, '#ff0000', (x, y-250), 5)

        pygame.draw.rect(scr, '#00ff00', (x+167, y+75, 100, 100))
        pygame.draw.circle(scr, '#ff0000', (x+217, y+125), 5)

        pygame.draw.rect(scr, '#00ff00', (x-267, y+75, 100, 100))
        pygame.draw.circle(scr, '#ff0000', (x-217, y+125), 5)

        pygame.draw.line(scr, '#ffff00', (x, y-250), (x+217, y+125),     3)
        pygame.draw.line(scr, '#ffff00', (x+217, y+125), (x-217, y+125), 3)
        pygame.draw.line(scr, '#ffff00', (x-217, y+125), (x, y-250),     3)

    # Draw and move objs
    for i in nat:
        if START_SIM: i.move()
        if i.rect.left <= 5 or i.rect.right >= WIDTH - 5 - STAT_BAR_WIDTH: i.change_angle(180-i.angle)
        if i.rect.top <= 5 or i.rect.bottom >= HEIGHT - 5: i.change_angle(360-i.angle)
        for j in wat:
            if i.rect.colliderect(j.rect):
                nat.append(j)
                wat.remove(j)
                j.set_surface(nat_surf)
        i.display(scr)
    for i in fir:
        if START_SIM: i.move()
        if i.rect.left <= 5 or i.rect.right >= WIDTH - 5 - STAT_BAR_WIDTH: i.change_angle(180-i.angle)
        if i.rect.top <= 5 or i.rect.bottom >= HEIGHT - 5: i.change_angle(360-i.angle)
        for j in nat:
            if i.rect.colliderect(j.rect):
                fir.append(j)
                nat.remove(j)
                j.set_surface(fir_surf)
        i.display(scr)
    for i in wat:
        if START_SIM: i.move()
        if i.rect.left <= 5 or i.rect.right >= WIDTH - 5 - STAT_BAR_WIDTH: i.change_angle(180-i.angle)
        if i.rect.top <= 5 or i.rect.bottom >= HEIGHT - 5: i.change_angle(360-i.angle)
        for j in fir:
            if i.rect.colliderect(j.rect):
                wat.append(j)
                fir.remove(j)
                j.set_surface(wat_surf)
        i.display(scr)

    if DEBUG_HIT:
        for i in nat:
            pygame.draw.line(scr, '#ff0000', i.rect.topleft, i.rect.topright)
            pygame.draw.line(scr, '#ff0000', i.rect.topleft, i.rect.bottomleft)
            pygame.draw.line(scr, '#ff0000', i.rect.topright, i.rect.bottomright)
            pygame.draw.line(scr, '#ff0000', i.rect.bottomleft, i.rect.bottomright)

            pygame.draw.line(scr, '#0000ff', i.rect.center, i.rect.center + i.move_vector * 30)
        for i in fir:
            pygame.draw.line(scr, '#ff0000', i.rect.topleft, i.rect.topright)
            pygame.draw.line(scr, '#ff0000', i.rect.topleft, i.rect.bottomleft)
            pygame.draw.line(scr, '#ff0000', i.rect.topright, i.rect.bottomright)
            pygame.draw.line(scr, '#ff0000', i.rect.bottomleft, i.rect.bottomright)
            
            pygame.draw.line(scr, '#0000ff', i.rect.center, i.rect.center + i.move_vector * 30)
        for i in wat:
            pygame.draw.line(scr, '#ff0000', i.rect.topleft, i.rect.topright)
            pygame.draw.line(scr, '#ff0000', i.rect.topleft, i.rect.bottomleft)
            pygame.draw.line(scr, '#ff0000', i.rect.topright, i.rect.bottomright)
            pygame.draw.line(scr, '#ff0000', i.rect.bottomleft, i.rect.bottomright)
            
            pygame.draw.line(scr, '#0000ff', i.rect.center, i.rect.center + i.move_vector * 30)

    if STAT_BAR:
        nat_height = round(len(nat)*HEIGHT/(3*OBJ_NUMBER))
        fir_height = round(len(fir)*HEIGHT/(3*OBJ_NUMBER))
        wat_height = round(len(wat)*HEIGHT/(3*OBJ_NUMBER))
        pygame.draw.rect(scr, FIR_COLOR, (HEIGHT, 0, STAT_BAR_WIDTH, HEIGHT))
        pygame.draw.rect(scr, NAT_COLOR, (HEIGHT, 0, STAT_BAR_WIDTH, nat_height))
        pygame.draw.rect(scr, WAT_COLOR, (HEIGHT, HEIGHT-wat_height, STAT_BAR_WIDTH, wat_height))

    pygame.display.update()
    clock.tick(60)