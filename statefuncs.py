import globvars

def state_named(name):
    for state in globvars.AllItems['states']:
        if state.name == name:
            return True
    return False
        
def move_all(x, y):
    for state in globvars.AllItems['states']:
        state.move(x, y)
        
def states_to_front():
    for state in globvars.AllItems['states']:
        globvars.AllItems['stateMachine'].remove_widget(state)
        globvars.AllItems['stateMachine'].add_widget(state)
        
def handled_by_state(touch):
    if identify_state_in(touch):
        return touch.ud['touched'].on_touch_down(touch)
    return False
    
def identify_state_in(touch):
    for state in globvars.AllItems['states']:
        if state.check_touch(touch):
            return True
    return False
    
def collide_state(x, y):        
    for state in globvars.AllItems['states']:
        if state.collide_state(x, y):
            return True
    return False
            
def find_state_by_name(name):
    for state in globvars.AllItems['states']:
        if state.name == name:
            return state
    return None
    
def remove_start_state():
    for state in globvars.AllItems['states']:
        state.start_state(False)
        
def find_start_and_centre():
    for state in globvars.AllItems['states']:
        if state.start:
            state.move_to_centre()
            return state
    return None
    
def remove_highlight():
    for state in globvars.AllItems['states']:
        state.highlighted(False)