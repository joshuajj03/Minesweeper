# Minesweeper
# Joshua Jacobson
import pygame, random, sys
from pygame.locals import *


pygame.init()
FPS = 30
WINDOWHEIGHT = 800
WINDOWWIDTH = 800
BORDERHEIGHT = 100
SQUARESWIDE = 40
SQUARESTALL = 35
BOXBORDER = 5
BOXSIZE = (WINDOWWIDTH / 40)
MINEFONT = pygame.font.Font('freesansbold.ttf', 16)
ENDFONT = pygame.font.Font('freesansbold.ttf', 100)
MINEAMOUNT = 50

RED = (192, 0, 0)
YELLOW = (192, 128, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FLAGCOLOR = YELLOW
MINECOLOR = RED
BOXCOLOR = GREY
CLICKEDBOXCOLOR = WHITE
BORDERCOLOR = BLACK


def main():
    global FPSCLOCK, DISPLAYSURF
    GAMEENDED = False
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    NUMCLICKED = 0
    mousex = 0  # used to store x coordinate of mouse event
    mousey = 0  # used to store y coordinate of mouse event
    xbox = -1
    ybox = -1
    pygame.display.set_caption('Minesweeper')
    mineGameboard = mineBoard(MINEAMOUNT)
    while True:  # main game loop
        mouseClicked = False
        mouseRightClicked = False
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_RIGHT:
                    mousex, mousey = event.pos
                    mouseRightClicked = True
                elif event.button == BUTTON_LEFT:
                    mousex, mousey = event.pos
                    mouseClicked = True
        if GAMEENDED == False:
            xbox, ybox = mineGameboard.boxClicked(mousex, mousey)
            if xbox > -1 and ybox > -1 and mouseClicked:
                mineGameboard.recursiveClick(xbox, ybox)
            elif xbox > -1 and ybox > -1 and mouseRightClicked:
                mineGameboard.board[xbox][ybox].flagBox()
            if mineGameboard.board[xbox][ybox].isClicked and mineGameboard.board[xbox][ybox].isBomb == 1 :
                GAMEENDED = True
                mineGameboard.displayAllMines()
                loseText = ENDFONT.render("GAME OVER", True, RED)
                DISPLAYSURF.blit(loseText, (75, 10))
            if mineGameboard.NUMCLICKED == (SQUARESWIDE*SQUARESTALL) - MINEAMOUNT:
                GAMEENDED = True
                winText = ENDFONT.render("You Win", True, YELLOW)
                DISPLAYSURF.blit(winText, (75, 10))


        pygame.display.update()



class mineBoard:

    def __init__(self, mineAmount=200):

        self.NUMCLICKED = 0
        mineTempx = 0
        mineTempy = 100
        self.board = []
        for x in range(SQUARESWIDE):
            mineColumn = []
            for y in range(SQUARESTALL):
                mineColumn.append(mineSquare(mineTempx, mineTempy))
                mineTempy += BOXSIZE
            mineTempy = 100
            mineTempx += BOXSIZE
            self.board.append(mineColumn)
        totalMineNum = mineAmount
        mineRand1 = 0
        mineRand2 = 0
        while (totalMineNum > 0):
            mineRand1 = random.randrange(0, len(self.board) - 1, 1)
            mineRand2 = random.randrange(0, len(self.board[0]) - 1, 1)
            if self.board[mineRand1][mineRand2].isBomb != 1:
                self.board[mineRand1][mineRand2].setBomb()
            totalMineNum -= 1
        mineNum = 0
        self.board[0][0].setMines(self.board[0][1].isBomb + self.board[1][0].isBomb + self.board[1][1].isBomb)
        self.board[len(self.board) - 1][0].setMines(
            self.board[len(self.board) - 1][1].isBomb + self.board[len(self.board) - 2][0].isBomb +
            self.board[len(self.board) - 2][1].isBomb)
        self.board[0][len(self.board[0]) - 1].setMines(
            self.board[0][len(self.board[0]) - 2].isBomb + self.board[1][len(self.board[0]) - 1].isBomb + self.board[1][
                len(self.board[0]) - 2].isBomb)
        self.board[len(self.board[0]) - 1][len(self.board[0]) - 1].setMines(
            self.board[len(self.board[0]) - 1][len(self.board[0]) - 2].isBomb + self.board[len(self.board[0]) - 2][
                len(self.board[0]) - 1].isBomb + self.board[len(self.board[0]) - 2][len(self.board[0]) - 2].isBomb)
        for x in range(1, SQUARESWIDE - 1):
            self.board[x][0].setMines(
                self.board[x][1].isBomb + self.board[x - 1][0].isBomb + self.board[x + 1][0].isBomb + self.board[x - 1][
                    1].isBomb + self.board[x + 1][1].isBomb)
            self.board[x][len(self.board[0]) - 1].setMines(
                self.board[x][len(self.board[0]) - 2].isBomb + self.board[x - 1][len(self.board[0]) - 1].isBomb +
                self.board[x + 1][len(self.board[0]) - 1].isBomb + self.board[x - 1][len(self.board[0]) - 2].isBomb +
                self.board[x + 1][len(self.board[0]) - 2].isBomb)
        for y in range(1, SQUARESTALL - 1):
            self.board[0][y].setMines(
                self.board[1][y].isBomb + self.board[0][y - 1].isBomb + self.board[0][y + 1].isBomb + self.board[1][
                    y - 1].isBomb + self.board[1][y + 1].isBomb)
            self.board[len(self.board) - 1][y].setMines(
                self.board[len(self.board) - 2][y].isBomb + self.board[len(self.board) - 1][y - 1].isBomb +
                self.board[len(self.board) - 1][y + 1].isBomb + self.board[len(self.board) - 2][y - 1].isBomb +
                self.board[len(self.board) - 1][y + 1].isBomb + self.board[len(self.board) - 2][y + 1].isBomb)
        for x in range(1, SQUARESWIDE - 1):
            for y in range(1, SQUARESTALL - 1):
                self.board[x][y].setMines(
                    self.board[x + 1][y].isBomb + self.board[x][y - 1].isBomb + self.board[x][y + 1].isBomb +
                    self.board[x + 1][y - 1].isBomb + self.board[x + 1][y + 1].isBomb + self.board[x - 1][
                        y - 1].isBomb + self.board[x - 1][y + 1].isBomb + self.board[x - 1][y].isBomb)

    def boxClicked(self, xcoord, ycoord):
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y].innerRect.collidepoint(xcoord, ycoord):
                    return x, y
        return -1, -1

    def recursiveClick(self, mineXbox, mineYbox):
        if self.board[mineXbox][mineYbox].isFlagged == False:
            self.board[mineXbox][mineYbox].click()
            self.NUMCLICKED+=1
            if self.board[mineXbox][mineYbox].nearMines == 0:
                if mineXbox > 0 and mineYbox > 0:
                    if self.board[mineXbox - 1][mineYbox - 1].nearMines == 0 and self.board[mineXbox - 1][
                        mineYbox - 1].isClicked == False:
                        self.recursiveClick(mineXbox - 1, mineYbox - 1)
                    elif self.board[mineXbox - 1][mineYbox - 1].isClicked == False:
                        self.board[mineXbox - 1][mineYbox - 1].click()
                        self.NUMCLICKED+=1
                if mineXbox > 0:
                    if self.board[mineXbox - 1][mineYbox].nearMines == 0 and self.board[mineXbox - 1][
                        mineYbox].isClicked == False:
                        self.recursiveClick(mineXbox - 1, mineYbox)
                    elif self.board[mineXbox - 1][mineYbox].isClicked == False:
                        self.board[mineXbox - 1][mineYbox].click()
                        self.NUMCLICKED+=1
                if mineXbox > 0 and mineYbox < SQUARESTALL - 1:
                    if self.board[mineXbox - 1][mineYbox + 1].nearMines == 0 and self.board[mineXbox - 1][
                        mineYbox + 1].isClicked == False:
                        self.recursiveClick(mineXbox - 1, mineYbox + 1)
                    elif self.board[mineXbox - 1][mineYbox + 1].isClicked == False:
                        self.board[mineXbox - 1][mineYbox + 1].click()
                        self.NUMCLICKED+=1
                if mineYbox > 0:
                    if self.board[mineXbox][mineYbox - 1].nearMines == 0 and self.board[mineXbox][
                        mineYbox - 1].isClicked == False:
                        self.recursiveClick(mineXbox, mineYbox - 1)
                    elif self.board[mineXbox][mineYbox - 1].isClicked == False:
                        self.board[mineXbox][mineYbox - 1].click()
                        self.NUMCLICKED+=1
                if mineYbox < SQUARESTALL - 1:
                    if self.board[mineXbox][mineYbox + 1].nearMines == 0 and self.board[mineXbox][
                        mineYbox + 1].isClicked == False:
                        self.recursiveClick(mineXbox, mineYbox + 1)
                    elif self.board[mineXbox][mineYbox + 1].isClicked == False:
                        self.board[mineXbox][mineYbox + 1].click()
                        self.NUMCLICKED+=1
                if mineXbox < SQUARESWIDE - 1 and mineYbox > 0:
                    if self.board[mineXbox + 1][mineYbox - 1].nearMines == 0 and self.board[mineXbox + 1][
                        mineYbox - 1].isClicked == False:
                        self.recursiveClick(mineXbox + 1, mineYbox - 1)
                    elif self.board[mineXbox + 1][mineYbox - 1].isClicked == False:
                        self.board[mineXbox + 1][mineYbox - 1].click()
                        self.NUMCLICKED+=1
                if mineXbox < SQUARESWIDE - 1:
                    if self.board[mineXbox + 1][mineYbox].nearMines == 0 and self.board[mineXbox + 1][
                        mineYbox].isClicked == False:
                        self.recursiveClick(mineXbox + 1, mineYbox)
                    elif self.board[mineXbox + 1][mineYbox].isClicked == False:
                        self.board[mineXbox + 1][mineYbox].click()
                        self.NUMCLICKED+=1
                if mineXbox < SQUARESWIDE - 1 and mineYbox < SQUARESTALL - 1:
                    if self.board[mineXbox + 1][mineYbox + 1].nearMines == 0 and self.board[mineXbox + 1][
                        mineYbox + 1].isClicked == False:
                        self.recursiveClick(mineXbox + 1, mineYbox + 1)
                    elif self.board[mineXbox + 1][mineYbox + 1].isClicked == False:
                        self.board[mineXbox + 1][mineYbox + 1].click()
                        self.NUMCLICKED+=1

    def displayAllMines(self):
        for x in range( SQUARESWIDE - 1):
            for y in range( SQUARESTALL - 1):
                if self.board[x][y].isBomb ==1:
                    self.board[x][y].displayBomb()



class mineSquare:

    def __init__(self, x, y):
        self.xcorner = x
        self.ycorner = y
        self.innerRect = pygame.Rect(x + BOXBORDER, y + BOXBORDER, BOXSIZE - BOXBORDER, BOXSIZE - BOXBORDER)
        self.outerRect = pygame.Rect(x, y, BOXSIZE, BOXSIZE)
        pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, self.outerRect)
        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, self.innerRect)
        self.isFlagged = False
        self.isBomb = 0
        self.isClicked = False
        self.nearMines = 0
        pygame.display.update()

    def setBomb(self):
        self.isBomb = 1

    def flagBox(self):
        if self.isFlagged:
            self.unflagBox()
        else:
            pygame.draw.rect(DISPLAYSURF, FLAGCOLOR, self.innerRect)
            self.isFlagged = True

    def unflagBox(self):
        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, self.innerRect)
        self.isFlagged = False

    def displayBomb(self):
        pygame.draw.rect(DISPLAYSURF, MINECOLOR, self.innerRect)

    def setMines(self, mineNum):
        self.nearMines = mineNum

    def click(self):
        if self.isBomb == 1:

            self.displayBomb()
            self.isClicked = True
        else:
            pygame.draw.rect(DISPLAYSURF, CLICKEDBOXCOLOR, self.innerRect)
            self.isClicked = True
            mineText = MINEFONT.render(str(self.nearMines), True, BLACK)
            DISPLAYSURF.blit(mineText, (self.xcorner + 0.5 * BOXSIZE, self.ycorner + 0.25 * BOXSIZE))


main()
