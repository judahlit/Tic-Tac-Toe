import pygame

# Hier wordt een nieuwe 2D list aangemaakt
def n2Dlist():
    board = [[0]*3]*3
    return board

# Hier wordt gekeken waar de player heeft geklikt
def inputCheck():
    pygame.event.get()
    if pygame.mouse.get_pressed()[0]:
        input = True
    else:
        input = False
    return input

# Code voor de input van de player
def playerInput(board, blocksize):
    nboard = board
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]

    for counti, i in enumerate(board):
        for countj, j in enumerate(i):
            borderx1 = countj * blocksize
            borderx2 = countj * blocksize + blocksize
            bordery1 = counti * blocksize
            bordery2 = counti * blocksize + blocksize
            if borderx1 < x < borderx2 and bordery1 < y < bordery2 and nboard[counti][countj] == 0:
                nboard[counti][countj] = -1

    npcturn = True
    shown = False
    return nboard

# Hier wordt er gekeken wie heeft gewonnen
def getWinner(board):
    winboard = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    if [1, 1, 1] in winboard:
        return 1

    elif [-1, -1, -1] in winboard:
        return -1
    else:
        return 0

# Hier wordt de beste zet voor de NPC berekend
def miniMax(board, player):
    winner = getWinner(board)
    if winner == player:
        return (0, 0, player)

    move = (-1, -1, -2)
    startmove = move
    score = move[2]

    for counti, i in enumerate(board):
        for countj, j in enumerate(i):
            if board[counti][countj] == 0:
                nboard = board
                nboard[counti][countj] = player
                scoreformove = miniMax(nboard, -player)
                #print(scoreformove)
                if scoreformove[2] > score:
                    score = scoreformove[2]
                    move = (counti, countj, score)

    if move == startmove:
        return 0, 0, 0

    return move

# Hier wordt het speelveld laten zien in een programma
def draw (board, blocksize, wincolor, playertakencolor, npctakencolor):
    countedcols = 0
    winwidth = 0
    winlength = blocksize
    for counti, i in enumerate(board):
        if countedcols == 0:
            for countj, j in enumerate(i):
                winwidth += blocksize

            countedcols = 1
        else:
            winlength += blocksize

    win = pygame.display.set_mode((winwidth, winlength))
    win.fill(wincolor)

    for counti, i in enumerate(board):
        for countj, j in enumerate(i):
            x = countj * blocksize
            y = counti * blocksize
            status = board[counti][countj]
            if status == -1:
                pygame.draw.rect(win, playertakencolor, (x, y, blocksize, blocksize))
            elif status == 1:
                pygame.draw.rect(win, npctakencolor, (x, y, blocksize, blocksize))

    pygame.display.update()

npcturn = True
shown = True
blocksize = 300
wincolor = (0, 0, 0)
playertakencolor = (0, 255, 0)
npctakencolor = (0, 0, 255)

board = n2Dlist()

pygame.init()

while True:

    if not npcturn:
        input = inputCheck()
        if input:
            nboard = playerInput(board, blocksize)
            board = nboard
        npcturn = True
        shown = False

    elif npcturn:
        move = miniMax(board, 1)
        i = move[0]
        j = move[1]
        board[i][j] = 1
        npcturn = False
        shown = False

    if not shown:
        draw(board, blocksize, wincolor, playertakencolor, npctakencolor)
        shown = True

    # Sluit de programma af wanneer Escape ingedrukt is
    key = pygame.key.get_pressed()

    if key[pygame.K_ESCAPE]:
        pygame.quit()
        quit()