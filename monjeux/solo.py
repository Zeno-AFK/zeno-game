import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("MonJeux - Solo")
clock = pygame.time.Clock()

BLANC, ROUGE, JAUNE, BLEU = (255,255,255), (255,0,0), (255,255,0), (0,100,255)
joueur = pygame.Rect(375, 550, 50, 30)
vitesse = 5
tirs, ennemis = [], []
vitesse_tir, vitesse_ennemi, spawn_timer = 7, 3, 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            tirs.append(pygame.Rect(joueur.centerx-5, joueur.top, 10, 20))

    keys = pygame.key.get_pressed()
if keys[pygame.K_q]: player.x -= 5
if keys[pygame.K_d]: player.x += 5
if keys[pygame.K_z]: player.y -= 5
if keys[pygame.K_s]: player.y += 5


    for tir in tirs[:]:
        tir.y -= vitesse_tir
        if tir.bottom < 0: tirs.remove(tir)

    spawn_timer += 1
    if spawn_timer > 60:
        ennemis.append(pygame.Rect(random.randint(0, 760), 0, 40, 30))
        spawn_timer = 0

    for ennemi in ennemis[:]:
        ennemi.y += vitesse_ennemi
        if ennemi.top > 600: ennemis.remove(ennemi)

    for tir in tirs[:]:
        for ennemi in ennemis[:]:
            if tir.colliderect(ennemi):
                tirs.remove(tir)
                ennemis.remove(ennemi)
                break

    screen.fill(BLEU)
    pygame.draw.rect(screen, BLANC, joueur)
    for tir in tirs: pygame.draw.rect(screen, JAUNE, tir)
    for ennemi in ennemis: pygame.draw.rect(screen, ROUGE, ennemi)
    pygame.display.flip()
    clock.tick(60)
