import pygame, socket, sys

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("MonJeux - Online")
clock = pygame.time.Clock()
player = pygame.Rect(0, 0, 40, 40)
other = pygame.Rect(0, 0, 40, 40)
vitesse = 5

client = socket.socket()
client.connect(("127.0.0.1", 12345))
x, y = map(int, client.recv(1024).decode().split(","))
player.x, player.y = x, y

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.x -= vitesse
    if keys[pygame.K_RIGHT]: player.x += vitesse
    if keys[pygame.K_UP]: player.y -= vitesse
    if keys[pygame.K_DOWN]: player.y += vitesse

    client.send(f"{player.x},{player.y}".encode())
    x, y = map(int, client.recv(1024).decode().split(","))
    other.x, other.y = x, y

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.draw.rect(screen, (255, 0, 0), other)
    pygame.display.flip()
    clock.tick(60)
