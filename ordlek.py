import random
import pygame
from pygame.locals import *

pygame.init()
###GLOBAL COLOR VARIABLES###
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
darkgray = (64, 64, 64)

###GLOBAL SCREEN VARIABLE###
screen_width = 1000
screen_height = 720
flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((screen_width, screen_height), flags, vsync=1)

clock = pygame.time.Clock()

###WORDLIST INITIATION FUNCTIONS###
def getKeyword():  # pulls nine-letter keyword from wordlist - this will be the game's usable letters
    f = open(".\eight.csv", encoding="utf-8")
    keywordlist = f.readlines()
    f.close()

    keyword = random.choice(keywordlist)
    return keyword


def getLetterList(keyword):  # converts the keyword into an alphabetically sorted list of characters
    k = keyword
    l = [c for c in k]  # turning keyword into list
    l.pop(-1)  # remove newline character
    l.sort()
    return l


def getAnswerList(keyword):  # pulls a list of all words from the wordlist that can be made using the letters in the keyword
    f = open(".\wordlisteight.csv", encoding="utf-8")
    l = f.readlines()
    f.close()

    wordlist = [i[: -1] for i in l]  # removing newline character
    sollist = []

    for word in wordlist:
        x = isAnagram(keyword, word)
        if x:
            sollist.append(word)

    return sollist


def isAnagram(keyword, targetword):  # determines if a word in the wordlist can be made using the keyword letters
    anagram = True
    keyword = list(keyword)
    for letter in targetword:
        if letter in keyword:
            keyword.remove(letter)
        else:
            anagram = False
            break
    return anagram


def getLengthList(solutionlist):  # creates a list of the length of each word in the solution list for scoring
    lengthlist = []
    for word in solutionlist:
        lengthlist.append(len(word))
    return lengthlist


def initFoundList(answerlist):
    foundlist = []
    for x in answerlist:
        foundlist.append("EMPTY")
    return foundlist


def wordlistInit():
    # keyword/solution list initialization
    answerlist = []
    while len(answerlist) <= 25 or len(answerlist) > 65:
        answerlist = []
        keyword = getKeyword()
        answerlist = getAnswerList(keyword)
    return keyword


###PYGAME DRAWING FUNCTIONS###
def getFont(size):
    return pygame.font.Font('.\Archivo-Bold.ttf', size)


def drawWordRectangles(lengthlist, foundlist):  # draws placeholder rectangles for solutions not yet found
    row = 0
    column = 0
    rectsize = 15
    offset = 5
    wordbackground = pygame.Rect(40,20,screen_width-80,screen_height-220)
    wbgborder = pygame.Rect(40,20,screen_width-80,screen_height-220)
    pygame.draw.rect(surface=screen, rect=wordbackground, color=gray, border_radius=5)
    pygame.draw.rect(surface=screen, rect=wbgborder, width=5, color=green, border_radius=5)
    for wordnumber in range(0, len(lengthlist)):
        entry = lengthlist[wordnumber]
        xpos = 50 + (column * 120)
        ypos = 50 + (row * 40)
        for z in range(1, (entry + 1)):
            blankrect = pygame.Rect((xpos + ((rectsize + offset) * z)), ypos, rectsize, rectsize)
            blankrectborder = pygame.Rect((xpos + ((rectsize + offset) * z)), ypos, rectsize, rectsize)
            if foundlist[wordnumber] == "EMPTY":
                pygame.draw.rect(surface=screen, rect=blankrect, color=green, border_radius=2)
                pygame.draw.rect(surface=screen, rect=blankrectborder, color=black, width=2, border_radius=2)
            else:
                pygame.draw.rect(surface=screen, rect=blankrect, color=gray)
        if row > 10:
            row = 0
            column += 1
        else:
            row += 1


def drawFoundWords(lengthlist, foundlist):  # draws found words on the screen in their place, "filling in the blanks"
    row = 0
    column = 0
    font = getFont(20)

    for entry in range(0, len(lengthlist)):
        answer = foundlist[entry]
        xpos = 70 + (column * 120)
        ypos = 50 + (row * 40)
        if answer != "EMPTY":
            text = font.render(answer, False, black, None)
            textrect = text.get_rect()
            textrect.left = xpos
            textrect.top = ypos
            screen.blit(text, textrect)
        if row > 10:
            row = 0
            column += 1
        else:
            row += 1


def drawKeyletterRectangles(letterlist):  # draws the "rack" of keyword letters
    column = 0
    rectsize = 60
    offset = 10
    font = getFont(50)
    for letter in letterlist:
        xpos = (screen_width / 2) - 250
        ypos = (screen_height - 150)
        text = font.render(letter, True, black, None)
        textrect = text.get_rect()
        blankrect = pygame.Rect(0, 0, rectsize, rectsize)
        blankrectborder = pygame.Rect(0,0,rectsize, rectsize)
        textrect.center = ((xpos + ((rectsize + offset) * column)), ypos)
        blankrect.center = textrect.center
        blankrectborder.center = textrect.center
        pygame.draw.rect(surface=screen, rect=blankrect, color=yellow, border_radius=5)
        pygame.draw.rect(surface=screen, rect=blankrectborder, color=black, border_radius=5, width=2)
        screen.blit(text, textrect)
        column += 1


def drawUserEntryRectangle(userentry):  # draws the user input display
    font = getFont(50)
    blankrect = pygame.Rect(0, 0, 318, 75)
    border = pygame.Rect(0,0,318,75)
    blankrect.center = ((screen_width / 2), (screen_height - 50))
    border.center = blankrect.center
    pygame.draw.rect(surface=screen, rect=blankrect, color=gray, border_radius=5)
    pygame.draw.rect(surface=screen, rect=border, color=green, border_radius=5, width=2)

    text = font.render(userentry, True, green, None)
    textrect = text.get_rect()
    textrect.center = blankrect.center
    screen.blit(text, textrect)


def drawAnswerValue(isword):  # draws notice that word was valid, invalid, or already used, and resets this notice upon entry of a new word
    font = getFont(30)
    rectbottom = (screen_height - 30)
    rectright = (screen_width - 30)

    truetext = font.render("Giltigt ord!", True, green, None)
    truetextrect = truetext.get_rect()
    truetextrect.bottom = rectbottom
    truetextrect.right = rectright

    falsetext = font.render("Ogiltigt ord!", True, red, None)
    falsetextrect = falsetext.get_rect()
    falsetextrect.bottom = rectbottom
    falsetextrect.right = rectright

    alreadytext = font.render("Redan hittat!", True, yellow, None)
    alreadytextrect = alreadytext.get_rect()
    alreadytextrect.bottom = rectbottom
    alreadytextrect.right = rectright

    noticereset = pygame.Rect(screen_width - 350, screen_height - 100, 350, 100)
    pygame.draw.rect(surface=screen, rect=noticereset, color=darkgray)
    if isword == 1:
        screen.blit(truetext, truetextrect)
    elif isword == 2:
        screen.blit(falsetext, falsetextrect)
    elif isword == 3:
        screen.blit(alreadytext, alreadytextrect)

def addScore(userentry):
    score = len(userentry) * 100
    return score

def drawScore(score):
    font = getFont(30)
    rectbottom = (screen_height - 30)
    rectleft = 30
    scorevalue = ("Poäng: " + str(score))
    scoretext = font.render(scorevalue, True, green, None)
    scoretextrect = scoretext.get_rect()
    scoretextrect.bottom = rectbottom
    scoretextrect.left = rectleft
    pygame.draw.rect(surface=screen,rect=scoretextrect, color=darkgray)
    screen.blit(scoretext,scoretextrect)
def main():
    # load and set the logo
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Ordlek")
    screen.fill(color=darkgray)

    # define a variable to control the main loop
    running = True

    # word content items initialization
    keyword = wordlistInit()
    answerlist = getAnswerList(keyword)
    letterlist = getLetterList(keyword)
    lengthlist = getLengthList(answerlist)
    backuplist = getLetterList(keyword)

    # list for keeping track of words already found
    foundlist = initFoundList(answerlist)

    entrybuffer = ""
    userentry = ""
    answerbuffer = []
    score: int = 0

    #hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                               # text='Say Hello',
                                               # manager=manager)
    # main loop
    while running:
        time_delta = clock.tick(60) / 1000.0
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == K_BACKSPACE:
                    if len(userentry) > 0:
                        returntoletterlist = backuplist.index(" ")
                        lettertoreturn = answerbuffer.pop(-1)
                        backuplist[returntoletterlist] = lettertoreturn
                        userentry = userentry[:-1]

                if event.key == K_SPACE:
                    continue

                if event.key == K_RETURN:
                    if userentry in answerlist:
                        if userentry in foundlist:
                            isword = 3
                            drawAnswerValue(isword)
                            backuplist = getLetterList(keyword)
                            userentry = ""
                        else:
                            isword = 1
                            scoreadd: int = addScore(userentry)
                            score += scoreadd
                            drawAnswerValue(isword)
                            d = answerlist.index(userentry)
                            foundlist[d] = userentry
                            backuplist = getLetterList(keyword)
                            userentry = ""
                    else:
                        isword = 2
                        drawAnswerValue(isword)
                        backuplist = getLetterList(keyword)
                        userentry = ""

                if len(userentry) <= 8:
                    entrybuffer += event.unicode.upper()
                    if entrybuffer in backuplist:
                        userentry += entrybuffer
                        answerbuffer.append(entrybuffer)
                        a = backuplist.index(entrybuffer)
                        backuplist[a] = " "
                entrybuffer = ""
        drawWordRectangles(lengthlist, foundlist)
        drawFoundWords(lengthlist, foundlist)
        drawKeyletterRectangles(backuplist)
        drawUserEntryRectangle(userentry)
        drawScore(score)
        pygame.display.update()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
