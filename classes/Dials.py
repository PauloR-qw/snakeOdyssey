from pygame import font
from math import trunc
from datetime import timedelta

class Dials:
    
    def __init__(self):

        # Dial title, inital value
        self.score = 0
        self.snakeSize = 3
        self.lastDest = []

        self.textColor = '#ffffff'
        self.fontSize = 13
        self.antialias = True
        self.font = font.SysFont('UbuntuMono', self.fontSize)
        self.trans = {}

    def renderScore (self, win):
        
        score = self.trans['score'] + ': '
        score += str(self.score).zfill(4)
        
        dest = (10, 10)
        scoreSurface = self.font.render(score, True, self.textColor)
        win.blit(scoreSurface, dest)
        self.lastDest.append(dest[0] + scoreSurface.get_width())
    
    def renderSnakeSize (self, win, snake):

        snakeSize = self.trans['size'] + ': '
        snakeSize += str(len(snake.segmentsPos)).zfill(3)

        dest = (self.lastDest.pop() + 10, 10)
        snakeSizeSurface = self.font.render(snakeSize, self.antialias, self.textColor)
        win.blit(snakeSizeSurface, dest)
        self.lastDest.append(dest[0] + snakeSizeSurface.get_width())
    
    def renderMatchTime (self, win, fc_match):

        time = timedelta(seconds=trunc(fc_match/60))
        matchTime = self.trans['time'] + ': '
        matchTime += str(time)[2:]

        dest = (self.lastDest.pop() + 10, 10)
        matchTimeSurface = self.font.render(matchTime, self.antialias, self.textColor)
        win.blit(matchTimeSurface, dest)
        