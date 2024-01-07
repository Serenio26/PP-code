import pygame
pygame.init()

# Set Frame rate
clock = pygame.time.Clock()
fps = 60

# Game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

# To run window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

# Load images
# Background images
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
# Panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

# Function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))

# Function for panel
def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))

run = True
while run:
    clock.tick(fps)

    # Draw background
    draw_bg()
    # Draw panel
    draw_panel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
