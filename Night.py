import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_SIZE = 800  # 800x800 window
SQUARE_SIZE = WINDOW_SIZE // 8  # Size of each square in the chessboard
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Knight's Moves")

# Define colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
HIGHLIGHT_COLOR = (0, 200, 50)  # Highlight valid moves
KNIGHT_COLOR = (200, 0, 0)  # Color to represent the knight
BUTTON_COLOR = (100, 150, 255)  # Color for the button
BUTTON_HOVER_COLOR = (150, 200, 255)  # Color when hovering over the button

# Store the knight's current position
knight_pos = None
valid_moves = [(10,10)]
past_moves = []
score = 1

# Create the chessboard
def draw_chessboard():
    for row in range(8):
        for col in range(8):
            # Determine the color of the square
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = BLACK

            # If this square is a valid move, highlight it
            if (row, col) in valid_moves:
                color = HIGHLIGHT_COLOR

            # If this is the knight's position, color it red
            if (row, col) in past_moves:
                color = KNIGHT_COLOR

            pygame.draw.rect(window, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to get the clicked square
def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    return (row, col)

# Function to calculate valid knight moves from a given position
def get_knight_moves(row, col):
    potential_moves = [
        (row + 2, col + 1), (row + 2, col - 1), (row - 2, col + 1), (row - 2, col - 1),
        (row + 1, col + 2), (row + 1, col - 2), (row - 1, col + 2), (row - 1, col - 2)
    ]
    # Filter out moves that are outside the chessboard
    valid = [(r, c) for r, c in potential_moves if 0 <= r < 8 and 0 <= c < 8]
    return valid

# Function to display the intro screen
def show_intro_screen():
    while True:
        window.fill(BLACK)
        font = pygame.font.SysFont("Helvetica", 72)
        title_text = font.render("Knight's Moves", True, WHITE)
        window.blit(title_text, (WINDOW_SIZE // 2 - title_text.get_width() // 2, 100))

        font = pygame.font.Font(None, 36)
        rules_text = font.render("Rules: Click to place the knight.", True, WHITE)
        window.blit(rules_text, (WINDOW_SIZE // 2 - rules_text.get_width() // 2, 300))

        # Draw the Play button
        button_rect = pygame.Rect(0, 600, WINDOW_SIZE, 50)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, BUTTON_HOVER_COLOR, button_rect)
        else:
            pygame.draw.rect(window, BUTTON_COLOR, button_rect)

        play_text = font.render("Play", True, BLACK)
        window.blit(play_text, (button_rect.x + button_rect.width // 2 - play_text.get_width() // 2,
                                 button_rect.y + button_rect.height // 2 - play_text.get_height() // 2))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if button_rect.collidepoint(mouse_pos):
                    return  # Exit the intro screen and start the game

        pygame.display.flip()


# Game loop
show_intro_screen()  # Show the intro screen before the game starts

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the square that was clicked
            clicked_square = get_square_under_mouse()

            # If the knight is not placed yet, place the knight on the first click
            if knight_pos is None:
                knight_pos = clicked_square
                # Calculate valid knight moves from the current position
                valid_moves = get_knight_moves(*knight_pos)
                past_moves = [knight_pos]
                print(f"Knight placed at: {chr(knight_pos[1] + 97)}{8 - knight_pos[0]}")

            # If the knight is placed, allow the player to move to a valid square
            elif clicked_square in valid_moves:
                score += 1
                knight_pos = clicked_square
                past_moves.append(knight_pos)
                # Recalculate valid knight moves
                valid_moves = get_knight_moves(*knight_pos)
                valid_moves = list(filter(lambda move: move not in past_moves, valid_moves))

                print(f"Knight moved to: {chr(knight_pos[1] + 97)}{8 - knight_pos[0]}")

            else:
                print("Invalid move! Choose a valid knight move.")

        if not valid_moves:
            print(f"Game over. You scored = {score}")

    # Draw the chessboard
    draw_chessboard()

    # Update the display
    pygame.display.flip()
