import pygame
import sys
import random

screen_width = 600
screen_height = 600
gridsize = 24
grid_width = screen_width // gridsize
grid_height = screen_height // gridsize

light_green = (0, 170, 140)
dark_green = (0, 140, 120)
food_color = (255, 0, 0)
snake_color = (34, 34, 34)
text_color = (0, 0, 0)

up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)


class SNAKE:
    def __init__(self):
        self.reset()

    def draw(self, surface):
        for p in self.positions:
            rect = pygame.Rect(p, (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, rect)

    def move(self):
        current = self.positions[0]
        x, y = self.direction
        new = (current[0] + (x * gridsize), current[1] + (y * gridsize))

        if new[0] in range(0, screen_width) and new[1] in range(0, screen_height) and new not in self.positions[1:]:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True
        return False
    def reset(self):
        self.length = 1
        self.positions = [(screen_width // 2 // gridsize * gridsize,
                           screen_height // 2 // gridsize * gridsize)]
        self.direction = right
        self.color = snake_color
        self.score = 0
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
    def turn(self, direction):
        # Yılanın geri dönüş hareketini engelle
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        self.direction = direction
class FOOD:
    def __init__(self):
        self.color = food_color  # Yiyeceğin rengi kırmızı
        self.random_position()
    def random_position(self):
        # Yiyeceği gridin içine rastgele bir konumda yerleştirin
        self.position = (random.randint(0, grid_width - 1) * gridsize,
                         random.randint(0, grid_height - 1) * gridsize)
    def draw(self, surface):
        rect = pygame.Rect(self.position, (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, rect)
def drawGrid(surface):
    for y in range(int(grid_height)):
        for x in range(int(grid_width)):
            color = light_green if (x + y) % 2 == 0 else dark_green
            rect = pygame.Rect(x * gridsize, y * gridsize, gridsize, gridsize)
            pygame.draw.rect(surface, color, rect)
def game_over(screen, score):
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, text_color)
    score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, text_color)
    instructions = pygame.font.Font(None, 24).render(
        "Press R to Restart or Q to Quit", True, text_color
    )

    screen.fill((255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 70))
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2))
    instructions_rect = instructions.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)
    screen.blit(instructions, instructions_rect)

    pygame.display.flip()
    pygame.time.wait(2000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Yeniden başlatmak için True döndür
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = SNAKE()
    food = FOOD()

    while True:
        clock.tick(17)
        snake.handle_keys()
        if not snake.move():
            if game_over(screen, snake.score):
                snake.reset()  # Oyun sıfırlanır

        if snake.positions[0] == food.position:
            snake.length += 1
            snake.score += 10  # Skoru 10 artır
            food.random_position()

        drawGrid(surface)
        snake.draw(surface)
        food.draw(surface)

        # Skoru ekranda göstermek için
        score_text = font.render("Score: {0}".format(snake.score), True, (0, 0, 0))
        surface.blit(score_text, (10, 10))

        screen.blit(surface, (0, 0))
        pygame.display.update()

main()
