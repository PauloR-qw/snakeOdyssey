from classes.Snake import Snake
import threading
import pygame

class Game ():

    def __init__(self) -> None:
        
        pygame.display.init()
        pygame.display.set_caption('Snake Odyssey')
        
        self.snake = Snake()
        self.winWidth = 800
        self.winHeight = 600
        self.win = pygame.display.set_mode(size=(self.winWidth, self.winHeight))
        self.gridColumns = self.winWidth/self.snake.segment.width
        self.gridRows = self.winHeight/self.snake.segment.height
        self.clock = pygame.time.Clock()
        self.run = True

        self.threadStopEvent = threading.Event()
        self.snakePosThread = threading.Thread(
            target=self.snake.setSnakePos,
            args=[self.threadStopEvent, self.gridColumns, self.gridRows])
        
        self.snakePosThread.start()
        self.drawSnake()
    
    def mainLoop (self) -> None:

        while (self.run):
            
            self.win.fill('#1a1a1a')

            self.listenQuit()
            self.listenKeys()

            self.drawSnake()
            
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
    
    def listenQuit (self):

        if len(pygame.event.get(eventtype=pygame.QUIT)) > 0:

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

    def calcNonGridPos (self, xPos: int, yPos: int):

        xResult = xPos*(self.winWidth/self.gridColumns)
        yResult = yPos*(self.winHeight/self.gridRows)

        return (xResult, yResult)

    def listenKeys (self):

        keyScan = pygame.key.get_pressed()
        self.snake.getSnakeSense(keyScan)


gameInstance = Game()
gameInstance.mainLoop()