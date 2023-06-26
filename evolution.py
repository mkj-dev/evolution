import random
import pygame

# Define screen dimensions
WIDTH = 400
HEIGHT = 400

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define the Cell class
class Cell:
    def __init__(self):
        self.health = 100
        self.energy = 100
        self.size = 50
        self.position = [WIDTH // 2, HEIGHT // 2]

    def update(self, food_list):
        self.health -= random.randint(1, 5)
        self.energy -= random.randint(1, 5)
        self.size = max(5, self.size - random.randint(1, 2))

        if len(food_list) > 0:
            closest_food = min(food_list, key=lambda food: self.distance_to_food(food))
            if self.distance_to_food(closest_food) > 0:
                self.move_towards_food(closest_food)

            if self.is_touching_food(closest_food):
                self.health += closest_food.size
                self.energy += closest_food.size
                self.size += closest_food.size
                food_list.remove(closest_food)

    def distance_to_food(self, food):
        return ((self.position[0] - food.position[0]) ** 2 + (self.position[1] - food.position[1]) ** 2) ** 0.5

    def move_towards_food(self, food):
        dx = food.position[0] - self.position[0]
        dy = food.position[1] - self.position[1]

        distance = self.distance_to_food(food)
        speed = min(distance, 10)

        self.position[0] += int(speed * dx / distance)
        self.position[1] += int(speed * dy / distance)

    def is_alive(self):
        return self.health > 0 and self.energy > 0

    def display_info(self):
        print("Health:", self.health)
        print("Energy:", self.energy)

    def display_cell(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0] - self.size // 2, self.position[1] - self.size // 2,
                                       self.size, self.size))

    def is_touching_food(self, food):
        distance = self.distance_to_food(food)
        return distance < (self.size + food.size) / 2

# Define the Food class
class Food:
    def __init__(self):
        self.size = random.randint(5, 10)
        self.position = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        self.color = GREEN

    def display_food(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.size)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cell Evolution")

# Main simulation loop
def simulate_evolution():
    cell = Cell()
    clock = pygame.time.Clock()
    food_list = []
    timer = 0

    while cell.is_alive():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        cell.update(food_list)
        timer += 1

        # Create new food randomly
        if random.random() < 0.25:
            food = Food()
            food_list.append(food)

        screen.fill(WHITE)

        # Display cell information
        font = pygame.font.Font(None, 18)
        text_health = font.render("Health: {}".format(cell.health), True, BLACK)
        text_energy = font.render("Energy: {}".format(cell.energy), True, BLACK)
        text_timer = font.render("Timer: {}".format(timer), True, BLACK)
        
        screen.blit(text_health, (20, 20))
        screen.blit(text_energy, (100, 20))
        screen.blit(text_timer, (180, 20))

        cell.display_cell(screen)

        # Display food
        for food in food_list:
            food.display_food(screen)

        pygame.display.flip()

        clock.tick(1)  # Set the desired frame rate

    # Create an ending screen
    screen.fill(WHITE)

    # Display game over message
    font_large = pygame.font.Font(None, 48)
    text_game_over = font_large.render("Game Over", True, BLACK)
    text_game_over_rect = text_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text_game_over, text_game_over_rect)

    # Display score for the cell
    text_timer = font.render("Your Cell lasted {} seconds.".format(timer), True, BLACK)
    screen.blit(text_timer, (WIDTH // 2 - 80, HEIGHT // 2))

    # Display restart button
    font_small = pygame.font.Font(None, 28)
    text_restart = font_small.render("Restart", True, BLACK)
    text_restart_rect = text_restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    pygame.draw.rect(screen, GREEN, (text_restart_rect.x - 10, text_restart_rect.y - 5,
                                     text_restart_rect.width + 20, text_restart_rect.height + 10))
    screen.blit(text_restart, text_restart_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if text_restart_rect.collidepoint(mouse_pos):
                    # Restart the simulation
                    simulate_evolution()
                    return

# Run the simulation
simulate_evolution()