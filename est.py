import random, pygame, sys
from pygame.locals import *

white = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
WinWid = 800
WinWhe = 500
sizebox = 70
spacesize = 15
colfon = (250, 250, 250)
colors = (red, green, blue, yellow)

def main():
    global fpsclock, display
    pygame.init()
    fpsclock = pygame.time.Clock()
    display = pygame.display.set_mode((WinWid, WinWhe))
    mousex = 0
    mousey = 0
    pygame.display.set_caption('игра')
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)
    firstSelection = None
    display.fill(colfon)
    while True:
        mouseClicked = False
        display.fill(colfon)
        drawBoard(mainBoard, revealedBoxes)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True
                if firstSelection == None:
                    firstSelection = (boxx, boxy)
                else:
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                    if icon1shape != icon2shape or icon1color != icon2color:
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    firstSelection = None
        pygame.display.update()
        fpsclock.tick(60)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(8):
        revealedBoxes.append([val] * 4)
    return revealedBoxes


def getRandomizedBoard():
    icons = []
    for color in colors:
        for shape in range(4):
            icons.append((shape, color))
    random.shuffle(icons)
    numIconsUsed = int(8 * 4 / 2)
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons)
    board = []
    for x in range(8):
        column = []
        for y in range(4):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (sizebox + spacesize) + int((WinWid - (8 * (sizebox + spacesize))) / 2)
    top = boxy * (sizebox + spacesize) + int((WinWhe - (4 * (sizebox + spacesize))) / 2)
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(8):
        for boxy in range(4):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, sizebox, sizebox)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(sizebox * 0.25)
    half = int(sizebox * 0.5)
    left, top = leftTopCoordsOfBox(boxx, boxy)
    if shape == 0:
        pygame.draw.circle(display, color, (left + half, top + half), half - 5)
        pygame.draw.circle(display, colfon, (left + half, top + half), quarter - 5)
    elif shape == 1:
        pygame.draw.rect(display, color, (left + quarter, top + quarter, sizebox - half, sizebox - half))
    elif shape == 2:
        pygame.draw.polygon(display, color, (
            (left + half, top), (left + sizebox - 1, top + half), (left + half, top + sizebox - 1), (left, top + half)))
    elif shape == 3:
        pygame.draw.ellipse(display, color, (left, top + quarter, sizebox, half))


def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(display, colfon, (left, top, sizebox, sizebox))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:  # only draw the cover if there is an coverage
            pygame.draw.rect(display, white, (left, top, coverage, sizebox))
    pygame.display.update()
    fpsclock.tick(60)


def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(sizebox, (-2) - 1, -2):
        drawBoxCovers(board, boxesToReveal, coverage)


def drawBoard(board, revealed):
    for boxx in range(8):
        for boxy in range(4):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(display, white, (left, top, sizebox, sizebox))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


if __name__ == '__main__':
    main()