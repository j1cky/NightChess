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

# Store the knight's current position and game data
knight_pos = None
valid_moves = []
past_moves = []
score = 0
player_name = ""  # Variable to store player's name
scoreboard = []  # List to store player scores

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
    global player_name
    input_active = True  # Start with input active
    font = pygame.font.Font(None, 36)

    while True:
        window.fill(BLACK)
        font = pygame.font.SysFont('Helvetica', 70)
        title_text = font.render("Knight's Moves", True, WHITE)

        window.blit(title_text, (WINDOW_SIZE // 2 - title_text.get_width() // 2, 100))



        # Name input
        font = pygame.font.SysFont('Helvetica', 36)
        rules_text = font.render("Set a name", True, WHITE)
        window.blit(rules_text, (WINDOW_SIZE // 2 - title_text.get_width() // 2,200))

        name_input_rect = pygame.Rect(WINDOW_SIZE // 2 - title_text.get_width() // 2, 240, title_text.get_width(), 50)
        pygame.draw.rect(window, WHITE, name_input_rect, 2)
        name_text = font.render(player_name, True, WHITE)
        window.blit(name_text, (name_input_rect.x + 5, name_input_rect.y + 10))

        # Rules
        font = pygame.font.SysFont('Helvetica', 23)
        rules_lines = [
            "Rules are simple,",
            "",
            "*  You move like a Knight!",
            "*  You fill the max!!",
            "*  You don't look back!!"
        ]

        # Render each line and display it
        for i, line in enumerate(rules_lines):
            rules_text = font.render(line, True, WHITE)
            window.blit(rules_text, (WINDOW_SIZE // 2 - title_text.get_width() // 2, 300 + i * 23))

        # Draw the Play button
        font = pygame.font.SysFont('Helvetica', 36, bold=True)
        button_rect = pygame.Rect(WINDOW_SIZE // 2 - title_text.get_width() // 2, 450, title_text.get_width(), 50)
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
                if button_rect.collidepoint(mouse_pos) and player_name:  # Check if Play button clicked and name is not empty
                    return  # Exit the intro screen and start the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  # Remove last character
                elif event.key == pygame.K_RETURN:
                    if player_name:  # Proceed only if there's a name
                        return  # Exit the intro screen and start the game
                else:
                    player_name += event.unicode  # Add new character

        pygame.display.flip()


# Function to display the game over screen
def show_game_over_screen():
    global score, scoreboard
    # Save the player's score
    scoreboard.append((player_name, score))
    # Sort the scoreboard by score in descending order and keep top 3
    scoreboard.sort(key=lambda x: x[1], reverse=True)
    top_scores = scoreboard[:3]

    while True:
        window.fill(BLACK)
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, WHITE)
        window.blit(game_over_text, (WINDOW_SIZE // 2 - game_over_text.get_width() // 2, 100))

        score_text = font.render(f"{player_name}, your score: {score}", True, WHITE)
        window.blit(score_text, (WINDOW_SIZE // 2 - score_text.get_width() // 2, 300))

        # Display top scores
        for i, (name, score) in enumerate(top_scores):
            top_score_text = font.render(f"{i + 1}. {name}: {score}", True, WHITE)
            window.blit(top_score_text, (WINDOW_SIZE // 2 - top_score_text.get_width() // 2, 400 + i * 50))

        # Draw the Play Again button
        button_rect = pygame.Rect(0, 600, WINDOW_SIZE, 50)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, BUTTON_HOVER_COLOR, button_rect)
        else:
            pygame.draw.rect(window, BUTTON_COLOR, button_rect)

        play_again_text = font.render("Play Again", True, BLACK)
        window.blit(play_again_text, (button_rect.x + button_rect.width // 2 - play_again_text.get_width() // 2,
                                       button_rect.y + button_rect.height // 2 - play_again_text.get_height() // 2))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if button_rect.collidepoint(mouse_pos):
                    reset_game()  # Reset the game

        pygame.display.flip()

# Function to reset the game
def reset_game():
    global knight_pos, valid_moves, past_moves, score, player_name
    knight_pos = None
    valid_moves = []
    past_moves = []
    score = 0
    player_name = ""  # Reset player name
    show_intro_screen()  # Show intro screen again

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

            # If the knight can't move anymore, end the game
            if not valid_moves:
                print("No more valid moves. Game over!")
                show_game_over_screen()

    # Draw the chessboard and the knight
    draw_chessboard()
    if knight_pos is not None:
        knight_x, knight_y = knight_pos[1] * SQUARE_SIZE, knight_pos[0] * SQUARE_SIZE
        pygame.draw.circle(window, KNIGHT_COLOR, (knight_x + SQUARE_SIZE // 2, knight_y + SQUARE_SIZE // 2), SQUARE_SIZE // 4)

    pygame.display.flip()
