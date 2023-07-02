import random
import pygame
import math

# Define screen dimensions
WIDTH = 600
HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Define the Cell class
class Cell:
    def __init__(self):
        """
        Initialize a cell with default attributes.
        """
        self.health = 100
        self.energy = 100
        self.size = 50
        self.position = [WIDTH // 2, HEIGHT // 2]
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.num_sides = random.randint(3, 16)  # Random number of sides between 3 and 16

    def update(self, food_list):
        """
        Update the cell's attributes based on its interactions with the environment.
        
        Args:
            food_list (list): List of Food objects in the environment.
        """
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
        """
        Calculate the distance between the cell and a food object.
        
        Args:
            food (Food): The Food object.
        
        Returns:
            float: The distance between the cell and the food object.
        """
        return ((self.position[0] - food.position[0]) ** 2 + (self.position[1] - food.position[1]) ** 2) ** 0.5

    def move_towards_food(self, food):
        """
        Move the cell towards a food object.
        
        Args:
            food (Food): The Food object.
        """
        dx = food.position[0] - self.position[0]
        dy = food.position[1] - self.position[1]

        distance = self.distance_to_food(food)
        speed = min(distance, 10)

        self.position[0] += int(speed * dx / distance)
        self.position[1] += int(speed * dy / distance)

    def is_alive(self):
        """
        Check if the cell is alive based on its health and energy.
        
        Returns:
            bool: True if the cell is alive, False otherwise.
        """
        return self.health > 0 and self.energy > 0

    def is_touching_food(self, food):
        """
        Check if the cell is touching a food object.
        
        Args:
            food (Food): The Food object.
        
        Returns:
            bool: True if the cell is touching the food object, False otherwise.
        """
        distance = self.distance_to_food(food)
        return distance < (self.size + food.size) / 2

    def display(self, screen):
        """
        Display the cell on the screen.

        Args:
            screen (pygame.Surface): The pygame surface representing the screen.
        """
        if self.num_sides > 2:
            if self.num_sides == 4:  # Special case for squares
                pygame.draw.rect(
                    screen,
                    self.color,
                    (self.position[0] - self.size // 2, self.position[1] - self.size // 2, self.size, self.size),
                )
            else:
                radius = self.size // 2
                angle = 2 * math.pi / self.num_sides
                vertices = [
                    (
                        self.position[0] + int(radius * math.cos(i * angle)),
                        self.position[1] + int(radius * math.sin(i * angle)),
                    )
                    for i in range(self.num_sides)
                ]
                pygame.draw.polygon(screen, self.color, vertices)
        else:
            pygame.draw.circle(
                screen,
                self.color,
                self.position,
                self.size // 2,
            )

# Define the Food class
class Food:
    def __init__(self):
        """
        Initialize a food object with random attributes.
        """
        self.size = random.randint(5, 10)
        self.position = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        self.color = GREEN

    def display_food(self, screen):
        """
        Display the food object on the screen.
        
        Args:
            screen (pygame.Surface): The pygame surface representing the screen.
        """
        pygame.draw.circle(screen, self.color, self.position, self.size)

# Define the Generation class
class Generation:
    def __init__(self, population_size):
        """
        Initialize a generation of cells.
        
        Args:
            population_size (int): The number of cells in the generation.
        """
        self.population_size = population_size
        self.cells = []
        self.food_list = []
        self.timer = 0
        self.generation_count = 0

        for _ in range(self.population_size):
            cell = Cell()
            self.cells.append(cell)

    def update(self):
        """
        Update the generation by updating each cell and handling reproduction.
        """
        for cell in self.cells:
            cell.update(self.food_list)

        self.timer += 1

        # Create new food randomly
        if random.random() < 0.25:
            food = Food()
            self.food_list.append(food)

        self.cells = [cell for cell in self.cells if cell.is_alive()]

        if self.generation_count == 0 or len(self.cells) == 0:
            self.reproduce_cells()

    def reproduce_cells(self):
        """
        Reproduce cells to create the next generation with visual changes.
        """
        if len(self.cells) == 0:
            self.cells = [Cell() for _ in range(self.population_size)]
        else:
            parents = random.sample(self.cells, k=min(2, len(self.cells)))

            if len(parents) > 0:  # Check if parents are available
                new_generation = []

                for _ in range(self.population_size):
                    parent = random.choice(parents)
                    child = Cell()

                    # Inherit properties from the parent
                    child.health = parent.health
                    child.energy = parent.energy
                    child.size = parent.size

                    # Modify the color of the child cell
                    child.color = (
                        (parent.color[0] + random.randint(-10, 10)) % 256,
                        (parent.color[1] + random.randint(-10, 10)) % 256,
                        (parent.color[2] + random.randint(-10, 10)) % 256,
                    )

                    new_generation.append(child)

                self.cells = new_generation
        self.generation_count += 1

    def display_info(self, screen):
        """
        Display generation information on the screen.
        
        Args:
            screen (pygame.Surface): The pygame surface representing the screen.
        """
        font = pygame.font.Font(None, 18)
        text_generation = font.render("Generation: {}".format(self.generation_count), True, BLACK)
        text_timer = font.render("Timer: {}".format(self.timer), True, BLACK)

        screen.blit(text_generation, (20, 20))
        screen.blit(text_timer, (180, 20))

    def display_cells(self, screen):
        """
        Display the cells in the generation on the screen.
        
        Args:
            screen (pygame.Surface): The pygame surface representing the screen.
        """
        for cell in self.cells:
            cell.display(screen)

    def display_food(self, screen):
        """
        Display the food objects in the environment on the screen.
        
        Args:
            screen (pygame.Surface): The pygame surface representing the screen.
        """
        for food in self.food_list:
            food.display_food(screen)

    def run_simulation(self):
        """
        Run the simulation.
        """
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cell Evolution")

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            screen.fill(WHITE)

            self.update()

            self.display_info(screen)
            self.display_cells(screen)
            self.display_food(screen)

            pygame.display.flip()

            clock.tick(10)  # Set the desired frame rate


# Define the main function
def main():
    """
    The main function that initializes a generation and runs the simulation.
    """
    generation = Generation(population_size=30)
    generation.run_simulation()

# Run the main function
if __name__ == "__main__":
    main()
