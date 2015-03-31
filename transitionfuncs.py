import globvars

def display_mover(display):
    for t in globvars.AllItems['transitions']:
        t.display_mover(display)
        
def movers_to_front():
    for t in globvars.AllItems['transitions']:
        globvars.AllItems['stateMachine'].remove_widget(t.midpoint)
        globvars.AllItems['stateMachine'].add_widget(t.midpoint)
        
def handled_by_transition(touch):
    mode = globvars.AllItems['stateMachine'].mode
    if identify_transition_on(touch):
        if mode == "create_t":
            return True
        if mode == "delete":
            touch.ud['touched'].destroy_self()
            return True
        if mode == "edit":
            touch.ud['touched'].edit_info()
            return True
        return False
    return False
            
def identify_transition_on(touch):
    for t in globvars.AllItems['transitions']:
        if t.check_touch(touch):
            return True
    return False
    
def reset_movement():
    for t in globvars.AllItems['transitions']:
        t.alongline = 0