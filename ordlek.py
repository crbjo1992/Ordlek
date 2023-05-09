import random
import pygame
from pygame.locals import *
import time

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
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Ordlek")
# define a variable to control the main loop
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


# noinspection PyUnusedLocal
def initFoundList(answerlist):
    foundlist = []
    for x in answerlist:
        foundlist.append("EMPTY")
    return foundlist


# noinspection PyUnboundLocalVariable
def wordlistInit():
    # keyword/solution list initialization
    answerlist = []
    while len(answerlist) <= 25 or len(answerlist) > 65:
        keyword = getKeyword()
        answerlist = getAnswerList(keyword)
    return keyword


def checkWin(answerlist, foundlist):
    if foundlist == answerlist:
        return True
    else:
        return False


###PYGAME DRAWING FUNCTIONS###
def getFont(size):
    return pygame.font.Font('.\Archivo-Bold.ttf', size)


def drawTitleScreen():
    big = getFont(150)
    smaller = getFont(60)
    small = getFont(30)
    tiny = getFont(15)
    version = "alpha 1.0, 9 Maj 2023"

    cover = pygame.Rect(0, 0, screen_width, screen_height)
    pygame.draw.rect(surface=screen, rect=cover, color=darkgray)

    title = big.render("ORDLEK", True, green, None)
    titlerect = title.get_rect()
    titlerect.center = ((screen_width // 2), (screen_height - 600))
    screen.blit(title, titlerect)

    subtitle = smaller.render("Ett svenskspråkigt anagramspel", True, green, None)
    subtitlerect = subtitle.get_rect()
    subtitlerect.center = ((screen_width // 2), (screen_height - 500))
    screen.blit(subtitle, subtitlerect)

    desc1 = small.render("Hinner du hitta alla ord innan tiden löper ut?", True, black, None)
    desc1rect = desc1.get_rect()
    desc1rect.center = ((screen_width // 2), (screen_height - 400))
    screen.blit(desc1, desc1rect)

    desc2 = small.render("Skriva ord med tangentbordet och mata in dem med Enter.", True, black, None)
    desc2rect = desc2.get_rect()
    desc2rect.center = ((screen_width // 2), (screen_height - 350))
    screen.blit(desc2, desc2rect)

    start = smaller.render("Starta spelet", True, yellow, None)
    startrect = start.get_rect()
    startwidth = startrect.width + 40
    startheight = startrect.height + 30
    startborder = pygame.Rect(0, 0, startwidth, startheight)
    startrect.center = ((screen_width // 2), (screen_height - 200))
    startborder.center = startrect.center
    screen.blit(start, startrect)
    pygame.draw.rect(surface=screen, rect=startborder, color=white, width=5, border_radius=5)

    contact = tiny.render("Made by Chris, github: crbjo1992", True, white, None)
    contactrect = contact.get_rect()
    contactrect.left = 10
    contactrect.bottom = (screen_height - 10)
    screen.blit(contact, contactrect)

    version = tiny.render(version, True, white, None)
    versionrect = version.get_rect()
    versionrect.right = (screen_width - 10)
    versionrect.bottom = (screen_height - 10)
    screen.blit(version, versionrect)


def drawWordRectangles(lengthlist, foundlist):  # draws placeholder rectangles for solutions not yet found
    row = 0
    column = 0
    rectsize = 15
    offset = 5
    wordbackground = pygame.Rect(40, 20, screen_width - 80, screen_height - 220)
    wbgborder = pygame.Rect(40, 20, screen_width - 80, screen_height - 220)
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
        blankrectborder = pygame.Rect(0, 0, rectsize, rectsize)
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
    border = pygame.Rect(0, 0, 318, 75)
    blankrect.center = ((screen_width / 2), (screen_height - 50))
    border.center = blankrect.center
    pygame.draw.rect(surface=screen, rect=blankrect, color=gray, border_radius=5)
    pygame.draw.rect(surface=screen, rect=border, color=green, border_radius=5, width=2)

    text = font.render(userentry, True, green, None)
    textrect = text.get_rect()
    textrect.center = blankrect.center
    screen.blit(text, textrect)


def drawAnswerValue(
        isword):  # draws notice that word was valid, invalid, or already used, and resets this notice upon entry of a new word
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
    rectbottom = (screen_height - 20)
    rectleft = 30
    scorevalue = ("Poäng: " + str(score))
    scoretext = font.render(scorevalue, True, green, None)
    scoretextrect = scoretext.get_rect()
    scoretextrect.bottom = rectbottom
    scoretextrect.left = rectleft
    pygame.draw.rect(surface=screen, rect=scoretextrect, color=darkgray)
    screen.blit(scoretext, scoretextrect)


def drawTime(current_time):
    font = getFont(30)
    rectbottom = (screen_height - 60)
    rectleft = 30
    timetext = font.render(("Tid kvar: " + str(int(current_time))), True, green, None)
    timetextrect = timetext.get_rect()
    timetextrect.bottom = rectbottom
    timetextrect.left = rectleft
    pygame.draw.rect(surface=screen, rect=timetextrect, color=darkgray)
    screen.blit(timetext, timetextrect)


def drawGameOver(score, win):
    rectwidth = 400
    rectheight = 600

    fontbig = getFont(50)
    fontsmall = getFont(30)

    # game over popup background
    gameoverrect = pygame.Rect(0, 0, rectwidth, rectheight)
    gameoverrect.center = ((screen_width // 2), (screen_height // 2))
    pygame.draw.rect(surface=screen, rect=gameoverrect, color=darkgray, border_radius=5)
    pygame.draw.rect(surface=screen, rect=gameoverrect, color=green, border_radius=5, width=5)

    # text rendering
    if win:
        gotext = fontbig.render("Bra gjort!", True, yellow, None)
    else:
        gotext = fontbig.render("Spelet slut!", True, green, None)
    gotextrect = gotext.get_rect()
    gotextrect.center = ((screen_width // 2), ((screen_height // 2) - 250))
    screen.blit(gotext, gotextrect)

    scoretext = fontsmall.render(("Totalpoäng: " + str(score)), True, green, None)
    scoretextrect = scoretext.get_rect()
    scoretextrect.center = ((screen_width // 2), ((screen_height // 2) - 150))
    screen.blit(scoretext, scoretextrect)

    playagaintext = fontsmall.render("Spela igen?", True, yellow, None)
    patextrect = playagaintext.get_rect()
    patextrect.center = ((screen_width // 2), (screen_height // 2 - 100))
    screen.blit(playagaintext, patextrect)

    pabuttontext = fontsmall.render("Nytt spel", True, green, None)
    pabuttonrect = pabuttontext.get_rect()
    borderwidth = pabuttonrect.width + 40
    borderheight = pabuttonrect.height + 30
    borderrect = pygame.Rect(0, 0, borderwidth, borderheight)
    pabuttonrect.center = ((screen_width // 2), (screen_height // 2))
    borderrect.center = pabuttonrect.center
    screen.blit(pabuttontext, pabuttonrect)
    pygame.draw.rect(surface=screen, rect=borderrect, color=white, width=5, border_radius=5)

    seeboardtext = fontsmall.render("Se slutresultat", True, green, None)
    seeboardrect = seeboardtext.get_rect()
    bwidth = seeboardrect.width + 40
    bheight = seeboardrect.height + 30
    brect = pygame.Rect(0, 0, bwidth, bheight)
    seeboardrect.center = ((screen_width // 2), ((screen_height // 2) + 100))
    brect.center = seeboardrect.center
    screen.blit(seeboardtext, seeboardrect)
    pygame.draw.rect(surface=screen, rect=brect, color=white, width=5, border_radius=5)

    endgametext = fontsmall.render("Stäng spelet", True, green, None)
    endgamerect = endgametext.get_rect()
    borwidth = endgamerect.width + 40
    borheight = endgamerect.height + 30
    borrect = pygame.Rect(0, 0, borwidth, borheight)
    endgamerect.center = ((screen_width // 2), ((screen_height // 2) + 200))
    borrect.center = endgamerect.center
    screen.blit(endgametext, endgamerect)
    pygame.draw.rect(surface=screen, rect=borrect, color=white, width=5, border_radius=5)


def continueButton():
    font = getFont(30)
    conttext = font.render("Fortsätt", True, green, None)
    conrect = conttext.get_rect()
    borderwidth = conrect.width + 40
    borderheight = conrect.height + 30
    borderrect = pygame.Rect(0, 0, borderwidth, borderheight)
    conrect.center = ((screen_width - 175), (screen_height - 50))
    borderrect.center = conrect.center
    screen.blit(conttext, conrect)
    pygame.draw.rect(surface=screen, rect=borderrect, color=white, width=5, border_radius=5)


def main():
    screen.fill(color=darkgray)

    # word content items initialization
    keyword = wordlistInit()
    answerlist = getAnswerList(keyword)
    lengthlist = getLengthList(answerlist)
    backuplist = getLetterList(keyword)
    # list for keeping track of words already found
    foundlist = initFoundList(answerlist)

    # score and user entry variable init
    entrybuffer = ""
    userentry = ""
    answerbuffer = []
    score: int = 0

    # timer init
    start_time = 300
    current_time = start_time
    prev_time = time.time()

    ### GAME FLAGS ###
    # starting screen flag
    isrunning = True
    startgame = False
    timeup = False
    # removes game over menu so players can read the board without exiting
    readboard = False
    continuebutton = False
    win = False

    # main loop
    while isrunning:
        mouse = pygame.mouse.get_pos()
        if not startgame:
            drawTitleScreen()

        # timer countdown
        if startgame:
            current_time -= time.time() - prev_time
            prev_time = time.time()

        if current_time <= 0:
            current_time = 0
            timeup = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isrunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isrunning = False
                if startgame:
                    if not timeup:
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if timeup:
                    if (420 <= mouse[0] <= 580) and (330 <= mouse[1] <= 390):
                        main()
                        isrunning = False
                    if (390 <= mouse[0] <= 610) and (530 <= mouse[1] <= 590):
                        isrunning = False
                    if (380 <= mouse[0] <= 620) and (430 <= mouse[1] <= 490):
                        readboard = True
                        continuebutton = True
                        screen.fill(color=darkgray)
                    if continuebutton:
                        if (750 <= mouse[0] <= 900) and (640 <= mouse[1] <= 700):
                            main()
                            isrunning = False
                if not startgame:
                    if (300 <= mouse[0] <= 700) and (475 <= mouse[1] <= 565):
                        startgame = True
                        screen.fill(color=darkgray)

                entrybuffer = ""
        if startgame:
            drawWordRectangles(lengthlist, foundlist)
            drawFoundWords(lengthlist, foundlist)
            drawKeyletterRectangles(backuplist)
            drawUserEntryRectangle(userentry)
            drawScore(score)
            drawTime(current_time)
            win = checkWin(answerlist, foundlist)
        if win:
            current_time = 0

        if timeup:
            if not readboard:
                drawGameOver(score, win)
            if continuebutton:
                continueButton()
        pygame.display.update()


if __name__ == "__main__":
    main()
