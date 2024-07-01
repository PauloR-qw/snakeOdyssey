from copy import copy
from time import sleep
from pygame import K_DOWN, K_LEFT, K_LSHIFT, K_RIGHT, K_UP, K_w, K_a, K_s, K_d, Rect

class Snake:

    def __init__(self):
        
        self.segmentsPos = [[20, 15], [19, 15], [18, 15]]
        self.newSegmentsPos = []
        self.sense = ['right']
        self.segment = Rect(0, 0, 10, 10)
        self.color = '#008000' # #66ff66 20%
        self.setInterval = 0.3
        self.rush = False
        self.rushInterval = self.setInterval * 0.3
        self.snakeHit = False
    
    def getSnakeSense (self, keysPressed):

        senseDown = keysPressed[K_DOWN] or keysPressed[K_s]
        senseRight = keysPressed[K_RIGHT] or keysPressed[K_d]
        senseUp = keysPressed[K_UP] or keysPressed[K_w]
        senseLeft = keysPressed[K_LEFT] or keysPressed[K_a]

        # Definindo a direção da cobrinha de acordo com as
        # teclas pressionadas.
        if senseDown and self.sense[0] != 'up' and self.sense[0] != 'down':
            self.sense.insert(0, 'down')
        elif senseRight and self.sense[0] != 'left' and self.sense[0] != 'right':
            self.sense.insert(0, 'right')
        elif senseUp and self.sense[0] != 'down' and self.sense[0] != 'up':
            self.sense.insert(0, 'up')
        elif senseLeft and self.sense[0] != 'right' and self.sense[0] != 'left':
            self.sense.insert(0, 'left')

        if len(self.sense) > 2:
            self.sense = self.sense[:2]

        if keysPressed[K_LSHIFT]:
            self.rush = True
        else:
            self.rush = False
    
    def setSnakePos (self, stopEvent, gridColumns, gridRows):
        
        while (True):
            self.newSegmentsPos = self.segmentsPos.copy()

            self.newSegmentsPos.insert(
                0,
                [self.newSegmentsPos[0][0], self.newSegmentsPos[0][1]]
                )
            del self.newSegmentsPos[-1]
            
            # Calculando a posição da cabeça da cobrinha.
            # Os seguimentos anteriores, da cobrinha, 'herdarão'
            # umas o estado das outras, a começar pela cabeça.
            
            if self.sense[0] == 'down':

                self.newSegmentsPos[0][1] += 1
                if self.newSegmentsPos[0][1] > gridRows - 1:
                    self.newSegmentsPos[0][1] = 0

            elif self.sense[0] == 'right':

                self.newSegmentsPos[0][0] += 1
                if self.newSegmentsPos[0][0] > gridColumns - 1:
                    self.newSegmentsPos[0][0] = 0

            elif self.sense[0] == 'up':

                self.newSegmentsPos[0][1] -= 1
                if self.newSegmentsPos[0][1] < 0:
                    self.newSegmentsPos[0][1] = gridRows - 1

            elif self.sense[0] == 'left':

                self.newSegmentsPos[0][0] -= 1
                if self.newSegmentsPos[0][0] < 0:
                    self.newSegmentsPos[0][0] = gridColumns - 1


            if self.newSegmentsPos[0] == self.newSegmentsPos[2]:

                self.sense[0] = copy(self.sense[1])

            elif self.newSegmentsPos[0] in self.newSegmentsPos[3:]:

                self.snakeHit = True
                break

            else:

                self.segmentsPos = self.newSegmentsPos.copy()

                if self.rush:
                    sleep(self.rushInterval)
                else:
                    sleep(self.setInterval)

                if stopEvent.is_set():
                    break