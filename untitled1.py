import pygame
pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Surface Error Example')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create a surface
    surface = pygame.Surface((50, 50))

    # Incorrect: Trying to call the surface as a function
    # This will result in the "pygame.Surface object is not callable" error
    # surface()

    # Correct: Do not use parentheses when using the surface
    # Blit the surface onto the screen
    screen.blit(surface, (100, 100))

    pygame.display.flip()

pygame.quit()