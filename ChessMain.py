import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = 64
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"C:/Users/jorda/OneDrive/Documents/Coding Files/Jordan EE/pieces/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    loadImages()

    validMoves = gs.getAllValidMoves()
    moveMade = False

    sqSelected = ()
    playerClicks = []

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE

                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []

                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getAllValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()

#highlight the square selected and possible moves for the piece selected
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else'b'): #square selected is their own piece
            #highlight the square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency value -> if 0 completely transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #hightlight moves from that square
            s.fill(p.Color('yellow')) #change colours
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color(139, 0, 0)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
                piece = board[r][c]
                if piece != "--":
                    screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#animating moves
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        #need to erase the piece moved from it's ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece back onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
            #draw the moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()