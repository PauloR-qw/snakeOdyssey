from pygame import font

class Dials ():
    
    def __init__(self) -> None:

        # Dial title, value
        self.score = ['Score', 0]
        self.textColor = '#ffffff'
        self.fontSize = 13

    def renderScore (self, win):
        
        scoreFont = font.SysFont('UbuntuMono', self.fontSize)
        score = self.score[0] + ': '
        score += str(self.score[1]).zfill(4)
        
        scoreSurface = scoreFont.render(score, True, self.textColor)
        win.blit(scoreSurface, (10, 10))
    