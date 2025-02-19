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
        return random.choice(win), random.choice(loser)
        
        
BFGconst = BFGstateClass()
