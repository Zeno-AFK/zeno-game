import pygame, sys
import subprocess

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("MonJeux - Menu")
font = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()

# Boutons
solo_btn = pygame.Rect(200, 120, 200, 60)
online_btn = pygame.Rect(200, 220, 200, 60)

def draw_menu():
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (70, 130, 180), solo_btn)
    pygame.draw.rect(screen, (180, 70, 70), online_btn)
    screen.blit(font.render("Solo", True, (255, 255, 255)), (260, 130))
    screen.blit(font.render("Online", True, (255, 255, 255)), (230, 230))
    pygame.display.flip()

while True:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if solo_btn.collidepoint(event.pos):
                subprocess.Popen(["python", "solo.py"])
            if online_btn.collidepoint(event.pos):
                subprocess.Popen(["python", "client.py"])
    clock.tick(60)
