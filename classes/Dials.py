from pygame import font
from math import trunc
from datetime import timedelta

class Dials ():
    
    def __init__(self) -> None:

        # Dial title, value
        self.score = ['Score', 0]
        self.snakeSize = ['Size', 3]

        self.textColor = '#ffffff'
        self.fontSize = 13
        self.antialias = True
        self.font = font.SysFont('UbuntuMono', self.fontSize)

    def renderScore (self, win):
        
        score = self.score[0] + ': '
        score += str(self.score[1]).zfill(4)
        
        scoreSurface = self.font.render(score, True, self.textColor)
        win.blit(scoreSurface, (10, 10))
    
    def renderSnakeSize (self, win, snake):

        snakeSize = self.snakeSize[0] + ': '
        snakeSize += str(len(snake.segmentsPos)).zfill(3)

        snakeSizeSurface = self.font.render(snakeSize, self.antialias, self.textColor)
        win.blit(snakeSizeSurface, (100, 10))
    
    def renderMatchTime (self, win, fc_match):

        time = timedelta(seconds=trunc(fc_match/60))
        matchTime = 'Time: '
        matchTime += str(time)[2:]

        matchTimeSurface = self.font.render(matchTime, self.antialias, self.textColor)
        win.blit(matchTimeSurface, (180, 10))
        