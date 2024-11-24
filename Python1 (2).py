import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fish Game")

# Load assets
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
player_image = pygame.image.load("player_fish.png")
enemy_image = pygame.image.load("enemy_fish.png")
shield_image = pygame.image.load("shield.png")
bomb_image = pygame.image.load("bomb.png")

# Fonts
start_end_font = pygame.font.Font("pressstart.ttf", 20)  # Replace "custom_font.ttf" with your font file
score_font = pygame.font.Font(None, 36)  # None uses default font

# Game variables
score = 0  # Initialize the score to 0

# Clock for controlling the frame rate
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # None uses the default font; 36 is the font size

# Resize images dynamically based on size
def scale_image(image, size):
    return pygame.transform.scale(image, (size * 2, size * 2))

# Fish class

ENEMY_SCALE_FACTOR = 1.5

class Fish:
    def __init__(self, x, y, size, image, scale_factor=1.0):
        self.x = x
        self.y = y
        self.size = size  # Logical size for collision
        self.scale_factor = scale_factor  # Visual scaling
        self.image = pygame.transform.scale(image, (int(size * 2 * scale_factor), int(size * 2 * scale_factor)))
        self.speed = random.randint(2, 5)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.x -= self.speed

    def draw(self, screen):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect.topleft)


# Shield class
class Shield:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.transform.scale(shield_image, (40, 40))
        self.visible = False
        self.active = False
        self.start_time = 0

    def spawn(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.visible = True
        self.start_time = time.time()

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, (self.x, self.y))

    def collect(self):
        self.visible = False
        self.active = True
        self.start_time = time.time()
        print("Shield ON")

    def deactivate(self):
        self.active = False
        print("Shield OFF")

# Bomb class
class Bomb:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.image = pygame.transform.scale(bomb_image, (50, 50))
        self.active = True
        self.flashing = True
        self.flash_start_time = time.time()
        self.start_time = self.flash_start_time
        self.speed = 2

    def move(self):
        if self.active:
            self.y += self.speed

    def draw(self, screen):
        if self.active:
            if self.flashing:
                elapsed_time = time.time() - self.flash_start_time
                if int(elapsed_time * 10) % 2 == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 50, 50))
                else:
                    screen.blit(self.image, (self.x, self.y))
            else:
                screen.blit(self.image, (self.x, self.y))

# Create the player fish
player = Fish(WIDTH // 2, HEIGHT // 2, 40, player_image)

# List of enemy fish
enemies = []
enemy_spawn_time = time.time()

# Shield object
shield = Shield()

# List of bombs
bombs = []
bomb_spawn_time = time.time()

# Winning size
WINNING_SIZE = 62

# Function to display the start screen
def show_start_screen():
    screen.blit(background_image, (0, 0))
    title_text = start_end_font.render("Fish Game", True, (255, 255, 255))
    instructions_text = start_end_font.render("Press SPACE key to start", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    instructions_rect = instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(title_text, title_rect)
    screen.blit(instructions_text, instructions_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def show_end_screen(message):
    screen.blit(background_image, (0, 0))
    end_text = start_end_font.render(message, True, (255, 255, 255))
    instructions_text = start_end_font.render("Press ESC to exit", True, (255, 255, 255))
    end_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    instructions_rect = instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(end_text, end_rect)
    screen.blit(instructions_text, instructions_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

# Game loop variables
running = True
last_shield_spawn = time.time()
is_shielded = False

show_start_screen()

# Game loop
while running:
    screen.blit(background_image, (0, 0))

    # Render and display the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and draw the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x - player.size > 0:
        player.x -= player.speed
    if keys[pygame.K_RIGHT] and player.x + player.size < WIDTH:
        player.x += player.speed
    if keys[pygame.K_UP] and player.y - player.size > 0:
        player.y -= player.speed
    if keys[pygame.K_DOWN] and player.y + player.size < HEIGHT:
        player.y += player.speed

    player.draw(screen)

    # Show shield around player if active
    if is_shielded:
        shield_icon = pygame.transform.scale(shield_image, (player.size * 3, player.size * 3))
        screen.blit(shield_icon, (player.x - player.size, player.y - player.size))

    # Spawn and manage shield
    if not shield.visible and not shield.active and time.time() - last_shield_spawn > 30:
        shield.spawn()
        last_shield_spawn = time.time()

    if shield.visible and time.time() - shield.start_time > 5:
        shield.visible = False

    shield.draw(screen)

    # Check if the player collects the shield
    shield_distance = ((player.x - shield.x) ** 2 + (player.y - shield.y) ** 2) ** 0.5
    if shield.visible and shield_distance < player.size + 20:
        shield.collect()
        is_shielded = True

    if shield.active and time.time() - shield.start_time > 5:
        shield.deactivate()
        is_shielded = False

    # Spawn bombs every 10 seconds
    if time.time() - bomb_spawn_time > 10:
        bombs.append(Bomb())
        bomb_spawn_time = time.time()

    # Bomb handling logic
    for bomb in bombs[:]:
        bomb.move()
        bomb.draw(screen)

        if bomb.flashing and time.time() - bomb.flash_start_time > 1:
            bomb.flashing = False

        bomb_distance = ((player.x - bomb.x) ** 2 + (player.y - bomb.y) ** 2) ** 0.5
        if bomb_distance < player.size + 20 and bomb.active:
            if not is_shielded and not bomb.flashing:
                print("Hit by bomb! Game Over!")
                show_end_screen("Game Over, You Lose (hit by bomb)")
                running = False
            elif is_shielded:
                bomb.active = False

        if time.time() - bomb.start_time > 7 or bomb.y > HEIGHT:
            bombs.remove(bomb)

    # Spawn enemies every 3 seconds
    if time.time() - enemy_spawn_time > 3:
        enemy_size = random.randint(30, 70)
        enemy_y = random.randint(50, HEIGHT - 50)
        # Scale only enemy images here
        enemy_image_scaled = pygame.transform.scale(enemy_image, (int(enemy_size * 2 * ENEMY_SCALE_FACTOR), int(enemy_size * 2 * ENEMY_SCALE_FACTOR)))
        enemies.append(Fish(WIDTH, enemy_y, enemy_size, enemy_image_scaled))
        enemy_spawn_time = time.time()





    # Move and draw enemies
    for enemy in enemies[:]:
        enemy.move()
        enemy.draw(screen)

        # Remove enemies if they move off-screen
        if enemy.x + enemy.size < 0:
            enemies.remove(enemy)

        # Check collision with the player
        enemy_distance = ((player.x - enemy.x) ** 2 + (player.y - enemy.y) ** 2) ** 0.5
        if enemy_distance < player.size + enemy.size:
            if player.size > enemy.size:
                player.size += 2  # Grow the player ---- !!!!!!!! 
                enemies.remove(enemy)  # Remove the eaten enemy
                score += 1
                print(f"Player ate a fish! New size: {player.size}")
            else:
                if is_shielded:  # Shield prevents being eaten
                    print("Shield protected you from a bigger fish!")
                    enemies.remove(enemy)  # Remove the enemy fish anyway
                else:
                    print("Eaten by a bigger fish! Game Over!")
                    show_end_screen("Game Over, You Lose (eaten by bigger fish)")
                    running = False



    # Check if the player wins
    if player.size >= WINNING_SIZE:
        print("You Win!")
        show_end_screen("You Win!")
        running = False

    # Update the display
    pygame.display.flip()
    clock.tick(30)
    # Draw background
    screen.blit(background_image, (0, 0))

    # Render and display the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White color
    screen.blit(score_text, (10, 10))  # Position at the top-left corner


pygame.quit()
