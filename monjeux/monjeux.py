import pygame, random, socket, os, sys

pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

def saisir_nom():
    nom = ""
    actif = True
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 25, 300, 50)
    while actif:
        screen.fill((20, 20, 20))
        txt = font.render("Entre ton pseudo :", True, (255, 255, 255))
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 100))
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        nom_txt = font.render(nom, True, (0, 255, 0))
        screen.blit(nom_txt, (input_box.x + 10, input_box.y + 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nom != "":
                    return nom
                elif event.key == pygame.K_BACKSPACE:
                    nom = nom[:-1]
                else:
                    if len(nom) < 15: nom += event.unicode

def menu():
    while True:
        screen.fill((30, 30, 30))
        solo = font.render("SOLO", True, (0, 255, 0))
        quitter = font.render("QUITTER", True, (255, 0, 0))
        screen.blit(font.render("MON JEU", True, (255, 255, 255)), (WIDTH//2 - 100, 100))
        screen.blit(solo, (WIDTH//2 - 50, 250))
        screen.blit(quitter, (WIDTH//2 - 80, 350))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 250 < y < 300: return "solo"
                if 350 < y < 400: pygame.quit(); sys.exit()

class Boss:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 50, -100, 100, 100)
        self.vie = 50
        self.projectiles = []
        self.direction = 1

    def update(self):
        self.rect.y += 1 if self.rect.y < 100 else 0
        self.rect.x += self.direction * 3
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1
        if random.randint(0, 20) == 0:
            for i in range(-1, 2):
                self.projectiles.append(pygame.Rect(self.rect.centerx + i * 15, self.rect.bottom, 10, 20))

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 255), self.rect)
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 20, 100, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 20, 100 * (self.vie / 50), 10))
        for p in self.projectiles:
            p.y += 7
            pygame.draw.rect(screen, (255, 100, 100), p)

def est_niveau_boss(n):
    return n % 5 == 0

def start_solo(pseudo):
    player = pygame.Rect(500, 350, 40, 40)
    vitesse = 8
    projectiles, ennemis = [], []
    boss = None
    item_clone = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
    clone_active = False
    clone_rect = None

    try:
        with open("save.txt") as f:
            niveau = int(f.read())
    except:
        niveau = 1

    vies = 10
    vaincus = 0
    a_battre = niveau * 10
    running = True

    while running and vies > 0:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), player)
        screen.blit(font.render(f"{pseudo}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"PV: {vies}", True, (255, 255, 255)), (10, 60))
        screen.blit(font.render(f"Niveau: {niveau}", True, (255, 255, 255)), (10, 110))
        screen.blit(font.render(f"Ennemis battus: {vaincus}/{a_battre}", True, (255, 255, 255)), (10, 160))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                projectiles.append(pygame.Rect(player.centerx, player.top, 5, 10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]: player.x -= vitesse
        if keys[pygame.K_d]: player.x += vitesse
        if keys[pygame.K_z]: player.y -= vitesse
        if keys[pygame.K_s]: player.y += vitesse

        for b in projectiles[:]:
            b.y -= 10
            pygame.draw.rect(screen, (255, 255, 0), b)
            if b.y < 0: projectiles.remove(b)

        if item_clone:
            pygame.draw.rect(screen, (0, 255, 255), item_clone)
            screen.blit(font.render("CLONE", True, (255, 255, 255)), (item_clone.x - 10, item_clone.y - 30))
            if player.colliderect(item_clone):
                clone_active = True
                clone_rect = pygame.Rect(player.x + 50, player.y, 40, 40)
                item_clone = None

        if clone_active and clone_rect:
            pygame.draw.rect(screen, (0, 200, 255), clone_rect)
            clone_rect.x = player.x + 50
            clone_rect.y = player.y
            if random.randint(0, 10) == 0:
                projectiles.append(pygame.Rect(clone_rect.centerx, clone_rect.top, 5, 10))

        if est_niveau_boss(niveau):
            if boss is None: boss = Boss()
            boss.update(); boss.draw()
            for p in boss.projectiles[:]:
                if p.colliderect(player): vies -= 1; boss.projectiles.remove(p)
            for b in projectiles[:]:
                if b.colliderect(boss.rect):
                    boss.vie -= 1; projectiles.remove(b)
            if boss and boss.vie <= 0:
                boss = None
                niveau += 1
                vaincus = 0
                a_battre = niveau * 10
                ennemis.clear()
        else:
            for e in ennemis[:]:
                pygame.draw.rect(screen, (255, 0, 0), e)
                e.y += 1 + niveau * 0.5
                if e.y > HEIGHT: vies -= 1; ennemis.remove(e)
                if e.colliderect(player): vies -= 1; ennemis.remove(e)
                for b in projectiles[:]:
                    if b.colliderect(e): ennemis.remove(e); projectiles.remove(b); vaincus += 1
            if random.randint(0, 30) == 0:
                ennemis.append(pygame.Rect(random.randint(0, WIDTH - 40), 0, 40, 40))
            if vaincus >= a_battre:
                niveau += 1
                vaincus = 0
                a_battre = niveau * 10
                ennemis.clear()

        with open("save.txt", "w") as f:
            f.write(str(niveau))

        pygame.display.flip()
        clock.tick(60)

choix = menu()
pseudo = saisir_nom()
if choix == "solo":
    start_solo(pseudo)
