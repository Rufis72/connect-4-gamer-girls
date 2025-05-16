import pygame
import time
import engine
import random
a = time.time()
time.sleep(1)
print(time.time() - a)

# the reason player is random, is so that the bot or player doesn't always go first
player = random.randint(1, 2) # this is the variable for the current player who's turn it is
def switch_player():
    """
    Switches the player from 1 to 2 or from 2 to 1.
    """
    global player
    if player == 1:
        player = 2
    else:
        player = 1
def get_player():
    """
    Returns the current player.
    :return: The current player (1 or 2).
    """
    return player
def get_board():
    """
    Returns the current board.
    :return: The current board.
    """
    return board
def get_piece(column:int):
    """
    Returns the piece at the specified column.
    :param column: The column to get the piece from (0-6).
    :return: The piece at the specified column.
    """
    if column < 0 or column > 7:
        raise ValueError("Column must be between 0 and 6.")
    return board[column]
def get_row(column:int):
    """
    Returns the row at the specified column.
    :param column: The column to get the row from (0-6).
    :return: The row at the specified column.
    """
    if column < 0 or column > 7:
        raise ValueError("Column must be between 0 and 6.")
    row = 5
    while board[column][row] != 0 and row > -1:
        row -= 1
    return row
def get_piece_at(column:int,row:int):
    """
    Returns the piece at the specified column and row.
    :param
    column: The column to get the piece from (0-6).
    :param row: The row to get the piece from (0-5).
    :return: The piece at the specified column and row.
    """
    if column < 0 or column > 7:
        raise ValueError("Column must be between 0 and 6.")
    if row < 0 or row > 5:
        raise ValueError("Row must be between 0 and 5.")
    return board[column][row]

def reset_board():
    """
    Resets the board to its initial state.
    """
    Tokens.update(reset=True)
    global board
    board = [[0 for _ in range(6)] for _ in range(7)]






pygame.init()
screen = pygame.display.set_mode(flags = pygame.FULLSCREEN)
#Basic fullscreenvpygame setup

board_png = pygame.image.load("Board.png")
board_screen = pygame.Surface((182, 156))
Red = pygame.image.load("RedToken.png")
Yellow = pygame.image.load("YellowToken.png")
#

class Token(pygame.sprite.Sprite):
    def __init__(self, color: int, platform: int,column: int):
        super().__init__()
        if color == 1:
            self.image = Red
        elif color == 2:
            self.image = Yellow
        else:
            raise ValueError("Color must be 1 or 2.")
        self.rect = self.image.get_rect()
        self.color = color
        self.position = (column * 26 + 3, 0 )
        self.velocity = 1
        self.rect = self.image.get_rect(bottomleft = self.position)
        self.platform = platform  
        self.reset = False 
        
        

    def update(self, reset: bool = False):
        #if not( self.reset == reset):
        #    velocity = 0
        if reset:
            self.reset = True
            self.velocity = 0
        
        if self.reset:
            self.velocity += 0.75
            self.rect[1] += self.velocity
            
            
            
            
        else:
            self.velocity += 0.75
            self.rect[1] = min(self.rect[1] + self.velocity, self.platform * 26 + 3)
        
        
            
       
        
        
Tokens = pygame.sprite.Group()

run = True
FPS = 30
clock = pygame.time.Clock()
width, height = pygame.display.get_surface().get_size()
board_w,board_h = 182,156
scale_x,scale_y = width / board_w, height / board_h

if scale_x > scale_y:
    size = scale_y * board_w,height
    scale = scale_y
else:
    size = width,scale_x * board_h
    scale = scale_x

padding = (width - size[0])/2,(height - size[1])/2

board = [[0 for _ in range(6)] for _ in range(7)]



def place_piece(column:int, piece: int):
    """
    Places a piece in the board at the specified column.
    :param column: The column to place the piece in (0-6).
    :param piece: The piece to place (one is red two is yellow).
    """
    if column < 0 or column > 7:
        raise ValueError(f"Column must be between 0 and 6. \'{column}\' is not valid")
    if piece not in [1, 2]:
        raise ValueError("Piece must be 1 or 2.")
    row = 5
    while board[column][row] != 0 and row > -1:
        row -= 1
        
    if row == -1:
        return
    
    board[column][row] = piece
    
    Tokens.add(Token(piece, row, column))

    # updating the bot's board
    bot_board_class.move(column)

    # updating the time since player played


# NOTE: The algorithm will also play as player 1
# this is all the logic for the bot
# these are some variables
time_player_played = time.time()
# this specifically is the board state for the bot
bot_board_class = engine.Board()


while run:
    # keeping a stable fps
    clock.tick(FPS)

    # drawing everything onto the screen
    Tokens.update()
    board_screen.fill((0, 0, 0, 0))
    Tokens.draw(board_screen)
    board_screen.blit(board_png, (0, 0))
    screen.blit(pygame.transform.scale(board_screen, size), padding)
    
    # updating the display
    pygame.display.flip()

    # checking if the game is over
    if bot_board_class.eval()[1] != 0:
        # resetting the board
        reset_board()
        # resetting the bot's board
        bot_board_class = engine.Board()
        # resetting the turn (or more accurately making it random
        player = random.randint(1, 2)

    # getting and playing the move for the bot (if it's it's turn)
    # we also check if it's been a short bit since the player played to make the moves easier to see
    if player == 2 and time_player_played + 0.4 < time.time():
        place_playing = bot_board_class.minimax(5, {1: True, 2: False}.get(player))[0]
        place_piece(place_playing, player)
        switch_player()
    
    
    for event in pygame.event.get():
        # quitting the game if the window was closed
        if event.type == pygame.QUIT:
            run = False

        # quitting the game is esc was pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            # checking if it's the algorithm or player's turn
            if player == 1:
                # playing a piece (if a number key was pressed)
                if event.key == pygame.K_1:
                    place_piece(0, player)
                    switch_player()
                    time_player_played = time.time()

                if event.key == pygame.K_2:
                    place_piece(1, player)
                    switch_player()
                    time_player_played = time.time()

                if event.key == pygame.K_3:
                    place_piece(2, player)
                    switch_player()
                    time_player_played = time.time()

                if event.key == pygame.K_4:
                    place_piece(3, player)
                    switch_player()
                    time_player_played = time.time()

                if event.key == pygame.K_5:
                    place_piece(4, player)
                    switch_player()
                    time_player_played = time.time()

                if event.key == pygame.K_6:
                    place_piece(5, player)
                    switch_player()
                    time_player_played = time.time()

                if event.key == pygame.K_7:
                    place_piece(6, player)
                    switch_player()
                    time_player_played = time.time()

            # resetting the board if 'r' was pressed
            if event.key == pygame.K_r:
                # resetting the board
                reset_board()
                # resetting the bot's board
                bot_board_class = engine.Board()
                # resetting the turn (or more accurately making it random
                player = random.randint(1, 2)

