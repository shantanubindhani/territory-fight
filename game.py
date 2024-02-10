import pygame
import sys
import random
import math

color1 = (0, 0, 0)
color2 = (180, 180, 180)

win_width = 700
win_height = 700

x_cell = win_width//10
y_cell = win_height//10

speed = 5

class Player:
    def __init__(self, x, y, color, direction, target_value):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        self.target_value = target_value

    def move(self):
        new_x = self.x + speed * math.cos(self.direction)
        new_y = self.y + speed * math.sin(self.direction)

        # collision with boundry
        if new_x < 0 or new_x > win_width:
            self.direction = math.pi - self.direction
            self.x += speed * math.cos(self.direction)
        elif new_y < 0 or new_y > win_height:
            self.direction = -self.direction
            self.y += speed * math.sin(self.direction)
        else:
            # Check collision with each grid cell
            grid_x = int(new_x / 10)
            grid_y = int(new_y / 10)

            # cell boundry check
            if 0 <= grid_y < len(grid) and 0 <= grid_x < len(grid[0]):
                if grid[grid_y][grid_x] == self.target_value:  # Cell matches target value
                    # Toggle cell value
                    grid[grid_y][grid_x] = not self.target_value
                    
                    # Calculate reflection angle
                    normal_x = grid_x * 10 + 5  # Center of the collided cell
                    normal_y = grid_y * 10 + 5
                    incident_angle = math.atan2(new_y - self.y, new_x - self.x)
                    reflection_angle = 2 * math.atan2(normal_y - self.y, normal_x - self.x) - incident_angle
                    self.direction = reflection_angle

                    self.x += speed * math.cos(self.direction)
                    self.y += speed * math.sin(self.direction)
                else:
                    self.x = new_x
                    self.y = new_y

def draw_grid(window, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(window, color1, (x * 10, y * 10, 10, 10))
            else:
                pygame.draw.rect(window, color2, (x * 10, y * 10, 10, 10))

def draw_players(window, player1, player2):
    pygame.draw.circle(window, player1.color, (int(player1.x), int(player1.y)), 9)
    pygame.draw.circle(window, player2.color, (int(player2.x), int(player2.y)), 9)

def main():
    # Initialize Pygame
    pygame.init()
    global grid
    grid = [[True if(i<(x_cell//2)) else False for i in range(x_cell)] for i in range(y_cell)]

    # Set up the window
    window_size = (win_width, win_height)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Territory Fight!")

    # Create players
    player1 = Player(window_size[0] // 4, window_size[1] // 2, color2, random.uniform(0, 2*math.pi), False)  # Player 1 starts on the left half
    player2 = Player(3 * window_size[0] // 4, window_size[1] // 2, color1, random.uniform(0, 2*math.pi), True)  # Player 2 starts on the right half

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill((255, 255, 255))

        draw_grid(window, grid)

        draw_players(window, player1, player2)

        player1.move()
        player2.move()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
