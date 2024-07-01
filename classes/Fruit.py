from typing import List, Tuple
from random import randint
from pygame import Rect

class Fruit:
    
    def __init__(self, snakePos:List, gridLimits:Tuple):
        
        self.snakePos = snakePos
        self.gridLimits = gridLimits
        self.position = self.sortPosition()
        self.color = '#b30000' #red 35%
        self.fruitRect = Rect(0, 0, 9, 9)
    
    def sortPosition (self):
        
        sortedPos = [
            randint(1, self.gridLimits[0] - 1),
            randint(1, self.gridLimits[1] - 1)
            ]
        
        for pos in self.snakePos:
            if sortedPos == pos:
                self.sortPosition()
    
        return sortedPos