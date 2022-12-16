class GameState(): #finished moves, pins, checks, double checks today
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () #will be the coordiantes where an en passent capture is possible
        self.currentCasltingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCasltingRight.wks, self.currentCasltingRight.bks, self.currentCasltingRight.wqs, self.currentCasltingRight.bqs)]

        self.moveFunctions = {
            'p' : self.getPawnMoves,
            'R' : self.getRookMoves,
            'N' : self.getKnightMoves,
            'B' : self.getBishopMoves,
            'Q' : self.getQueenMoves,
            'K' : self.getKingMoves
            }

    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.endRow + move.startRow)//2, move.endCol)
        else:
            self.enpassantPossible = ()
        #if en passant move, must update the board to capture the pawn
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"
        #if pawn promotion change piece
        if move.pawnPromotion:
            promotedPiece = input("Promote to Q, R, B, or N:") #we can make this part of the ui later
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCasltingRight.wks, self.currentCasltingRight.bks, self.currentCasltingRight.wqs, self.currentCasltingRight.bqs))

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            #undo a 2 square pawn advance
            if move.pieceMoved[1] =='p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

    def getAllValidMoves(self):
        moves = []
        tempCastleRights = CastleRights(self.currentCasltingRight.wks, self.currentCasltingRight.bks, self.currentCasltingRight.wqs, self.currentCasltingRight.bqs)
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: #single check, can be blocked or piece taken
                moves = self.getAllPossibleMoves()
                check = self.checks[0] #check information from checkForPinsAndChecks function later on
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] #which enemy piece is causing the check
                validSquares = [] #creating a list where pieces can move to
                if pieceChecking[1] == "N": #Because if the piece checking is a knight you must either take it or move king
                    validSquares = [(checkRow, checkCol)] #the only place a piece can move to is the knight
                else: #any other piece but a knight
                    for i in range(1, 8):
                        validSquare = (kingRow +check[2] * i, kingCol + check[3] * i) #you can continue moving closer and closer to the attacking piece
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: #once you arrive at the attacking piece you can take and break the loop
                            break 
                for i in range(len(moves) - 1, -1, -1): #go through the list backwards
                    if moves[i].pieceMoved[1] != "K": #check if it isn't the king moving
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: #check if the move blocks or takes the check
                            moves.remove(moves[i]) #if the king does not move and nothing else blocks or captures it is removed from the list
            else: #double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: #no checks, all moves are fine
            moves = self.getAllPossibleMoves()
        
        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        self.currentCasltingRight = tempCastleRights
        return moves
    
#    def checkingChecks(self):
#        if self.whiteToMove:
#            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
#        else:
#            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
#
#    def squareUnderAttack(self, r, c):
#        self.whiteToMove = not self.whiteToMove
#        oppMoves = self.getAllPossibleMoves()
#        self.whiteToMove = not self.whiteToMove
#        for move in oppMoves:
#            if move.endRow == r and move.endCol == c:
#                return True
#        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]

                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'

        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
        pawnPromotion = False

        if self.board[r+moveAmount][c] == "--":
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r+moveAmount == backRow:
                    pawnPromotion = True
                moves.append(Move((r, c), (r+moveAmount, c), self.board, pawnPromotion=pawnPromotion))
                if r == startRow and self.board[r+2*moveAmount][c] == "--":
                    moves.append(Move((r, c), (r+2*moveAmount, c), self.board))
        if c-1 >= 0:
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r+moveAmount, c-1), self.board, pawnPromotion=pawnPromotion))
                if (r + moveAmount, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c-1), self.board, isEnpassantMove=True))
        if c+1 <= 7:
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r+moveAmount, c+1), self.board, pawnPromotion=pawnPromotion))
                if (r + moveAmount, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+moveAmount, c+1), self.board, isEnpassantMove=True))

#            if self.whiteToMove:
#            if self.board[r-1][c] == "--":
#               if not piecePinned or pinDirection == (-1, 0):
#                    moves.append(Move((r,c), (r-1, c), self.board))
#                    if r == 6 and self.board[r-2][c] == "--":
#                        moves.append(Move((r,c), (r-2, c), self.board))
#
#            if c-1 >= 0:
#                if self.board[r-1][c-1][0] == 'b':
#                    if not piecePinned or pinDirection == (-1, -1):
#                        moves.append(Move((r,c), (r-1, c-1), self.board))
#                elif (r-1, c-1) == self.enpassantPossible:
#                    moves.append(Move((r,c), (r-1, c-1), self.board, isEnpassantMove = True))
#
#            if c+1 <= 7:
#                if self.board[r-1][c+1][0] == 'b':
#                    if not piecePinned or pinDirection == (-1, 1):
#                        moves.append(Move((r,c), (r-1, c+1), self.board))
#                elif (r-1, c+1) == self.enpassantPossible:
#                    moves.append(Move((r,c), (r-1, c+1), self.board, isEnpassantMove = True))
#
#        else:
#            if self.board[r+1][c] == "--":
#                if not piecePinned or pinDirection == (1, 0):
#                    moves.append(Move((r,c), (r+1, c), self.board))
#
#                    if r == 1 and self.board[r+2][c] == "--":
#                        moves.append(Move((r,c), (r+2, c), self.board))
#
#                if c-1 >= 0:
#                    if self.board[r+1][c-1][0] == 'w':
#                        if not piecePinned or pinDirection == (1, -1):
#                            moves.append(Move((r,c), (r+1, c-1), self.board))
#                    elif (r+1, c-1) == self.enpassantPossible:
#                        moves.append(Move((r,c), (r+1, c-1), self.board, isEnpassantMove = True))
#
#                if c+1 <= 7:
#                    if self.board[r-1][c+1][0] == 'w':
#                        if not piecePinned or pinDirection == (1, 1):
#                            moves.append(Move((r,c), (r+1, c+1), self.board))
#                    elif (r+1, c+1) == self.enpassantPossible:
#                        moves.append(Move((r,c), (r+1, c+1), self.board, isEnpassantMove = True))

    
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            piecePinned = True
            pinDirection = (self.pins[i][2], self.pins[i][3])
            if self.board[r][c][1] != "Q": #because our queen moves are generated based on rook moves
                self.pins.remove(self.pins[i])
            break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]

                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))

                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))

                        else:
                            break

                    else: 
                        break

                else:
                    break

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, 1), (-2, -1), (-1, 2), (1, 2), (-1, -2), (1, -2), (-2, 1), (-2, -1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range (len(self.pins)-1, -1, -1):
            piecePinned = True
            pinDirection = (self.pins[i][2], self.pins[i][3])
            self.pins.remove(self.pins[i])
            break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break
        
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == "w":
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    if allyColor == "w":
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        self.getCastleMoves(r, c, moves)

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != "K": #and statement is because in the find king moves we 'ghost' move the king so there is a phantom king that the function will detect and call check on
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == "R") or \
                                (4 <= j <= 7 and type == "B") or \
                                (i == 1 and type == "p" and ((enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or \
                                (type == "Q") or (i == 1 and type == "K"):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N":
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    def getCastleMoves(self, r, c, moves):
        if self.inCheck():
            return #no castle when in check
        if (self.whiteToMove and self.currentCasltingRight.wks) or (not self.whiteToMove and self.currentCasltingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCasltingRight.wqs) or (not self.whiteToMove and self.currentCasltingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.inCheck(r, c+1) and not self.inCheck(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove = True))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.inCheck(r, c-1) and not self.inCheck(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():

    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, pawnPromotion = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]

        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #pawn promotion
        self.pawnPromotion = pawnPromotion
        #pawn en passant
        self.isEnpassantMove = isEnpassantMove
        self.isCastleMove = isCastleMove
        if isEnpassantMove:
            self.pieceCaptured = 'bp' if self.pieceMoved == 'wp' else 'wp'

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]