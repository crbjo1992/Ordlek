import os
import sys
import random
import pygame
from pygame.locals import *

#sets path for files to same folder as the python file
os.chdir(os.path.dirname(sys.argv[0]))

###GLOBAL COLOR VARIABLES###
white = (255,255,255)
yellow = (255,255,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
gray = (128,128,128)

###GLOBAL SCREEN VARIABLES###
screen_width = 1280
screen_height = 720
flags = pygame.SCALED
screen = pygame.display.set_mode((screen_width,screen_height), flags, vsync=1)

###WORDLIST INITIATION FUNCTIONS###
def getKeyword(): #pulls eight-letter keyword from wordlist - this will be the game's usable letters
    f = open("eight.csv", encoding="utf-8")
    keywordlist = f.readlines()
    f.close()
    
    keyword = random.choice(keywordlist)
    return keyword

def getLetterList(keyword): #converts the keyword into an alphabetically sorted list of characters
    k = keyword
    l = [c for c in k] #turning keyword into list
    l.pop(-1) #remove newline character
    l.sort()
    return l

def getAnswerList(keyword): #pulls a list of all words from the wordlist that can be made using the letters in the keyword
    f= open("wordlisteight.csv", encoding="utf-8")
    l = f.readlines()
    f.close()
    
    wordlist = [i[: -1] for i in l] #removing newline character
    sollist = []
    
    for word in wordlist:
        x = isAnagram(keyword, word)
        if x == True:
            sollist.append(word)
            
    return sollist
    
def isAnagram(keyword, targetword): #determines if a word in the wordlist can be made using the keyword letters
    anagram = True
    keyword = list(keyword)
    for letter in targetword:
        if letter in keyword:
            keyword.remove(letter)
        else: 
            anagram = False
            break
    return anagram

def getLengthList(solutionlist): #creates a list of the length of each word in the solution list for scoring
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
    #keyword/solution list initialization
    answerlist = []
    while len(answerlist) <= 25 or len(answerlist) > 65:
        answerlist = []
        keyword = getKeyword()
        answerlist = getAnswerList(keyword)
    return keyword

###PYGAME DRAWING FUNCTIONS###
def getFont(size):
    return pygame.font.Font('Archivo-Bold.ttf', size)

def drawWordRectangles(lengthlist, foundlist): #draws placeholder rectangles for solutions not yet found
    row = 0
    column = 0
    rectsize = 20
    offset = 5
    
    for wordnumber in range(0, len(lengthlist)-1):
        entry = lengthlist[wordnumber]
        xpos = 50 + (column * 150)
        ypos = 50 + (row * 40)
        for z in range(1, (entry + 1)):
            blankrect = pygame.Rect((xpos + ((rectsize + offset) * z)), ypos,rectsize,rectsize)
            if foundlist[wordnumber] == "EMPTY":
                pygame.draw.rect(surface=screen,rect=blankrect,color=green)
            else: pygame.draw.rect(surface=screen,rect=blankrect,color=black)
        if row > 10:
            row = 0
            column += 1
        else: row += 1
        
def drawFoundWords(lengthlist, foundlist): #draws found words on the screen in their place, "filling in the blanks"
    row = 0
    column = 0
    font = getFont(30)
    
    for entry in range(0, (len(lengthlist)-1)):
        answer = foundlist[entry]
        xpos = 80 + (column * 150)
        ypos = 50 + (row * 40)
        if answer != "EMPTY":
            text = font.render(answer, False, green, None)
            textrect = text.get_rect()
            textrect.left = xpos
            textrect.top = ypos
            screen.blit (text, textrect)
        if row > 10:
            row = 0
            column += 1
        else: row += 1
        
def drawKeyletterRectangles(letterlist): #draws the "rack" of keyword letters
    column = 0
    rectsize = 60
    offset = 10
    font = getFont(50)
    for letter in letterlist:
            xpos = (screen_width/2) - 250
            ypos = (screen_height - 150)
            text = font.render(letter, True, black, None)
            textrect = text.get_rect()
            blankrect = pygame.Rect(0,0,rectsize,rectsize)
            textrect.center = ((xpos + ((rectsize + offset) * column)),ypos)
            blankrect.center = textrect.center
            pygame.draw.rect(surface=screen,rect=blankrect,color=yellow)
            screen.blit(text,textrect)
            column += 1


def drawUserEntryRectangle(userentry): #draws the user input display
    font = getFont(50)
    blankrect = pygame.Rect(0,0,318,75)
    blankrect.center = ((screen_width/2), (screen_height - 50))
    pygame.draw.rect(surface=screen, rect=blankrect, color=gray)
    
    text = font.render(userentry, True, green, None)
    textrect = text.get_rect()
    textrect.center = blankrect.center
    screen.blit(text, textrect)

def drawAnswerValue(isword): #draws notice that word was valid, invalid, or already used, and resets this notice upon entry of a new word
    font = getFont(50)
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
    
    noticereset = pygame.Rect(screen_width - 350,screen_height - 100,350,100)
    pygame.draw.rect(surface=screen,rect=noticereset,color=black)
    if isword == 1:
        screen.blit(truetext, truetextrect)
    elif isword == 2:
        screen.blit(falsetext, falsetextrect)
    elif isword == 3:
        screen.blit(alreadytext,alreadytextrect)
    
def main():
      # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Ordlek")
     
    # define a variable to control the main loop
    running = True
    
    #word content items initialization
    keyword = wordlistInit()
    answerlist = getAnswerList(keyword)
    letterlist = getLetterList(keyword)
    lengthlist = getLengthList(answerlist)
    backuplist = getLetterList(keyword)
    
    #list for keeping track of words already found
    foundlist = initFoundList(answerlist)

    entrybuffer = ""
    userentry = ""
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                if event.key == K_BACKSPACE:
                    if len(userentry) > 0:
                        backuplist = getLetterList(keyword)
                        userentry = ""
                        
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
                        a = backuplist.index(entrybuffer)
                        backuplist[a] = " "
                entrybuffer = ""
            
        
        drawWordRectangles(lengthlist,foundlist)
        drawFoundWords(lengthlist,foundlist)
        drawKeyletterRectangles(backuplist)
        drawUserEntryRectangle(userentry)
        pygame.display.update()

if __name__=="__main__":
    # call the main function
    main()
