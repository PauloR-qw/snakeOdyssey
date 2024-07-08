from operator import contains
from classes.Data import Data
from classes.Fruit import Fruit
from classes.Snake import Snake
from classes.Dials import Dials
import threading
import asyncio
import pygame

class Game:

    def __init__(self):
        
        pygame.font.init()
        pygame.display.init()
        pygame.display.set_caption('Snake Odyssey')
        
        self.started = False

        self.dials = Dials()

        self.snake = Snake()
        self.fruits = []
        self.fruitsLimit = 4

        self.winWidth = 450
        self.winHeight = 350
        self.win = pygame.display.set_mode(size=(self.winWidth, self.winHeight))
        self.winBgColor = '#1a1a1a'

        self.gridColumns = self.winWidth/self.snake.segment.width
        self.gridRows = self.winHeight/self.snake.segment.height
        self.clock = pygame.time.Clock()
        self.fc_fruits = 0
        self.fc_match = 0
        self.run = True

        self.threadStopEvent = threading.Event()
        self.snakePosThread = threading.Thread(
            target=self.snake.setSnakePos,
            args=[self.threadStopEvent, self.gridColumns, self.gridRows])
        
    def mainLoop (self):

        while (self.run):
            
            self.win.fill(self.winBgColor)

            self.listenQuit()
            self.snake.setSnakeSense(self.listenKeys())
            
            asyncio.run(self.initMenu())

            self.createFruit()
            self.drawSnake()
            self.listenEat()

            self.dials.trans = Data.getTrans()['dials']
            self.dials.renderScore(self.win)
            self.dials.renderSnakeSize(self.win, self.snake)
            self.dials.renderMatchTime(self.win, self.fc_match)

            pygame.display.update()

            if len(self.fruits) < self.fruitsLimit:
                self.fc_fruits += 1

            if not self.snake.snakeHit:
                self.fc_match += 1
            else:
                asyncio.run(self.restartMenu())

            self.clock.tick(60)

        pygame.quit()
    
    def listenQuit (self):

        if len(pygame.event.get(eventtype=pygame.QUIT)) > 0:
            
            if self.snakePosThread != None and self.snakePosThread.is_alive():
                self.threadStopEvent.set()
                self.snakePosThread.join()

            self.run = False
        
        else:

            self.run = True

    def drawSnake (self):

        for seg in self.snake.segmentsPos:

            sPos = self.calcNonGridPos(seg[0], seg[1])

            newRect = self.snake.segment.copy()
            newRect = newRect.move(sPos).inflate(-1, -1)

            pygame.draw.rect(self.win, self.snake.color, newRect)
    
    def createFruit (self):

        if (self.fc_fruits/60 >= 3) and not self.snake.snakeHit:

            newFruit = Fruit(
                self.snake.segmentsPos,
                (self.gridColumns, self.gridRows)
                )
            
            fPos = self.calcNonGridPos(
                newFruit.position[0],
                newFruit.position[1]
                )

            newFruit.fruitRect = newFruit.fruitRect.move(fPos)
            
            self.fruits.append(newFruit)
            self.fc_fruits = 0
        
        for fruit in self.fruits:
            pygame.draw.rect(self.win, fruit.color, fruit.fruitRect)

    def calcNonGridPos (self, xPos: int, yPos: int):

        xResult = xPos*(self.winWidth/self.gridColumns)
        yResult = yPos*(self.winHeight/self.gridRows)

        return (xResult, yResult)

    async def initMenu (self):
        
        mouseOverStart = False
        mouseOverQuit = False
        mouseOverLang = False
        mouseOverPort = False
        mouseOverEn = False
        langSelect = False

        while (not self.started and self.run):

            trans = Data.getTrans()
            self.win.fill(self.winBgColor)

            titleFont = pygame.font.SysFont('UbuntuMono', 44)
            titleSurface = titleFont.render(
                'Snake Odyssey', 
                True, 
                '#ffffff',
                self.winBgColor
                )
            titlePos = (
                (self.winWidth/2) - (titleSurface.get_width()/2), 
                (self.winHeight/3) - (titleSurface.get_height()/2)
                )
            
            buttonFont = pygame.font.SysFont('UbuntuMono', 25)
            startButton = buttonFont.render(
                trans['init']['start'],
                True,
                '#0d0d0d' if mouseOverStart else '#ffffff',
                '#e6e6e6' if mouseOverStart else self.winBgColor
            )
            startPos = (
                (self.winWidth/2) - (startButton.get_width()/2), 
                (self.winHeight/(4/3)) - (startButton.get_height()/2)
            )
            
            quitButton = buttonFont.render(
                trans['init']['quit'],
                True,
                '#0d0d0d' if mouseOverQuit else '#ffffff',
                '#e6e6e6' if mouseOverQuit else self.winBgColor
            )
            quitPos = (
                (self.winWidth/2) - (quitButton.get_width()/2), 
                (startPos[1] + startButton.get_height()) + 10
            )

            langButton = buttonFont.render(
                trans['init']['lang'],
                True,
                '#0d0d0d' if mouseOverLang else '#ffffff',
                '#e6e6e6' if mouseOverLang else self.winBgColor
            )
            langPos = (
                self.winWidth - langButton.get_width() - 15, 
                self.winHeight - langButton.get_height() - 10
            )

            langPortuguese = buttonFont.render(
                'Português (BR)',
                True,
                '#0d0d0d' if mouseOverPort else '#ffffff',
                '#e6e6e6' if mouseOverPort else self.winBgColor
            )
            langPortPos = (
                self.winWidth - langPortuguese.get_width() - 15,
                langPos[1] - langPortuguese.get_height() - 10
            )

            langEnglish = buttonFont.render(
                'English',
                True,
                '#0d0d0d' if mouseOverEn else '#ffffff',
                '#e6e6e6' if mouseOverEn else self.winBgColor
            )
            langEnPos = (
                self.winWidth - langEnglish.get_width() - 15,
                langPortPos[1] - langEnglish.get_height() - 10
            )
            
            self.win.blit(titleSurface, titlePos)
            startRect = self.win.blit(startButton, startPos)
            quitRect = self.win.blit(quitButton, quitPos)
            langRect = self.win.blit(langButton, langPos)

            mouseClick = self.listenClick()

            if startRect.collidepoint(pygame.mouse.get_pos()):
                mouseOverStart = True
                if mouseClick != None and mouseClick[0]:
                    self.started = True
                    if self.snakePosThread != None:
                        self.snakePosThread.start()
            else:
                mouseOverStart = False

            if quitRect.collidepoint(pygame.mouse.get_pos()):
                mouseOverQuit = True
                if mouseClick != None and mouseClick[0]:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            else:
                mouseOverQuit = False

            if langRect.collidepoint(pygame.mouse.get_pos()):
                mouseOverLang = True
            else:
                mouseOverLang = False

            for e in pygame.event.get(pygame.MOUSEBUTTONUP, False):
                
                if langRect.collidepoint(e.pos):
                    langSelect = not langSelect

            if langSelect:
                
                portRect = self.win.blit(langPortuguese, langPortPos)
                enRect = self.win.blit(langEnglish, langEnPos)

                if portRect.collidepoint(pygame.mouse.get_pos()):

                    mouseOverPort = True
                
                    if mouseClick != None and mouseClick[0]:
                        
                        langSelect = False
                        config = Data.getConfigs()
                        config['language'] = 'pt-br'
                        Data.setConfigs(config)

                else:
                    mouseOverPort = False
                
                if enRect.collidepoint(pygame.mouse.get_pos()):
                    mouseOverEn = True

                    if mouseClick != None and mouseClick[0]:

                        langSelect = False
                        config = Data.getConfigs()
                        config['language'] = 'en'
                        Data.setConfigs(config)

                else:                
                    mouseOverEn = False

            self.listenQuit()
            pygame.display.update()
            self.clock.tick(60)

    async def restartMenu (self):

        mouseOverRestart = False
        mouseOverHome = False
        trans = Data.getTrans()['restart']

        while (self.run):

            lostFont = pygame.font.SysFont('UbuntuMono', 34)
            lostSurface = lostFont.render(
                trans['lose'], 
                True, 
                '#ffffff',
                self.winBgColor
                )
            lostPos = (
                (self.winWidth/2) - (lostSurface.get_width()/2), 
                (self.winHeight/3) - (lostSurface.get_height()/2)
                )
            
            buttonFont = pygame.font.SysFont('UbuntuMono', 25)
            restartButton = buttonFont.render(
                trans['restart'],
                True,
                '#0d0d0d' if mouseOverRestart else '#ffffff',
                '#e6e6e6' if mouseOverRestart else self.winBgColor
            )
            resButtonPos = (
                (self.winWidth/2) - (restartButton.get_width()/2), 
                (self.winHeight/(4/3)) - (restartButton.get_height()/2)
            )

            homeMenuButton = buttonFont.render(
                trans['init'],
                True,
                '#0d0d0d' if mouseOverHome else '#ffffff',
                '#e6e6e6' if mouseOverHome else self.winBgColor
            )
            homePos = (
                (self.winWidth/2) - (homeMenuButton.get_width()/2), 
                resButtonPos[1] + homeMenuButton.get_height() + 10
            )

            self.win.blit(lostSurface, lostPos)
            restartRect = self.win.blit(restartButton, resButtonPos)
            homeRect = self.win.blit(homeMenuButton, homePos)

            mouseClick = self.listenClick()

            if restartRect.collidepoint(pygame.mouse.get_pos()):
                
                mouseOverRestart = True
                
                if mouseClick != None and mouseClick[0]:

                    self.resetGame()
                    if self.snakePosThread != None:
                        self.snakePosThread.start() 
                    break

            else:
                mouseOverRestart = False
            
            if homeRect.collidepoint(pygame.mouse.get_pos()):
                mouseOverHome = True
            else:
                mouseOverHome = False

            e = pygame.event.get(pygame.MOUSEBUTTONUP)
            if len(e) > 0 and homeRect.collidepoint(e[0].pos):
                self.started = False
                self.resetGame()
                break

            self.listenQuit()
            pygame.display.update()
            self.clock.tick(60)

    def listenClick (self):
    
        mouseButtons = pygame.mouse.get_pressed()

        if contains(mouseButtons, True):
            return mouseButtons
        else:
            return None

    def listenKeys (self):

        keyScan = pygame.key.get_pressed()
        return keyScan
    
    def listenEat (self):
        for fruit in self.fruits:
            if self.snake.segmentsPos[0] == fruit.position:
                self.fruits.remove(fruit)
                self.dials.score += 1
                self.snake.segmentsPos.append(
                    self.snake.segmentsPos[-1]
                )
    
    def resetGame (self):

        # Recomeçar todo o jogo; zerar todas as variáveis.
        self.dials = Dials()
        self.fruits = []
        
        self.snake.snakeHit = False
        self.snake.segmentsPos = [[20, 15], [19, 15], [18, 15]]
        self.snake.newSegmentsPos = []
        self.snake.sense = ['right']
        self.snake.setInterval = 0.3

        self.snakePosThread = None
        self.snakePosThread = threading.Thread(
        target=self.snake.setSnakePos,
        args=[self.threadStopEvent, self.gridColumns, self.gridRows])

        self.fc_fruits = 0
        self.fc_match = 0

gameInstance = Game()
gameInstance.mainLoop()