from time import sleep
from pygame import K_DOWN, K_LEFT, K_LSHIFT, K_RIGHT, K_UP, K_w, K_a, K_s, K_d, Rect

class Snake ():

    def __init__(self) -> None:
        
        self.segmentsPos = [[20, 15], [19, 15], [18, 15]]
        self.sense = 'right'
        self.segment = Rect(0, 0, 10, 10)
        self.color = '#006600' # #66ff66 20%
        self.setInterval = 0.3
        self.rush = False
        self.rushInterval = self.setInterval * 0.3
    
    def getSnakeSense (self, keysPressed):

        senseDown = keysPressed[K_DOWN] or keysPressed[K_s]
        senseRight = keysPressed[K_RIGHT] or keysPressed[K_d]
        senseUp = keysPressed[K_UP] or keysPressed[K_w]
        senseLeft = keysPressed[K_LEFT] or keysPressed[K_a]

        # Definindo a direção da cobrinha de acordo com as
        # teclas pressionadas.
        if senseDown and self.sense != 'up':
            self.sense = 'down'
        elif senseRight and self.sense != 'left':
            self.sense = 'right'
        elif senseUp and self.sense != 'down':
            self.sense = 'up'
        elif senseLeft and self.sense != 'right':
            self.sense = 'left'

        if keysPressed[K_LSHIFT]:
            self.rush = True
        else:
            self.rush = False
       
    def setSnakePos (self, stopEvent, gridColumns, gridRows):

        while (True):
            
            self.segmentsPos.insert(
                0,
                [self.segmentsPos[0][0], self.segmentsPos[0][1]]
                )
            self.segmentsPos.pop()
            
            # Calculando a posição da cabeça da cobrinha.
            # Os seguimentos anteriores, da cobrinha, 'herdarão'
            # umas o estado das outras, a começar pela cabeça.
            if self.sense == 'down':

                self.segmentsPos[0][1] += 1
                if self.segmentsPos[0][1] > gridRows - 1:
                    self.segmentsPos[0][1] = 0

            elif self.sense == 'right':

                self.segmentsPos[0][0] += 1
                if self.segmentsPos[0][0] > gridColumns - 1:
                    self.segmentsPos[0][0] = 0

            elif self.sense == 'up':

                self.segmentsPos[0][1] -= 1
                if self.segmentsPos[0][1] < 0:
                    self.segmentsPos[0][1] = gridRows - 1

            elif self.sense == 'left':

                self.segmentsPos[0][0] -= 1
                if self.segmentsPos[0][0] < 0:
                    self.segmentsPos[0][0] = gridColumns - 1
            
            if self.rush:
                sleep(self.rushInterval)
            else:
                sleep(self.setInterval)

            if stopEvent.is_set():
                break