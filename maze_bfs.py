import pygame
import sys
from collections import deque

pygame.init()

# Window and grid settings
WIDTH, HEIGHT = 600, 650
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Pathfinding Visualizer - BFS and DFS")

font = pygame.font.SysFont("Arial", 22)

# Button class
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, color):
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)
        label = font.render(self.text, True, BLACK)
        screen.blit(label, (self.rect.x + 15, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Initialize buttons
bfs_button = Button(60, 605, 120, 35, "BFS")
dfs_button = Button(240, 605, 120, 35, "DFS")
clear_button = Button(420, 605, 120, 35, "Clear Grid")

# Grid setup
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
start, end = None, None

def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            x, y = j * CELL_SIZE, i * CELL_SIZE
            color = WHITE
            if grid[i][j] == 1:
                color = BLACK
            elif grid[i][j] == 2:
                color = GREEN
            elif grid[i][j] == 3:
                color = RED
            elif grid[i][j] == 4:
                color = BLUE
            elif grid[i][j] == 5:
                color = YELLOW
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE-1, CELL_SIZE-1))
    pygame.draw.line(screen, BLACK, (0, 600), (WIDTH, 600), 3)

def get_clicked_pos(pos):
    x, y = pos
    if y >= 600:
        return None
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

def bfs(start, end):
    q = deque([start])
    visited = {start: None}
    while q:
        current = q.popleft()
        if current == end:
            break
        row, col = current
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            r, c = row+dr, col+dc
            if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] != 1 and (r,c) not in visited:
                visited[(r,c)] = current
                q.append((r,c))
                grid[r][c] = 4
                draw_window()
    reconstruct_path(visited, start, end)

def dfs(start, end):
    stack = [start]
    visited = {start: None}
    while stack:
        current = stack.pop()
        if current == end:
            break
        row, col = current
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            r, c = row+dr, col+dc
            if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] != 1 and (r,c) not in visited:
                visited[(r,c)] = current
                stack.append((r,c))
                grid[r][c] = 4
                draw_window()
    reconstruct_path(visited, start, end)

def reconstruct_path(visited, start, end):
    current = end
    while current and current != start:
        grid[current[0]][current[1]] = 5
        current = visited.get(current)
        draw_window()

def draw_window():
    screen.fill(WHITE)
    draw_grid()
    bfs_button.draw((150, 200, 255))
    dfs_button.draw((150, 255, 200))
    clear_button.draw((255, 200, 200))
    pygame.display.update()
    pygame.time.delay(20)

def clear_grid():
    global grid, start, end
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    start, end = None, None

def main():
    global start, end
    running = True
    while running:
        draw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:  # left click
                pos = pygame.mouse.get_pos()
                cell = get_clicked_pos(pos)
                if not cell:
                    if bfs_button.is_clicked(pos) and start and end:
                        bfs(start, end)
                    elif dfs_button.is_clicked(pos) and start and end:
                        dfs(start, end)
                    elif clear_button.is_clicked(pos):
                        clear_grid()
                    continue
                row, col = cell
                if not start:
                    start = (row, col)
                    grid[row][col] = 2
                elif not end and (row, col) != start:
                    end = (row, col)
                    grid[row][col] = 3
                elif (row, col) != start and (row, col) != end:
                    grid[row][col] = 1
            elif pygame.mouse.get_pressed()[2]:  # right click to erase
                pos = pygame.mouse.get_pos()
                cell = get_clicked_pos(pos)
                if cell:
                    row, col = cell
                    if (row, col) == start:
                        start = None
                    elif (row, col) == end:
                        end = None
                    grid[row][col] = 0

if __name__ == "__main__":
    main()
