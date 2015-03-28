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