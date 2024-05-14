import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH, HEIGHT = 300, 300
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Art Cat")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Set the size of each pixel
PIXEL_SIZE = 30

def draw_cat():
    cat_pixels = [
        [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE],
        [WHITE, WHITE, GRAY, GRAY, GRAY, GRAY, WHITE, WHITE],
        [WHITE, GRAY, BLACK, BLACK, BLACK, BLACK, GRAY, WHITE],
        [WHITE, GRAY, BLACK, BLACK, BLACK, BLACK, GRAY, WHITE],
        [WHITE, WHITE, BLACK, BLACK, BLACK, BLACK, WHITE, WHITE],
        [WHITE, WHITE, BLACK, BLACK, BLACK, BLACK, WHITE, WHITE],
        [WHITE, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, WHITE],
        [WHITE, BLACK, BLACK, WHITE, WHITE, BLACK, BLACK, WHITE]
    ]
    for y, row in enumerate(cat_pixels):
        for x, color in enumerate(row):
            pygame.draw.rect(WIN, color, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

# Main loop
def main():
    run = True
    while run:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Fill the window with white
        WIN.fill(WHITE)

        # Draw the cat
        draw_cat()

        # Update the display
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
   
