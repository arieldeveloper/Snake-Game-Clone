#########################################
# Programmer: Ariel Chouminov
# Date: 16/11/18
# File Name: snake-main.py
# Description: Very fun snake game, where you are trying to eat good apples and avoiding the bad apples
# in order to get your high score!
#########################################

import pygame
pygame.init()
pygame.display.set_caption('Mario Snake game')
from random import randint
import time

#Sets the current directory to the current file path folder (only needed because mac)
import os
import sys
os.chdir(sys.path[0])

#Variables to ensure nothing runs into itself
horizontal = True
vertical = True

snakeUp = False
snakeDown = False
snakeRight = False
snakeLeft = False

#Game window variables
screenY = 500
screenX  = 700
screen = pygame.display.set_mode((screenX,screenY))
gameOn = False

#Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
outline = 0

snakeList = []

#Fonts
smallText = 15
mediumText = 18
largeText = 40
smallFont = pygame.font.Font("font.ttf", smallText)  # create a variable font
mediumFont = pygame.font.Font("font.ttf", mediumText)  # create a variable font
largeFont = pygame.font.Font("font.ttf", largeText)  # create a variable font
titleFont = pygame.font.Font("titleFont.ttf", largeText + 8)

#Game Speed variables
BODY_SIZE = 15
HSPEED = 15
VSPEED = 15
speedX = 0
speedY = -VSPEED

ghostVertical = False
ghostHorizontal = False

#Score
score = 0

#Mouse
mouse_pos = pygame.mouse.get_pos()

#Game variables that control the screens
introScreen = True
gameScreen = False
gameOverScreen = False
difficulty = None
instructionsScreen = False

#Controls the delay of the game
gameSpeed = 42

#---------------------------------------#
# function that redraws all objects     #
#---------------------------------------#
snakeList = []

#Timer
clock = pygame.time.Clock()
currentTime = 10
clock.tick(60)

#Snake class that draws all the segments
class Snake():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.bodySize = 15

    def create(self, screen):
        rect = self.image.get_rect()
        rect = rect.move((self.x, self.y))
        screen.blit(self.image, rect)

    def reset(self):
        self.x = int(screenX / 2)
        self.y = int(screenY / 2)

#Ghost class
class Ghost():
    def __init__(self):
        self.size = 15
        self.x = randint(0 + self.size, screenX - self.size)
        self.y = randint(0 + self.size, screenY - self.size)
        self.HSPEED = 1
        self.VSPEED = 1
        self.speedX = 0
        self.speedY = -self.VSPEED
    
    
    def show(self, screen, imageLeft, imageRight, head):
        
        imageLeftRect = imageLeft.get_rect()
        imageLeftRect = imageLeftRect.move((self.x, self.y))
        
        imageRightRect = imageRight.get_rect()
        imageRightRect = imageRightRect.move((self.x, self.y))
        
        stop = False
    
        up = False
        down = False
        left = False
        right = False
        
        headX = head.x
        headY = head.y
        
        #Ensures it follows the place where the snake is
        if self.x <= 0:
            right = True
        
        if self.x + self.size >= screenX:
            left = True
            right = False
        
        if self.y <= 0:
            down = True

        if self.y >= screenY:
            up = True

        #If snake is moving horizontally
        if self.x < headX:
            right = True
            left = False

        if self.x > headX:
            left = True
            right = False

        if self.y < headY:
            down = True
            up = False

        if self.y > headY:
            up = True
            down = False

        if up and snakeDown:
            stop = True
        elif down and snakeUp:
            stop = True
        elif right and snakeLeft:
            stop = True
        elif left and snakeRight:
            stop = True
        else:
            stop = False
    
        if left: #Check what side it is on
            self.speedX = -self.HSPEED

        if right:
            self.speedX = self.HSPEED

        if up:
            self.speedY = -self.VSPEED

        if down:
            self.speedY = self.VSPEED
        if right:
            screen.blit(imageRight, imageRightRect)
                
        if left:
            screen.blit(imageLeft, imageLeftRect)

        if not stop:
            self.x += self.speedX
            self.y += self.speedY
    
    #Repositions the ghost
    def rePosition(self):
        self.x = randint(0 + self.size, screenX - self.size)
        self.y = randint(0 + self.size, screenY - self.size)



#Apple class holds all information about bad and good apples
class Apple():
    def __init__(self, size, good):
        self.size = size
        self.x = randint(0 + self.size, screenX - self.size)
        self.y = randint(0 + self.size, screenY - self.size)
        self.clr = WHITE
        self.good = good
    

    def show(self, screen, image):
#        pygame.draw.rect(screen, self.clr, ((self.x, self.y), (self.size, self.size)))
        #Blit the image to the x and the y
        rect = image.get_rect()
        rect = rect.move((self.x, self.y))
        screen.blit(image, rect)
        
    def rePosition(self):
        self.x = randint(0 + self.size, screenX - self.size)
        self.y = randint(0 + self.size, screenY - self.size)

#First apples to start off with
goodApple = Apple(25, True)
badApple = Apple(25, False)
ghost = Ghost()
anotherGhost = Ghost()

#Images
#Obstacles
mushroom = pygame.image.load("mushroom.png").convert_alpha()
mushroom = pygame.transform.scale(mushroom, (goodApple.size, goodApple.size))
goomba = pygame.image.load("goomba.png").convert_alpha()
goomba = pygame.transform.scale(goomba, (badApple.size, badApple.size))
ghostLeft = pygame.image.load("ghost-left.png").convert_alpha()
ghostLeft = pygame.transform.scale(ghostLeft, (ghost.size, ghost.size))
ghostRight = pygame.image.load("Images/ghost-right.png").convert_alpha()
ghostRight = pygame.transform.scale(ghostRight, (ghost.size, ghost.size))
playerBody = pygame.image.load("Images/player-body.png").convert_alpha()
playerBody = pygame.transform.scale(playerBody, (BODY_SIZE, BODY_SIZE))

#Mario Heads
marioHeadLeft = pygame.image.load("mario-left.png").convert_alpha()
marioHeadLeft = pygame.transform.scale(marioHeadLeft, (BODY_SIZE, BODY_SIZE))
marioHeadRight = pygame.image.load("mario-right.png").convert_alpha()
marioHeadRight = pygame.transform.scale(marioHeadRight, (BODY_SIZE, BODY_SIZE))
marioHeadUp = pygame.image.load("mario-up.png").convert_alpha()
marioHeadUp = pygame.transform.scale(marioHeadUp, (BODY_SIZE, BODY_SIZE))
marioHeadDown = pygame.image.load("mario-down.png").convert_alpha()
marioHeadDown = pygame.transform.scale(marioHeadDown, (BODY_SIZE, BODY_SIZE))

#Backgrounds
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (screenX,screenY))
introBackground = pygame.transform.scale(pygame.image.load("intro-background.png"), (screenX, screenY))

#Sound Effects
powerupSound = pygame.mixer.Sound('powerup.wav')   #
powerupSound.set_volume(0.3)

timeWarningSound = pygame.mixer.Sound('time-warning.wav')   #
timeWarningSound.set_volume(0.3)

marioDeadSound = pygame.mixer.Sound('mariodead.wav')   #
marioDeadSound.set_volume(0.3)

gameoverSound = pygame.mixer.Sound('gameover.wav')
gameoverSound.set_volume(0.5)

shrinkingSound = pygame.mixer.Sound('shrink.wav')
shrinkingSound.set_volume(0.5)

enterLevelSound = pygame.mixer.Sound('enter-level.wav')
enterLevelSound.set_volume(0.5)

#Music
ghostHouseMusic = pygame.mixer.Sound('ghosthouse-music.wav')
introMusic = pygame.mixer.Sound('intro-music.wav')

#Put in a first snake to start off with
snakeList = []
firstSnake = Snake(int(screenX / 2), int(screenY / 2), marioHeadRight)
snakeList.append(firstSnake)

#Starts off the intro music
introMusic.play()


def restart():
    global currentTime
    global gameOn
    global horizontal
    global vertical
    global score
    score  -= 1
    currentTime = 10
    gameOn = False
    horizontal = True
    vertical = True
    goodApple.rePosition()
    badApple.rePosition()
    ghost.rePosition()
    anotherGhost.rePosition()

class Button():
    def __init__(self, color, x,y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.underlayColour = (0,0,255)
    
    def draw(self, screen, colour):
        pygame.draw.rect(screen, self.color, (self.x-2,self.y-2,self.width+4,self.height+4))
        
        if self.text != '':
            text = mediumFont.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


instructionsWidth = screenX / 3
instructionsHeight = screenY / 6

instructionsBtnX = screenX / 2 - instructionsWidth / 2
instructionsBtnY = screenY / 2

startButtonSize = screenX / 3
startButtonX = screenX / 4 + startButtonSize / 4
startButtonY = screenY - startButtonSize + screenY / 8

backBtnSize = screenX / 5
backBtnX = screenX / 3 + backBtnSize / 2
backBtnY = screenY - backBtnSize

easyBtnSize = screenX / 5
easyBtnX = screenX / 7 + easyBtnSize / 2
easyBtnY = screenY - easyBtnSize

hardBtnSize = screenX / 5
hardBtnX = screenX / 2 + hardBtnSize / 2
hardBtnY = screenY - hardBtnSize

def instructions():
    global instructionsScreen
    global introScreen
    screen.fill(BLACK)
    
    #Blitting all the intro text on the screen
    
    screen.blit(titleFont.render("Instructions", 1, WHITE),(screenX / 4,50))
    
    screen.blit(smallFont.render("1. Use Arrow Keys to eat mushrooms", 1, WHITE),(screenX / 8,screenY / 4))
    screen.blit(smallFont.render("2. Avoid Goomba's and Ghost's!", 1, WHITE),(screenX / 8,screenY / 3))
    screen.blit(smallFont.render("3. Don't let the time run out!", 1, WHITE),(screenX / 8,screenY / 2 - screenY / 11))
    screen.blit(smallFont.render("4. Avoid touching the borders!", 1, WHITE),(screenX / 8,screenY / 2))

    #Create a start button
    button = Button(WHITE,backBtnX, backBtnY, backBtnSize, backBtnSize / 2, "Go Back")
    button.draw(screen, RED)
    
    if pygame.mouse.get_pressed()[0]:
          mouse = pygame.mouse.get_pos()
          if backBtnX + backBtnSize > mouse[0] > backBtnX and backBtnY + backBtnSize > mouse[1] > backBtnY:
              instructionsScreen = False
              introScreen = True

    pygame.display.update()

def introscreen():
    global introScreen
    global instructionsScreen
    global gameScreen
    global difficulty
    screen.blit(introBackground, (0,0,screenX,screenY))
    textX = screenX / 2
    textY = screenY / 2
    size = 10

    
    #Create a start button
    instructionsBtn = Button(WHITE,instructionsBtnX, instructionsBtnY, instructionsWidth, instructionsHeight, "Instructions")
    instructionsBtn.draw(screen, RED)
    
    #Create a start button
    easyBtn = Button(WHITE,easyBtnX, easyBtnY, easyBtnSize, easyBtnSize / 2, "Easy")
    easyBtn.draw(screen, RED)
    
    #Create a start button
    hardBtn = Button(WHITE,hardBtnX, hardBtnY, hardBtnSize, hardBtnSize / 2, "Hard")
    hardBtn.draw(screen, RED)
    
    #Navigate the buttons on screen
    if pygame.mouse.get_pressed()[0]:
        mouse = pygame.mouse.get_pos()
        if instructionsBtnX + instructionsWidth > mouse[0] > instructionsBtnX and instructionsBtnY + instructionsHeight > mouse[1] > instructionsBtnY:
            introScreen = False
            instructionsScreen = True
    
        #If the user selects easy make it only one ghost
        if easyBtnX + easyBtnSize > mouse[0] > easyBtnX and easyBtnY + easyBtnSize > mouse[1] > easyBtnY:
            difficulty = 0
            enterLevelSound.play()
            ghostHouseMusic.play()
            introScreen = False
            gameScreen = True
            goodApple.rePosition()
            badApple.rePosition()
            ghost.rePosition()
            anotherGhost.rePosition()
            snakeList[0].reset()

        #If the user selects hard, ensure that there is two ghosts
        if hardBtnX + hardBtnSize > mouse[0] > hardBtnX and hardBtnY + hardBtnSize > mouse[1] > hardBtnY:
            difficulty = 1
            enterLevelSound.play()
            ghostHouseMusic.play()
            introScreen = False
            gameScreen = True
            goodApple.rePosition()
            badApple.rePosition()
            ghost.rePosition()
            anotherGhost.rePosition()
            snakeList[0].reset()

    #Blitting all the intro text on the screen
    screen.blit(titleFont.render("Super Mario Snake", 1, WHITE),(screenX / 8,60))
    screen.blit(mediumFont.render("Haunted House Edition!", 1, WHITE),(screenX / 4,screenY / 4))
    
    #Update the screen so everything appears
    pygame.display.update()

def gameOver():
    global introScreen
    global score
    global gameOverScreen
    global snakeList
    global gameSpeed
    global firstSnake
    screen.fill(BLACK)
    size = 10
    
    #Create a start button
    button = Button(WHITE,startButtonX, startButtonY, startButtonSize, startButtonSize / 2, "Play Again!")
    button.draw(screen, RED)
    

    #Blitting all the intro text on the screen
    screen.blit(titleFont.render("Game Over!", 1, WHITE),(screenX / 4,30))
    screen.blit(mediumFont.render("Score: " + str(score), 1, WHITE),(screenX / 3 + 20,screenY / 3))
    
    if pygame.mouse.get_pressed()[0]:
        mouse = pygame.mouse.get_pos()
        
        if startButtonX + startButtonSize > mouse[0] > startButtonX and startButtonY + startButtonSize > mouse[1] > startButtonY:
            gameOverScreen = False
            introScreen = True
            introMusic.play()
            restart()
            score = 0
            snakeList = []
            firstSnake = Snake(int(screenX / 2), int(screenY / 2), marioHeadRight)
            snakeList.append(firstSnake)
            gameSpeed = 40


    #Updating the screen
    pygame.display.update()



def redraw_screen():
    global gameOn
    global vertical
    global horizontal
    global currentTime
    global score
    global gameScreen
    global gameOverScreen
    global gameSpeed
    
    #Blits the background to the screen
    screen.blit(background, (0,0,screenX,screenY))
    
    #Make sure to set some variables to make more difficult if selected
    if difficulty == 1:
        anotherGhost.show(screen, ghostLeft, ghostRight, snakeList[0])
        
        #Collide between snake and the ghost
        
        if pygame.Rect(snakeList[0].x, snakeList[0].y, snakeList[0].bodySize, snakeList[0].bodySize).colliderect(pygame.Rect(anotherGhost.x, anotherGhost.y, anotherGhost.size, anotherGhost.size)):
            marioDeadSound.play()
            gameOverScreen = True
            gameScreen = False

#Shows all the apples and ghost
    goodApple.show(screen, mushroom)
    badApple.show(screen, goomba)
    ghost.show(screen, ghostLeft, ghostRight, snakeList[0])
    tempList = []

    if gameOn:
        if currentTime <= 3 and currentTime >= 2:
            timeWarningSound.play()
    
        if currentTime <= 0:
            #Time ran out, its gameover
            marioDeadSound.play()
            gameOverScreen = True
            gameScreen = False
    
        elif currentTime > 0:
            currentTime -= clock.tick(60) / 1000

    #blit score at the top of the screen
    timeText = smallFont.render("Time Left: " + str(int(currentTime)), 1, WHITE)
    screen.blit(timeText, (screenX / 2, 10))
    
    scoreText = smallFont.render("Score: " + str(score), 1, WHITE)
    screen.blit(scoreText, (screenX / 4, 10))
    
    pygame.display.update()  # position and then update the screen

    clock.tick(60)

    #Draws the snake
    for i in range(len(snakeList)):
        snakeList[i].create(screen)

    #Detecting the collision for good Apple
    if pygame.Rect(snakeList[0].x, snakeList[0].y, snakeList[0].bodySize, snakeList[0].bodySize).colliderect(pygame.Rect(goodApple.x, goodApple.y, goodApple.size, goodApple.size)):
        
        score += 1
        currentTime = 10
        
        goodApple.rePosition()
        badApple.rePosition()
        
        snakeList.append(Snake(snakeList[-1].x, snakeList[-1].y, playerBody))   # assign the same x and y coordinates
        gameSpeed -= 3
        powerupSound.play()

    #Collision of the bad apple
    if pygame.Rect(snakeList[0].x, snakeList[0].y, snakeList[0].bodySize, snakeList[0].bodySize).colliderect(pygame.Rect(badApple.x, badApple.y, badApple.size, badApple.size)):
        
        gameOn = False
        snakeList[-1].reset()
        
        if len(snakeList) > 1:
            shrinkingSound.play()
            snakeList.pop()
            badApple.rePosition()
        else:
            #This is if there is only one snake and it eats a bad apple
            marioDeadSound.play()
            gameOverScreen = True
            gameScreen = False

        restart() #Restarts the timer
            
    #Collide between snake and the ghost
    if pygame.Rect(snakeList[0].x, snakeList[0].y, snakeList[0].bodySize, snakeList[0].bodySize).colliderect(pygame.Rect(ghost.x, ghost.y, ghost.size, ghost.size)):
        marioDeadSound.play()
        gameOverScreen = True
        gameScreen = False

    #Allows the snake to move next to eachother
    for i in range(len(snakeList)-1,0,-1):   # start from the tail, and go backwards:
        
        snakeList[i].x = snakeList[i-1].x               # every segment takes the coordinates
        snakeList[i].y = snakeList[i-1].y

    
    #Moves the snake as long as its in the boundaries
    if snakeList[0].x > 0 and snakeList[0].x < screenX and snakeList[0].y > 0 and snakeList[0].y < screenY and gameOn == True:
        snakeList[0].x += speedX
        snakeList[0].y += speedY
    
    #Kills the snake if the game is on and it hits the boundaries
    elif gameOn == True:
        marioDeadSound.play()
        gameOverScreen = True
        gameScreen = False

    #Detecting if snake hits itself:
    if len(snakeList) > 5:
        for i in range(len(snakeList)-1, 3, -1):
            if pygame.Rect(snakeList[0].x, snakeList[0].y, snakeList[0].bodySize, snakeList[0].bodySize).colliderect(pygame.Rect(snakeList[i].x, snakeList[i].y, snakeList[i].bodySize, snakeList[i].bodySize)):
                
                #Gameover
                marioDeadSound.play()
                gameOverScreen = True
                gameScreen = False

    pygame.display.update()

#---------------------------------------#
# the main program begins here          #
#---------------------------------------#

inPlay = True

while inPlay:
    # check for events
    #pygame.event.get()
    for event in pygame.event.get():    # check for any events
        if event.type == pygame.QUIT:       # If user clicked close
            inPlay = False

#Enters the intro screen
    if introScreen:
        introscreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False

#Enters the intructions screen screen
    if instructionsScreen:
        instructions()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False

#Enters the game screen
    if gameScreen:
        introMusic.stop()
        #key commands for moving the snake
        keys = pygame.key.get_pressed() #the list that contains the keys pressed

        # Variables to ensure that the snake can only go vertically or horizontally one way at a time
        if horizontal:
            if keys[pygame.K_LEFT]:
                speedX = -HSPEED
                speedY = 0
                gameOn = True
                vertical = True
                horizontal = False
                firstSnake.image = marioHeadLeft
            
            
                snakeUp = False
                snakeDown = False
                snakeRight = False
                snakeLeft = True
            

            if keys[pygame.K_RIGHT]:
                speedX = HSPEED
                speedY = 0
                gameOn = True
                vertical = True
                horizontal = False
                firstSnake.image = marioHeadRight

                snakeUp = False
                snakeDown = False
                snakeRight = True
                snakeLeft = False

        if vertical:
            if keys[pygame.K_UP]:
                speedY = -VSPEED
                gameOn = True
                speedX = 0
                vertical = False
                horizontal = True
                snakeUp = True
                snakeDown = False
                snakeRight = False
                snakeLeft = False
                firstSnake.image = marioHeadUp


            if keys[pygame.K_DOWN]:
                speedY = VSPEED
                gameOn = True
                speedX = 0
                vertical = False
                horizontal = True
                firstSnake.image = marioHeadDown
                
                snakeUp = False
                snakeDown = True
                snakeRight = False
                snakeLeft = False

        redraw_screen()
            
    if gameOverScreen:
        ghostHouseMusic.stop()
        gameOver()
        #Allows the game to quit if x is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False


    pygame.time.delay(gameSpeed)
    
pygame.quit()
