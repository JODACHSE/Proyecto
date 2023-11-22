import sys
import pygame
import random

# Constantes
WIDTH = 900
HEIGHT = 506

# Colores
negro = (0, 0, 0)
blanco = (255, 255, 255)
verde = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dragon Ball Z - shooter game')
icon = pygame.image.load('Game/assets/Goku_icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Cargar música
pygame.mixer.music.load('Game/audio/CHALA_HEAD_CHALA.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont('serif', size)
    text_surface = font.render(text, True, blanco)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, verde, fill)
    pygame.draw.rect(surface, blanco, border, 2)


def draw_volume_bar(surface, x, y, volume):
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill_width = int(BAR_LENGTH * volume)
    fill = pygame.Rect(x, y, fill_width, BAR_HEIGHT)
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    pygame.draw.rect(surface, verde, fill)
    pygame.draw.rect(surface, blanco, border, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Game/assets/player.png').convert()
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100

    # Funcion de actualizacion
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        power = Power(self.rect.centerx, self.rect.top)
        all_sprites.add(power)
        powers.add(power)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_images)
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)


class Power(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Game/assets/laser1.png')
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


enemy_images = []
enemy_list = ["Game/assets/big1.png", "Game/assets/big2.png", "Game/assets/big3.png", "Game/assets/big4.png",
              "Game/assets/med1.png", "Game/assets/med2.png", "Game/assets/small1.png", "Game/assets/small2.png",
              "Game/assets/tiny1.png", "Game/assets/tiny2.png"]

for img in enemy_list:
    enemy_images.append(pygame.image.load(img).convert())

# Cargar Imagen De Fondo
background = pygame.image.load('Game/assets/background.png').convert()

all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
powers = pygame.sprite.Group()

player = Player()
all_sprites.add(player)


def new_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemy_group.add(enemy)


for i in range(8):
    new_enemy()


score = 0
volume = 0.5
running = True
menu_active = False
paused = False
previous_volume = volume
music_position = 0

while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            elif event.key == pygame.K_ESCAPE:
                if not paused:
                    previous_volume = volume
                    music_position = pygame.mixer.music.get_pos()
                    volume = 0.5
                    pygame.mixer.music.set_volume(volume)
                paused = not paused
            elif paused:
                if event.key == pygame.K_RETURN:
                    paused = False
                    volume = previous_volume
                    pygame.mixer.music.set_volume(volume)
                    pygame.mixer.music.play(-1, fade_ms=100, start=music_position)
                elif event.key == pygame.K_UP:
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_DOWN:
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)

    if not paused:
        all_sprites.update()

        # Verificar colisiones - enemigo - poder
        hits = pygame.sprite.groupcollide(enemy_group, powers, True, True)
        for hit in hits:
            score += 1
            new_enemy()

        # Verificar colisiones - jugador - enemigo
        hits = pygame.sprite.spritecollide(player, enemy_group, True)

        for hit in hits:
            player.shield -= 20
            new_enemy()
            if player.shield <= 0:
                running = False

    screen.blit(background, [0, 0])

    all_sprites.draw(screen)

    # Marcador
    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    # Escudo
    draw_shield_bar(screen, 5, 5, player.shield)

    # Menu
    if paused:
        draw_text(screen, "Game Paused", 40, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "Press Enter to resume", 20, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text(screen, "Volume:", 20, WIDTH // 2 - 80, HEIGHT // 2 + 80)
        draw_volume_bar(screen, WIDTH // 2 - 20, HEIGHT // 2 + 80, volume)

    pygame.display.flip()

# Detener música, salir del juego y cerrar ventana
pygame.mixer.music.stop()
pygame.quit()
sys.exit()