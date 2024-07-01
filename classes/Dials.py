from pygame import font
from math import trunc
from datetime import timedelta

class Dials ():
    
    def __init__(self) -> None:

        # Dial title, inital value
        self.score = ['Score', 0]
        self.snakeSize = ['Size', 3]

        self.textColor = '#ffffff'
        self.fontSize = 13
        self.antialias = True
        self.font = font.SysFont('UbuntuMono', self.fontSize)

    def renderScore (self, win):
        
        score = self.score[0] + ': '
        score += str(self.score[1]).zfill(4)
        
        dest = (10, 10)
        scoreSurface = self.font.render(score, True, self.textColor)
        win.blit(scoreSurface, dest)
        self.score.append(dest[0] + scoreSurface.get_width())
    
    def renderSnakeSize (self, win, snake):

        snakeSize = self.snakeSize[0] + ': '
        snakeSize += str(len(snake.segmentsPos)).zfill(3)

        dest = (self.score.pop() + 10, 10)
        snakeSizeSurface = self.font.render(snakeSize, self.antialias, self.textColor)
        win.blit(snakeSizeSurface, dest)
        self.snakeSize.append(dest[0] + snakeSizeSurface.get_width())
    
    def renderMatchTime (self, win, fc_match):

        time = timedelta(seconds=trunc(fc_match/60))
        matchTime = 'Time: '
        matchTime += str(time)[2:]

        dest = (self.snakeSize.pop() + 10, 10)
        matchTimeSurface = self.font.render(matchTime, self.antialias, self.textColor)
        win.blit(matchTimeSurface, dest)
        