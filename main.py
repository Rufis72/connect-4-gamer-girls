import pygame
import random



player = 1 #Detirmins the
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



def place_piece(column:int,piece: int):
    """
    Places a piece in the board at the specified column.
    :param column: The column to place the piece in (0-6).
    :param piece: The piece to place (one is red two is yellow).
    """
    if column < 0 or column > 7:
        raise ValueError("Column must be between 0 and 6.")
    if piece not in [1, 2]:
        raise ValueError("Piece must be 1 or 2.")
    row = 5
    while board[column][row] != 0 and row > -1:
        row -= 1
        
    if row == -1:
        return
    
    board[column][row] = piece
    
    Tokens.add(Token(piece, row, column))
    



while run:
    #Draw the tokens on the board
    
    
               
    player = random.choice([1, 2])
    
    clock.tick(FPS)
   
    screen.fill((255, 255, 255))
    
    Tokens.update()
    board_screen.fill((0, 0, 0, 0))
    Tokens.draw(board_screen)
    board_screen.blit(board_png, (0, 0))
    screen.blit(pygame.transform.scale(board_screen, size), padding)
    
    
    pygame.display.flip()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_1:
                place_piece(0, player)
            if event.key == pygame.K_2:
                place_piece(1, player)
            if event.key == pygame.K_3:
                place_piece(2, player)  
            if event.key == pygame.K_4:
                place_piece(3, player)
            if event.key == pygame.K_5:
                place_piece(4, player)
            if event.key == pygame.K_6:
                place_piece(5, player)
            if event.key == pygame.K_7:
                place_piece(6, player)
            if event.key == pygame.K_r:
                
                reset_board()

