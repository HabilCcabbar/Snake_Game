import pygame
import random
import os
import sys


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
#To turn the file into .exe

# Initialize PyGame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
NUM_CELLS_WIDTH, NUM_CELLS_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)  # Adjusted light green color
RED = (255, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)

# Snake
snake = [(NUM_CELLS_WIDTH // 2, NUM_CELLS_HEIGHT // 2)]
snake_direction = (1, 0)  # Initial direction (right)
food_eaten = 0

# Food
food = (random.randint(1, NUM_CELLS_WIDTH - 2), random.randint(1, NUM_CELLS_HEIGHT - 2))
life_food = None  # No life food initially

# Score font
font = pygame.font.Font(None, 36)

# Clock to control the game speed
clock = pygame.time.Clock()

# Game state
game_started = False
paused = False
lives = 1  # Initial number of lives

# Start button rectangle
start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)

# Function to draw the start button
def draw_start_button():
    pygame.draw.rect(screen, BLACK, start_button_rect)
    pygame.draw.rect(screen, WHITE, start_button_rect, 3)
    button_text = font.render("Start", True, WHITE)
    screen.blit(button_text, (start_button_rect.centerx - button_text.get_width() // 2,
                              start_button_rect.centery - button_text.get_height() // 2))

# Function to check if the mouse is clicked within the start button
def is_start_button_clicked(mouse_pos):
    return start_button_rect.collidepoint(mouse_pos)

# Function to draw the life counter
def draw_life_counter():
    life_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(life_text, (20, 20))

# Draw snake body and head with white outline
def draw_snake():
    for i, segment in enumerate(snake):
        color = GREEN if i > 0 and i <= food_eaten else LIGHT_GREEN  # Adjust color for snake body segments
        pygame.draw.rect(screen, color, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Draw white outline around each segment
        pygame.draw.rect(screen, WHITE, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Draw score counter at the top-middle of the screen
def draw_score_counter():
    score_text = font.render(f"Score: {food_eaten}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 30))

# Function to draw the life food
def draw_life_food():
    if life_food:
        pygame.draw.rect(screen, PURPLE, (life_food[0] * CELL_SIZE, life_food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused  # Toggle pause state
            elif game_started and not paused:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started and is_start_button_clicked(pygame.mouse.get_pos()):
                game_started = True

    if not game_started:
        # Display the start button if the game hasn't started yet
        draw_start_button()
    elif paused:
        # Display the pause menu if the game is paused
        pause_text = font.render("Paused", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
    else:
        # Draw visible boundaries
        pygame.draw.rect(screen, WHITE, (CELL_SIZE, CELL_SIZE, WIDTH - 2 * CELL_SIZE, HEIGHT - 2 * CELL_SIZE), 2)

        # Move the snake
        head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])

        # Check if snake hits boundaries
        if head[0] <= 0 or head[0] >= NUM_CELLS_WIDTH - 1 or head[1] <= 0 or head[1] >= NUM_CELLS_HEIGHT - 1:
            lives -= 1
            snake = [(NUM_CELLS_WIDTH // 2, NUM_CELLS_HEIGHT // 2)]  # Reset snake position
            snake_direction = (1, 0)  # Reset snake direction
            if lives == 0:
                running = False  # End the game if no lives left
        else:
            snake.insert(0, head)

            # Check for collision with food
            if head == food:
                food_eaten += 1
                food = (random.randint(1, NUM_CELLS_WIDTH - 2), random.randint(1, NUM_CELLS_HEIGHT - 2))

            # Check for collision with life food
            if head == life_food:
                lives += 1
                life_food = None  # Remove the life food from the screen

            # Generate new life food randomly
            if not life_food and random.random() < 0.01:  # Adjust probability as needed
                life_food = (random.randint(1, NUM_CELLS_WIDTH - 2), random.randint(1, NUM_CELLS_HEIGHT - 2))

            # Remove the last segment if the snake didn't eat food
            if len(snake) > 1 and len(snake) > food_eaten + 1:
                snake.pop()

            # Check for collision with itself
            if head in snake[1:]:
                lives -= 1
                snake = [(NUM_CELLS_WIDTH // 2, NUM_CELLS_HEIGHT // 2)]  # Reset snake position
                snake_direction = (1, 0)  # Reset snake direction
                if lives == 0:
                    running = False  # End the game if no lives left

            # Draw food and life food
            pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            draw_life_food()

            # Draw snake
            draw_snake()

            # Draw life counter and score counter
            draw_life_counter()
            draw_score_counter()

            # Control game speed
            clock.tick(10)

    pygame.display.flip()

pygame.quit()
