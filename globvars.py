from kivy.clock import Clock
import string

def create():
    global AllItems
    AllItems = {}
    AllItems['states'] = []
    AllItems['transitions'] = []
    AllItems['linethickness'] = 2
    AllItems['gs'] = 20 #grabber size
    AllItems['alphabet'] = ""
    AllItems['reservedCharacters'] = "/"
    AllItems['moverDisplayModes'] = ["create_t", "edit", "delete"]
    AllItems['movementClock'] = create
    AllItems['undo'] = []
    AllItems['redo'] = []
    AllItems['animation'] = True
    AllItems['animationStep'] = 1