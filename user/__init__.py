from .main import User
import random


class BFGuser(
    User
):
    pass


class BFGstateClass:
    def __init__(self):
        self.ads = ''
    
    def emj(self):
        win = ['🙂', '😋', '😄', '🤑', '😃', '😇']
        loser = ['😔', '😕', '😣', '😞', '😢']
        rwin = random.choice(win)
        rloser = random.choice(loser)
        return rwin, rloser
        
        
BFGconst = BFGstateClass()