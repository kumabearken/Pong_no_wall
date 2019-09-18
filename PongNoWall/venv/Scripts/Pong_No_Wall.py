# to do list

import math
import sys
import time
import random
import pygame
from pygame.locals import*
from tkinter import*

# replay window
class RepWindow(Frame):

    def __init__(self,master = NONE):
        Frame.__init__(self,master)
        self.master =master
        self.init_window()

    #creation of init_window
    def init_window(self):

        #change title
        self.master.title("Replay Prompt")

        #widget allowed full space
        self.pack(fill=BOTH, expand=1)

        #create a button
        quitButton = Button(self, text = "Quit",command = self.client_exit)
        replayButton = Button(self, text = "Replay", command = self.replay)

        #placing button
        quitButton.place(x=40, y =250)
        replayButton.place(x=260, y = 250)
    def client_exit(self):
        exit()
    def replay(self):
        root.destroy()

# setup pygame
pygame.init()
fps = pygame.time.Clock()

# setup music
loseSound = pygame.mixer.Sound('lose.ogg')
winSound = pygame.mixer.Sound('win.ogg')
victorySound = pygame.mixer.Sound('victory.ogg')
bounceSound = pygame.mixer.Sound('bounce.ogg')

# setup window
WINDOWWIDTH = 601
WINDOWHEIGHT = 400
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pong_No_Wall')

# setup colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUEISH = (148, 171, 220)

# setup font
fontname = 'freesansbold.ttf'
fontsize = 20
font = pygame.font.Font(fontname, fontsize)

# helper function
def drawnet(win, color, start, end, width=1, length=10):
    x1, y1 = start
    x2, y2 = end
    dl = length

    if x1 == x2:
        ycord = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcord = [x1] * len(ycord)
    elif y1 == y2:
        xcord = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycord = [y1] * len(xcord)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcord = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycord = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)

def printScore():
    antialias = True
    textAI = 'AI'
    textAIScore = 'AI Score is: ' + str(AISCORE)
    textAIRounds = 'AI rounds won is: ' + str(AIROUNDS)
    textPlayer = 'Player'
    textPlayerScore = 'Player Score is: ' + str(PLAYERSCORE)
    textPlayerRounds = 'Player rounds won is: ' + str(PLAYERROUNDS)
    textrenderAI = font.render(textAI,antialias,BLUEISH)
    textrenderPlayer = font.render(textPlayer,antialias,BLUEISH)
    textrenderAIScore = font.render(textAIScore,antialias,BLUEISH)
    textrenderPlayerScore = font.render(textPlayerScore,antialias, BLUEISH)
    textrenderAIRounds = font.render(textAIRounds, antialias,BLUEISH)
    textrenderPlayerRounds = font.render(textPlayerRounds, antialias, BLUEISH)
    window.blit(textrenderAI, (50,50))
    window.blit(textrenderAIScore, (50, 100))
    window.blit(textrenderAIRounds, (50, 150))
    window.blit(textrenderPlayer, (302,50))
    window.blit(textrenderPlayerScore, (302,100))
    window.blit(textrenderPlayerRounds, (302,150))

# setup paddles
PADWIDTH = 100
PADHEIGHT = 25
padAI1 = pygame.Rect(0, WINDOWHEIGHT//2, PADHEIGHT, PADWIDTH)
padImg1 = pygame.image.load('paddle.png')
padImg1 = pygame.transform.scale(padImg1, (PADWIDTH, PADHEIGHT))
padImg1 = pygame.transform.rotate(padImg1, 90)
padAI2 = pygame.Rect(PADHEIGHT + 1, 0, PADWIDTH, PADHEIGHT)
padImg2 = pygame.image.load('paddle.png')
padImg2 = pygame.transform.scale(padImg2, (PADWIDTH, PADHEIGHT))
padAI3 = pygame.Rect(PADHEIGHT+1, WINDOWHEIGHT-PADHEIGHT, PADWIDTH, PADHEIGHT)
padPlayer1 = pygame.Rect(WINDOWWIDTH-PADHEIGHT, WINDOWHEIGHT//2, PADHEIGHT, PADWIDTH)
padPlayer2 = pygame.Rect(WINDOWWIDTH-1-PADWIDTH-PADHEIGHT, 0, PADWIDTH, PADHEIGHT)
padPlayer3 = pygame.Rect(WINDOWWIDTH-1-PADWIDTH-PADHEIGHT, WINDOWHEIGHT-PADHEIGHT, PADWIDTH, PADHEIGHT)

# setup scoring system
AISCORE = 0
PLAYERSCORE = 0
AIROUNDS = 0
PLAYERROUNDS = 0
WIN = False
LOSE = False

#new game reset
def fullreset():
    global WIN
    WIN = False
    global LOSE
    LOSE = False
    global AISCORE
    AISCORE = 0
    global PLAYERSCORE
    PLAYERSCORE= 0
    global AIROUNDS
    AIROUNDS= 0
    global PLAYERROUNDS
    PLAYERROUNDS= 0

# setup direction variables
DOWNLEFT = 'downleft'
DOWNRIGHT = 'downright'
UPLEFT = 'upleft'
UPRIGHT = 'upright'
DirList = [DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT]
ballDir = random.choice(DirList)
SpeedList = [2, 3, 4, 5, 10]
BALLSPEED = random.choice(SpeedList)
BALLPOSX = WINDOWWIDTH//2 - 20
BALLPOSY = WINDOWHEIGHT//2 - 20
BALLPOS = [BALLPOSX, BALLPOSY]
POINTS = 90

class Ball:
    # create a list of points for the ball
    ballPointList = []
    for x in range(0, POINTS):
        ballPointList.append([(BALLPOS[0] + (20*math.cos(x))), (BALLPOS[1] + (20*math.sin(x)))])

    @classmethod
    def drawcircle(cls):
        pygame.draw.circle(window, WHITE, BALLPOS, 20)

    top = BALLPOS[1] - 20
    bottom = BALLPOS[1] + 20
    left = BALLPOS[0] - 20
    right = BALLPOS[0] + 20
    ballVecX = 0
    ballVecY = 0

    if ballDir == DOWNLEFT:
        ballVecX = BALLSPEED * -1
        ballVecY = BALLSPEED * 1
    if ballDir == DOWNRIGHT:
        ballVecX = BALLSPEED * 1
        ballVecY = BALLSPEED * 1
    if ballDir == UPLEFT:
        ballVecX = BALLSPEED * -1
        ballVecY = BALLSPEED * -1
    if ballDir == UPRIGHT:
        ballVecX = BALLSPEED * 1
        ballVecY = BALLSPEED * -1

    @classmethod
    def vector(cls):
        if ballDir == DOWNLEFT:
            cls.ballVecX = BALLSPEED * -1
            cls.ballVecY = BALLSPEED * 1
        if ballDir == DOWNRIGHT:
            cls.ballVecX = BALLSPEED * 1
            cls.ballVecY = BALLSPEED * 1
        if ballDir == UPLEFT:
            cls.ballVecX = BALLSPEED * -1
            cls.ballVecY = BALLSPEED * -1
        if ballDir == UPRIGHT:
            cls.ballVecX = BALLSPEED * 1
            cls.ballVecY = BALLSPEED * -1

    @classmethod
    def update(cls):
        cls.top = BALLPOS[1] - 20
        cls.bottom = BALLPOS[1] + 20
        cls.left = BALLPOS[0] - 20
        cls.right = BALLPOS[0] + 20

    @classmethod
    def reset(cls):
        BALLPOS[0] = WINDOWWIDTH//2 - 20
        BALLPOS[1] = WINDOWHEIGHT//2 - 20

    @classmethod
    def ballpoints(cls):
        cls.ballPointList = []
        for x in range(0, POINTS):
            cls.ballPointList.append([(BALLPOS[0] + (20*math.cos(x))), (BALLPOS[1] + (20*math.sin(x)))])

ballImg = pygame.image.load('ball.png')
ballImg = pygame.transform.scale(ballImg, (40, 40))

# setup keyboard variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6

# game loop
while True:
    # check for quit
    ball = Ball
    printScore()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_LEFT or event.key == K_a:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False
            if event.key == K_x:
                padPlayer1.top = random.randint(0, WINDOWHEIGHT - padPlayer1.height)
                padPlayer1.left = random.randint(0, WINDOWWIDTH - padPlayer1.width)

    # draw black background and lines
    window.fill(BLACK)
    drawnet(window, WHITE, (WINDOWWIDTH//2+1, 0), (WINDOWWIDTH//2+1, WINDOWHEIGHT), length=20)

    # move the paddles
    if moveDown and padPlayer1.bottom < WINDOWHEIGHT:
        padPlayer1.top += MOVESPEED
    if moveUp and padPlayer1.top > 0:
        padPlayer1.top -= MOVESPEED
    if moveLeft and padPlayer2.left > WINDOWWIDTH//2 + 3:
        padPlayer2.left -= MOVESPEED
        padPlayer3.left -= MOVESPEED
    if moveRight and padPlayer2.right < WINDOWWIDTH - PADHEIGHT - 1:
        padPlayer2.right += MOVESPEED
        padPlayer3.right += MOVESPEED

    # ai moves paddle
    AISPEED = 1
    if padAI1.midright[1] < BALLPOS[1]:
        padAI1.bottom +=AISPEED
    if padAI1.midright[1] > BALLPOS[1]:
        padAI1.bottom -= AISPEED
    if (padAI2.midbottom[0] < BALLPOS[0]) and (padAI2.right < WINDOWWIDTH//2):
        padAI2.right += AISPEED
        padAI3.right += AISPEED
    if (padAI2.midbottom[0] > BALLPOS[0]) and (padAI2.left > PADHEIGHT+1):
        padAI2.left -= AISPEED
        padAI3.left -= AISPEED

    # move the ball
    BALLPOS[0] += ball.ballVecX
    BALLPOS[1] += ball.ballVecY
    ball.update()

    # ball hits outside
    if ball.top < 0:
        if WINDOWWIDTH//2+1 > BALLPOS[0]:
            PLAYERSCORE += 1
        else:
            AISCORE += 1
        if (PLAYERSCORE >= 11) and (PLAYERSCORE - AISCORE >= 2):
            winSound.play()
            PLAYERROUNDS += 1
            PLAYERSCORE = 0
            AISCORE = 0
        elif (AISCORE >= 11) and (AISCORE - PLAYERSCORE >= 2):
            AIROUNDS += 1
            loseSound.play()
            PLAYERSCORE = 0
            AISCORE = 0
        if PLAYERROUNDS == 3:
            victorySound.play()
            WIN = True
        elif AIROUNDS == 3:
            LOSE = True
        ball.reset()
        ballDir = random.choice(DirList)
        BALLSPEED = random.choice(SpeedList)
        ball.vector()
    if ball.bottom > WINDOWHEIGHT:
        if WINDOWWIDTH//2+1 > BALLPOS[0]:
            PLAYERSCORE += 1
        else:
            AISCORE += 1
        if (PLAYERSCORE >= 11) and (PLAYERSCORE - AISCORE >= 2):
            winSound.play()
            PLAYERROUNDS += 1
            PLAYERSCORE = 0
            AISCORE = 0
        elif (AISCORE >= 11) and (AISCORE - PLAYERSCORE >= 2):
            AIROUNDS += 1
            loseSound.play()
            PLAYERSCORE = 0
            AISCORE = 0
        if PLAYERROUNDS == 3:
            victorySound.play()
            WIN = True
        elif AIROUNDS == 3:
            LOSE = True
        ball.reset()
        ballDir = random.choice(DirList)
        BALLSPEED = random.choice(SpeedList)
        ball.vector()
    if ball.left < 0:
        if WINDOWWIDTH//2+1 > BALLPOS[0]:
            PLAYERSCORE += 1
        else:
            AISCORE += 1
        if (PLAYERSCORE >= 11) and (PLAYERSCORE - AISCORE >= 2):
            winSound.play()
            PLAYERROUNDS += 1
            PLAYERSCORE = 0
            AISCORE = 0
        elif (AISCORE >= 11) and (AISCORE - PLAYERSCORE >= 2):
            AIRROUNDS += 1
            loseSound.play()
            PLAYERSCORE = 0
            AISCORE = 0
        if PLAYERROUNDS == 3:
            victorySound.play()
            WIN = True
        elif AIROUNDS == 3:
            LOSE = True
        ball.reset()
        ballDir = random.choice(DirList)
        BALLSPEED = random.choice(SpeedList)
        ball.vector()
    if ball.right > WINDOWWIDTH:
        if WINDOWWIDTH // 2 + 1 > BALLPOS[0]:
            PLAYERSCORE += 1
        else:
            AISCORE += 1
        if (PLAYERSCORE >= 11) and (PLAYERSCORE - AISCORE >= 2):
            PLAYERROUNDS += 1
            winSound.play()
            PLAYERSCORE = 0
            AISCORE = 0
        elif (AISCORE >= 11) and (AISCORE - PLAYERSCORE >= 2):
            AIROUNDS += 1
            loseSound.play()
            PLAYERSCORE = 0
            AISCORE = 0
        if PLAYERROUNDS == 3:
            WIN = True
            victorySound.play()
        elif AIROUNDS == 3:
            LOSE = True
        ball.reset()
        ballDir = random.choice(DirList)
        BALLSPEED = random.choice(SpeedList)
        ball.vector()

    # replay prompt
    if WIN or LOSE:
        root = Tk()
        root.geometry("400x300")
        app = RepWindow(root)
        if WIN:
            app = Label(root, text='You won, would you like to play again?')
        if LOSE:
            app = Label(root,text ='You lost, would you like to play again?')
        app.pack()
        fullreset()
        root.mainloop()


    # ball hits paddle
    ball.ballpoints()
    for x in range(0,POINTS):
        if padPlayer1.collidepoint(ball.ballPointList[x]):
            ball.ballVecX *= -1
            bounceSound.play()
    for x in range(0,POINTS):
        if padPlayer2.collidepoint(ball.ballPointList[x]):
            ball.ballVecY *= -1
            bounceSound.play()
    for x in range(0,POINTS):
        if padPlayer3.collidepoint(ball.ballPointList[x]):
            ball.ballVecY *= -1
            bounceSound.play()
    for x in range(0, POINTS):
        if padAI1.collidepoint(ball.ballPointList[x]):
            ball.ballVecX *= -1
            bounceSound.play()
    for x in range(0, POINTS):
        if padAI2.collidepoint(ball.ballPointList[x]):
            ball.ballVecY *= -1
            bounceSound.play()
    for x in range(0, POINTS):
        if padAI3.collidepoint(ball.ballPointList[x]):
            ball.ballVecY *= -1
            bounceSound.play()

    # draw img onto surface
    window.blit(padImg1, padPlayer1)
    window.blit(padImg2, padPlayer2)
    window.blit(padImg2, padPlayer3)
    window.blit(padImg1, padAI1)
    window.blit(padImg2, padAI2)
    window.blit(padImg2, padAI3)
    ball.drawcircle()
    window.blit(ballImg, (BALLPOS[0]-20, BALLPOS[1]-20))
    printScore()

    # draw the window onto the screen
    pygame.display.update()
    fps.tick(40)
