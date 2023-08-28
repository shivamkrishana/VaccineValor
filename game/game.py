import pygame
from pygame import mixer #module for audio 
import sys
import random

# Initialize pygame
pygame.init()
mixer.init()
mixer.music.load('./music.mp3')
music_playing = True
'''
1. music will run in background untill the game is not finished.
2. play(loops=0, start=0.0, fade_ms=0) -> None
3. The music repeats indefinitely if this argument is set to -1.
'''
mixer.music.play(-1,0,0) 



# Constants
SCREEN_WIDTH = 1000  # Increased width
SCREEN_HEIGHT = 600
VIRUS_SIZE = 60
CELL_SIZE = 30
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Virus Hunter Game")
clock = pygame.time.Clock()

# Load images
background_image = pygame.image.load("./background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
virus_image = pygame.image.load("./virus.png")
virus_image = pygame.transform.scale(virus_image, (VIRUS_SIZE, VIRUS_SIZE))
cell_image = pygame.image.load("./cell.png")
cell_image = pygame.transform.scale(cell_image, (CELL_SIZE, CELL_SIZE))

# Initialize the virus
virus_x = SCREEN_WIDTH // 2 - VIRUS_SIZE // 2
virus_y = SCREEN_HEIGHT // 2 - VIRUS_SIZE // 2
virus_speed = 5

# Initialize healthy cells
cells = []

def spawn_cell():
    x = random.randint(0, SCREEN_WIDTH - CELL_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - CELL_SIZE)
    cells.append((x, y))

def draw_virus(x, y):
    screen.blit(virus_image, (x, y))

def draw_cells():
    for cell in cells:
        screen.blit(cell_image, cell)



# Main game loop
running = True
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if music_playing:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                music_playing = not music_playing
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and virus_x > 0:
        virus_x -= virus_speed
    if keys[pygame.K_RIGHT] and virus_x < SCREEN_WIDTH - VIRUS_SIZE:
        virus_x += virus_speed
    if keys[pygame.K_UP] and virus_y > 0:
        virus_y -= virus_speed
    if keys[pygame.K_DOWN] and virus_y < SCREEN_HEIGHT - VIRUS_SIZE:
        virus_y += virus_speed
    
    virus_rect = pygame.Rect(virus_x, virus_y, VIRUS_SIZE, VIRUS_SIZE)
    for cell in cells:
        cell_rect = pygame.Rect(cell[0], cell[1], CELL_SIZE, CELL_SIZE)
        if virus_rect.colliderect(cell_rect):
            cells.remove(cell)
            spawn_cell()
            score += 1
    
    if len(cells) < 10:
        spawn_cell()
    
    screen.blit(background_image, (0, 0))
    draw_virus(virus_x, virus_y)
    draw_cells()
    
    score_text = f"Score: {score}"
    font = pygame.font.Font(None, 36)
    text_surface = font.render(score_text, True, WHITE)  # Display score in white
    screen.blit(text_surface, (10, 10))
    
    developer_text = "by: SHIVAM KRISHANA"
    developer_surface = font.render(developer_text, True, WHITE)  # Display developer name in white
    screen.blit(developer_surface, (SCREEN_WIDTH - developer_surface.get_width() - 10, SCREEN_HEIGHT - 40))
    
    
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
