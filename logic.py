import globvars
import statefuncs
import transitionfuncs

def begin_simulation():
    globvars.AllItems['simState'] = statefuncs.find_start_and_centre()
    globvars.AllItems['simState'].highlighted(True)
    globvars.AllItems['simCell'] = 0
    globvars.AllItems['tape'].save_values()
    globvars.AllItems['tape'].allowshift = False
    globvars.AllItems['running'] = False
    
def do_run():
    if globvars.AllItems['running']:
        do_step()

def do_step():
    readVal = globvars.AllItems['tape'].get_value(globvars.AllItems['simCell'])
    for t in globvars.AllItems['simState'].transitions:
        if t.read_value() == readVal:
            globvars.AllItems['tape'].set_value(globvars.AllItems['simCell'], t.write_value())
            globvars.AllItems['simCell'] += t.move_value()
            globvars.AllItems['tape'].select_cell(globvars.AllItems['simCell'])
            t.move_along_line()
            globvars.AllItems['simState'] = t.endstate
            return
            
    print "Done" #popup, deselect run
    
def end_simulation():
    globvars.AllItems['simState'] = None
    globvars.AllItems['simCell'] = None
    globvars.AllItems['tape'].select_cell(0)
    globvars.AllItems['tape'].restore_values()
    globvars.AllItems['tape'].allowshift = True
    globvars.AllItems['tape'].reset_position()
    statefuncs.remove_highlight()
    
def reset_simulation():
    end_simulation()
    transitionfuncs.reset_movement()
    begin_simulation()
    