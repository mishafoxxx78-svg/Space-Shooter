import pygame
import random
import sys

# ================= НАСТРОЙКИ =================

WIDTH = 800
HEIGHT = 600
FPS = 60

PLAYER_SPEED = 6
BULLET_SPEED = 8
ENEMY_SPEED = 3
SPAWN_DELAY = 1000  # миллисекунды

# ================= ИНИЦИАЛИЗАЦИЯ =================

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Shooter")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)

# ================= КЛАССЫ =================

class Player:
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 70
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.score = 0

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect())

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed


class Bullet:
    def __init__(self, x, y):
        self.width = 5
        self.height = 10
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED

    def update(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 0), self.rect())

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed = ENEMY_SPEED

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect())

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# ================= ФУНКЦИИ =================

def draw_text(text, font, color, x, y):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))


def game_over_screen(score):
    screen.fill((0, 0, 0))
    draw_text("GAME OVER", big_font, (255, 0, 0), WIDTH // 2 - 150, HEIGHT // 2 - 60)
    draw_text(f"Score: {score}", font, (255, 255, 255), WIDTH // 2 - 50, HEIGHT // 2)
    draw_text("Press R to Restart or Q to Quit", font, (255, 255, 255), WIDTH // 2 - 180, HEIGHT // 2 + 40)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# ================= ОСНОВНАЯ ИГРА =================

def main():
    player = Player()
    bullets = []
    enemies = []

    pygame.time.set_timer(pygame.USEREVENT, SPAWN_DELAY)

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 20))

        # ======= СОБЫТИЯ =======
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Спавн врагов
            if event.type == pygame.USEREVENT:
                enemies.append(Enemy())

            # Стрельба
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(
                        player.x + player.width // 2 - 2,
                        player.y
                    ))

        keys = pygame.key.get_pressed()
        player.move(keys)

        # ======= ОБНОВЛЕНИЕ ПУЛЬ =======
        for bullet in bullets[:]:
            bullet.update()
            if bullet.y < 0:
                bullets.remove(bullet)

        # ======= ОБНОВЛЕНИЕ ВРАГОВ =======
        for enemy in enemies[:]:
            enemy.update()

            # Враг достиг низа
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                player.lives -= 1

            # Столкновение с игроком
            if enemy.rect().colliderect(player.rect()):
                enemies.remove(enemy)
                player.lives -= 1

        # ======= ПРОВЕРКА ПОПАДАНИЙ =======
        for enemy in enemies[:]:
            for bullet in bullets[:]:
                if enemy.rect().colliderect(bullet.rect()):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    player.score += 1
                    break

        # ======= ОТРИСОВКА =======
        player.draw()

        for bullet in bullets:
            bullet.draw()

        for enemy in enemies:
            enemy.draw()

        draw_text(f"Score: {player.score}", font, (255, 255, 255), 10, 10)
        draw_text(f"Lives: {player.lives}", font, (255, 255, 255), 10, 40)

        pygame.display.flip()

        # ======= GAME OVER =======
        if player.lives <= 0:
            game_over_screen(player.score)
            main()
            return

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()