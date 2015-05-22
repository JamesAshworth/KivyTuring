def create():
    global AllItems
    AllItems = {}
    AllItems['states'] = []
    AllItems['transitions'] = []
    AllItems['linethickness'] = 2
    AllItems['alphabet'] = ""
    AllItems['reservedCharacters'] = "/"
    AllItems['moverDisplayModes'] = ["create_t", "edit", "delete"]
    AllItems['movementClock'] = create
    AllItems['undo'] = []
    AllItems['redo'] = []
    AllItems['animation'] = True
    AllItems['animationStep'] = 0.05
    AllItems['inStep'] = False
    AllItems['undoDisabled'] = False
    AllItems['stateSize'] = 0