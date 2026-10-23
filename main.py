import pygame
import random
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Sand Simulator (Sandbox)")
clock = pygame.time.Clock()

# Grille de simulation (Cellules)
CELL_SIZE = 8
COLS = WIDTH // CELL_SIZE
ROWS = (HEIGHT - 100) // CELL_SIZE
GRID_OFFSET_Y = 80

# Identifiants des matériaux
# 0: Vide, 1: Sable, 2: Eau, 3: Pierre
EMPTY = 0
SAND = 1
WATER = 2
STONE = 3

# Couleurs des matériaux (Thème Néon & Rétro)
DARK_BG = (15, 18, 25)
PANEL_BG = (25, 30, 42)
COLORS = {
    EMPTY: (15, 18, 25),
    SAND: (255, 200, 50),     # Jaune sablonneux
    WATER: (0, 162, 255),     # Bleu cyan fluide
    STONE: (120, 130, 140)    # Gris pierre solide
}

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 15)

def create_grid():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

grid = create_grid()
current_material = SAND

def update_physics():
    global grid
    new_grid = [row[:] for row in grid]
    
    # Parcourir de bas en haut pour éviter que les éléments ne tombent trop vite d'un coup
    for r in range(ROWS - 2, -1, -1):
        for c in range(COLS):
            cell = grid[r][c]
            
            if cell == EMPTY or cell == STONE:
                continue
                
            # --- PHYSIQUE DU SABLE ---
            if cell == SAND:
                # Tomber tout droit
                if grid[r + 1][c] == EMPTY:
                    new_grid[r][c] = EMPTY
                    new_grid[r + 1][c] = SAND
                # Glisser en diagonale bas-gauche ou bas-droite
                else:
                    dir_list = [-1, 1]
                    random.shuffle(dir_list)
                    moved = False
                    for dc in dir_list:
                        nc = c + dc
                        if 0 <= nc < COLS and grid[r + 1][nc] == EMPTY:
                            new_grid[r][c] = EMPTY
                            new_grid[r + 1][nc] = SAND
                            moved = True
                            break
                            
            # --- PHYSIQUE DE L'EAU ---
            elif cell == WATER:
                # Tomber tout droit
                if grid[r + 1][c] == EMPTY:
                    new_grid[r][c] = EMPTY
                    new_grid[r + 1][c] = WATER
                # Glisser en diagonale
                else:
                    dir_list = [-1, 1]
                    random.shuffle(dir_list)
                    moved = False
                    for dc in dir_list:
                        nc = c + dc
                        if 0 <= nc < COLS and grid[r + 1][nc] == EMPTY:
                            new_grid[r][c] = EMPTY
                            new_grid[r + 1][nc] = WATER
                            moved = True
                            break
                    if not moved:
                        # S'écouler horizontalement (gauche ou droite)
                        for dc in dir_list:
                            nc = c + dc
                            if 0 <= nc < COLS and grid[r][nc] == EMPTY:
                                new_grid[r][c] = EMPTY
                                new_grid[r][nc] = WATER
                                break
                                
    grid = new_grid

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_material = SAND
            elif event.key == pygame.K_2:
                current_material = WATER
            elif event.key == pygame.K_3:
                current_material = STONE
            elif event.key == pygame.K_4:
                current_material = EMPTY  # Gomme
            elif event.key == pygame.K_c:
                grid = create_grid()      # Effacer tout

    # Dessin continu à la souris (maintenir le clic gauche)
    if mouse_pressed[0]:
        x, y = mouse_pos
        if GRID_OFFSET_Y <= y < GRID_OFFSET_Y + ROWS * CELL_SIZE and 0 <= x < WIDTH:
            c = x // CELL_SIZE
            r = (y - GRID_OFFSET_Y) // CELL_SIZE
            # Peindre un petit cercle de matière autour du curseur
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if grid[nr][nc] == EMPTY or current_material == EMPTY:
                            grid[nr][nc] = current_material

    # Mettre à jour la physique des fluides/particules
    update_physics()

    screen.fill(DARK_BG)

    # 1. En-tête et HUD / Barre de sélection
    title_txt = font_medium.render("FALLING SAND SIMULATOR (SANDBOX)", True, (255, 255, 255))
    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 12))

    mat_names = {SAND: "1: Sable", WATER: "2: Eau", STONE: "3: Pierre", EMPTY: "4: Gomme"}
    mat_txt = font_small.render(f"Matière active : {mat_names[current_material]}", True, COLORS[current_material] if current_material != EMPTY else (200, 200, 200))
    screen.blit(mat_txt, (35, 48))

    controls_txt = font_small.render("1-4 : Changer de matière | C : Tout effacer", True, (130, 140, 160))
    screen.blit(controls_txt, (WIDTH - controls_txt.get_width() - 35, 48))

    # 2. Dessin de la grille de simulation
    for r in range(ROWS):
        for c in range(COLS):
            mat = grid[r][c]
            if mat != EMPTY:
                rect = pygame.Rect(c * CELL_SIZE, GRID_OFFSET_Y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLORS[mat], rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()