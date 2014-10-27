from Pawn import Pawn
from Rook import Rook
from King import King
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from Piece import Piece
from Coordinate import Coordinate as C
from termcolor import colored
import copy

from Move import Move


WHITE = True
BLACK = False

class Board :

    def __init__(self, mateInOne = False, castleBoard = False, pessant = False, promotion = False) :
        self.pieces = []

        if not mateInOne and not castleBoard and not pessant and not promotion:
            self.pieces.extend([Rook(self, BLACK, C(0,7)), Knight(self, BLACK, C(1,7)), Bishop(self, BLACK, C(2,7)), King(self, BLACK, C(3,7)), Queen(self, BLACK, C(4,7)), Bishop(self, BLACK, C(5,7)), Knight(self, BLACK, C(6,7)), Rook(self, BLACK, C(7,7))])
            for x in range(8) :
                self.pieces.append(Pawn(self, BLACK, C(x, 6)))

            for x in range(8) :
                self.pieces.append(Pawn(self, WHITE, C(x, 1)))
            self.pieces.extend([Rook(self, WHITE, C(0,0)), Knight(self, WHITE, C(1,0)), Bishop(self, WHITE, C(2,0)), King(self, WHITE, C(3,0)), Queen(self, WHITE, C(4,0)), Bishop(self, WHITE, C(5,0)), Knight(self, WHITE, C(6,0)), Rook(self, WHITE, C(7,0))])

        elif mateInOne :
            self.boardArray.append([None, None, None, None, None, None, None, None])
            self.boardArray.append([None, None, None, None, None, None, None, None])
            self.boardArray.append([None, None, None, None, None, None, None, None])
            self.boardArray.append([None, None, None, None, None, None, None, None])
            self.boardArray.append([None, None, None, None, None, None, None, None])
            self.boardArray.append([None, None, None, King(self, BLACK), None, None, None, None])
            self.boardArray.append([None, None, None, None, None, None, None, Queen(self, BLACK)])
            self.boardArray.append([None, None, None, King(self, WHITE), None, None, None, None])


        elif castleBoard :
            self.boardArray.append([None, None, None, None, None, None, None, None])
            self.boardArray.append([None, None, None, None, None, None, None, None])
            self.boardArray.append([None, None, None, None, None, None, None, None])
            self.boardArray.append([None, None, None, None, None, None, None, None])
            self.boardArray.append([None, None, None, None, None, None, None, None])
            self.boardArray.append([None, None, None, King(self, BLACK), None, None, None, None])
            self.boardArray.append([None, None, None, None, None, None, None, None])
            self.boardArray.append([Rook(self, WHITE), None, None, None, King(self, WHITE), None, None, None])

        elif pessant :

            #self.boardArray.append([None, None, None, None, None, None, None, None])
            #self.boardArray.append([None, None, Pawn(self, BLACK), None, None, None, None, None])
            #self.boardArray.append([None, None, None, None, None, None, None, None])
            #self.boardArray.append([None, Pawn(self, WHITE), None, None, None, None, None, None])
            #self.boardArray.append([None, None, None, None, None, None, None, None])
            #self.boardArray.append([None, None, None, King(self, BLACK), None, None, None, None])
            #self.boardArray.append([None, None, None, None, None, None, None, None])
            #self.boardArray.append([None, None, None, None, King(self, WHITE), None, None, None])
            pawn = Pawn(self, WHITE, C(1,4))
            pawn2 = Pawn(self, BLACK, C(2,6))
            kingWhite = King(self, WHITE, C(4,0))
            kingBlack = King(self, BLACK, C(3, 2))
            self.pieces.extend([pawn, pawn2, kingWhite, kingBlack])
            self.history = []
            self.currentSide = BLACK
            self.points = 0
            self.movesMade = 0
            self.checkmate = False
            firstMove = Move(C(2,6), C(2,4))
            self.makeMove(firstMove)
            self.currentSide = WHITE
            return
            


        self.history = []

        self.points = 0
        self.currentSide = WHITE
        self.movesMade = 0
        self.checkmate = False





    def __str__(self) :
        return self.makeStringRep(self.pieces)

    def undoLastMove(self) :
        lastMove, pieceTaken = self.history.pop()

        if lastMove.queensideCastle or lastMove.kingsideCastle :
            king = self.pieceAtPosition(lastMove.newPos)
            rook = move.specialMovePiece
            
            self.movePieceToPosition(king, lastMove.oldPos)
            self.movePieceToPosition(rook, move.rookMove.oldPos)

            king.movesMade -= 1
            rook.movesMade -= 1

        elif lastMove.pessant :
            pawnMoved = self.pieceAtPosition(lastMove.newPos)
            pawnTaken = pieceTaken
            self.pieces.append(pawnTaken)
            self.movePieceToPosition(pawnMoved, lastMove.oldPos)
            pawnMoved.movesMade -= 1
            if pawnTaken.side == WHITE :
                self.points += 1
            if pawnTaken.side == BLACK :
                self.points -= 1

        elif lastMove.promotion :
            pass

        else :
            pieceToMoveBack = self.pieceAtPosition(lastMove.newPos)
            self.movePieceToPosition(pieceToMoveBack, lastMove.oldPos)
            if pieceTaken :
                if pieceTaken.side == WHITE :
                    self.points += pieceTaken.value
                if pieceTaken.side == BLACK :
                    self.points -= pieceTaken.value
                self.addPieceToPosition(pieceTaken, lastMove.newPos)
                self.pieces.append(pieceTaken)
            pieceToMoveBack.movesMade -= 1

        self.currentSide = not self.currentSide



    def isCheckmate(self) :
        if len(self.getAllMovesLegal(self.currentSide)) == 0 :
            for move in self.getAllMovesUnfiltered(not self.currentSide) :
                pieceToTake = self.pieceAtPosition(move.newPos)
                if pieceToTake and pieceToTake.stringRep == "K" :
                    return True
        return False
    
    def getLastMove(self) :
        if self.history :
            return self.history[-1][0]

    def getLastPieceMoved(self) :
        if self.history :
            return self.pieceAtPosition(self.history[-1][0].newPos)
    
    def addMoveToHistory(self, move) :
        pieceTaken = None
        if move.pessant :
            pieceTaken = move.specialMovePiece
            self.history.append([move, pieceTaken])
            print("APPENDING PAWN : " + str(pieceTaken) + ' at mem pos : ' + repr(pieceTaken))
            print(self.pieces)
            return
        pieceTaken = self.pieceAtPosition(move.newPos)
        if pieceTaken :
            self.history.append([move, pieceTaken])
            return

        self.history.append([move, None])

    def getCurrentSide(self) :
        return self.currentSide
            
    def makeStringRep(self, pieces) :
        stringRep = ''
        for y in range(7, -1, -1) :
            for x in range(8) :
                piece = None
                for p in pieces :
                    if p.position == C(x, y) :
                        piece = p
                        break
                pieceRep = ''
                if piece :
                    side = piece.side
                    color = 'blue' if side == WHITE else 'red'
                    pieceRep = colored(piece.stringRep, color)
                else :
                    pieceRep = 'x'
                stringRep += pieceRep + ' '
            stringRep += '\n'
        stringRep = stringRep.strip()
        return stringRep

    def rankOfPiece(self, piece) :
        return str(piece.position[1] + 1)


    def fileOfPiece(self, piece) :
        transTable = str.maketrans('01234567', 'abcdefgh')
        return str(piece.position[0]).translate(transTable)


    def getShortNotationOfMove(self, move) :
        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToMove.stringRep != 'p' :
            notation += pieceToMove.stringRep

        if pieceToTake is not None :
            if pieceToMove.stringRep == 'p' :
                notation += self.fileOfPiece(pieceToMove)
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation
    
    def getShortNotationOfMoveWithFile(self, move) :
        #TODO: Use self.getShortNotationOfMove instead of repeating code
        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToMove.stringRep != 'p' :
            notation += pieceToMove.stringRep
            notation += self.fileOfPiece(pieceToMove)

        if pieceToTake is not None :
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation
    
    def getShortNotationOfMoveWithRank(self, move) :
        #TODO: Use self.getShortNotationOfMove instead of repeating code
        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToMove.stringRep != 'p' :
            notation += pieceToMove.stringRep
            notation += self.rankOfPiece(pieceToMove)

        if pieceToTake is not None :
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation

    def getShortNotationOfMoveWithFileAndRank(self, move) :
        #TODO: Use self.getShortNotationOfMove instead of repeating code
        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToMove.stringRep != 'p' :
            notation += pieceToMove.stringRep
            notation += self.fileOfPiece(pieceToMove)
            notation += self.rankOfPiece(pieceToMove)
            

        if pieceToTake is not None :
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation
        return 

    def humanCoordToPosition(self, coord) :
        transTable = str.maketrans('abcdefgh', '12345678')
        coord = coord.translate(transTable)
        coord = [int(c)-1 for c in coord]
        pos = C(coord[0], coord[1])
        return pos
        
    def positionToHumanCoord(self, pos) :
        transTable = str.maketrans('01234567', 'abcdefgh')
        notation = str(pos[0]).translate(transTable) + str(pos[1]+1) 
        return notation

    def isValidPos(self, pos) :
        if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7 :
            return True
        else :
            return False

    def getSideOfMove(self, move) :
        return self.pieceAtPosition(move.oldPos).side

    def getPositionOfPiece(self, piece) :
        for y in range(8) :
            for x in range(8) :
                if self.boardArray[y][x] is piece :
                    return C(x, 7-y)

    def pieceAtPosition(self, pos) :
        for piece in self.pieces :
            if piece.position == pos :
                return piece

    def movePieceToPosition(self, piece, pos) :
        piece.position = pos

    def addPieceToPosition(self, piece, pos) :
        piece.position = pos

    def clearPosition(self, pos) :
        x, y = self.coordToLocationInArray(pos)
        self.boardArray[x][y] = None

        
    def coordToLocationInArray(self, pos) :
        return (7-pos[1], pos[0])

    def locationInArrayToCoord(self, loc) :
        return (loc[1], 7-loc[0])

    def makeMove(self, move) :
        self.addMoveToHistory(move)
        if move.kingsideCastle or move.queensideCastle :
            kingToMove = self.pieceAtPosition(move.oldPos)
            rookToMove = move.specialMovePiece
            self.movePieceToPosition(kingToMove, move.newPos)
            self.movePieceToPosition(rookToMove, move.rookMovePos)
            kingToMove.movesMade += 1
            rookToMove.movesMade += 1

        elif move.pessant :
            pawnToMove = self.pieceAtPosition(move.oldPos)
            pawnToTake = move.specialMovePiece
            pawnToMove.position = move.newPos
            self.pieces.remove(pawnToTake)
            pawnToMove.movesMade += 1

        else :
            pieceToMove = self.pieceAtPosition(move.oldPos)
            pieceToTake = self.pieceAtPosition(move.newPos)

            if pieceToTake :
                if pieceToTake.side == WHITE :
                    self.points -= pieceToTake.value
                if pieceToTake.side == BLACK :
                    self.points += pieceToTake.value
                self.pieces.remove(pieceToTake)
                
            self.movePieceToPosition(pieceToMove, move.newPos)
            pieceToMove.movesMade += 1
        self.movesMade += 1
        self.currentSide = not self.currentSide

    def getPointValueOfSide(self, side) :
        points = 0
        for piece in self.pieces :
            if piece.side == side :
                points += piece.value
        return points

    def getPointAdvantageOfSide(self, side) :
        if side == WHITE :
            return self.points
        if side == BLACK :
            return -self.points
        

    def getAllMovesUnfiltered (self, side, includeKing=True) :
        unfilteredMoves = []
        for piece in self.pieces :
            if piece.side == side :
                if includeKing or piece.stringRep != 'K' :
                    for move in piece.getPossibleMoves() :
                        unfilteredMoves.append(move)
        return unfilteredMoves

    def testIfLegalBoard(self, side) :
        for move in self.getAllMovesUnfiltered(side) :
            pieceToTake = self.pieceAtPosition(move.newPos)
            if pieceToTake and pieceToTake.stringRep == 'K' :
                return False
        return True


    def moveIsLegal(self, move) :
        side = self.pieceAtPosition(move.oldPos).side 
        self.makeMove(move)
        isLegal = self.testIfLegalBoard(not side)
        self.undoLastMove()
        return isLegal  



    def getAllMovesLegal (self, side) :
        unfilteredMoves = list(self.getAllMovesUnfiltered(side))
        legalMoves = []
        for move in unfilteredMoves :
            if self.moveIsLegal(move) :
                legalMoves.append(move)
        return legalMoves


