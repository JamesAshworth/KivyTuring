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
    mode = globvars.AllItems['stateMachine'].mode
    if identify_state_in(touch):
        if mode == "final":
            touch.ud['touched'].final_state_toggle()
            return True
        if mode == "start":
            touch.ud['touched'].set_start_state()
            return True
        if mode == "delete":
            touch.ud['touched'].destroy_self()
            return True
        if mode == "create_t":
            globvars.AllItems['stateMachine'].make_transition(touch)
            return True
        if mode == "edit":
            touch.ud['touched'].edit_name()
            return True
        return True
    return False
    
def identify_state_in(touch):
    for state in globvars.AllItems['states']:
        if state.check_touch(touch):
            return True
    return False
    
def collide_state(x, y):        
    for state in globvars.AllItems['states']:
        if state.collide_state(x, y):
            return None
            
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