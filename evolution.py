import random
import pygame

# Define screen dimensions
WIDTH = 400
HEIGHT = 400

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define the Cell class
class Cell:
    def __init__(self):
        self.health = 100
        self.energy = 100
        self.size = 50
        self.position = [WIDTH // 2, HEIGHT // 2]

    def update(self):
        self.health -= random.randint(1, 10)
        self.energy -= random.randint(1, 10)
        self.size = max(0, self.size - random.randint(1, 5))

    def is_alive(self):
        return self.health > 0 and self.energy > 0

    def display_info(self):
        print("Health:", self.health)
        print("Energy:", self.energy)

    def display_cell(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0] - self.size // 2, self.position[1] - self.size // 2,
                                       self.size, self.size))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cell Evolution")

# Main simulation loop
def simulate_evolution():
    cell = Cell()

    clock = pygame.time.Clock()

    while cell.is_alive():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        cell.update()

        screen.fill(WHITE)

        # Display cell information
        font = pygame.font.Font(None, 28)
        text_health = font.render("Health: {}".format(cell.health), True, BLACK)
        text_energy = font.render("Energy: {}".format(cell.energy), True, BLACK)

        screen.blit(text_health, (20, 20))
        screen.blit(text_energy, (20, 60))

        cell.display_cell(screen)

        pygame.display.flip()

        clock.tick(1)  # Set the desired frame rate

    print("The cell has died.")

# Run the simulation
simulate_evolution()
