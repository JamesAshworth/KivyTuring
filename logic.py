import globvars
import statefuncs
import transitionfuncs
from popups import InfoBox

def begin_simulation():
    globvars.AllItems['simState'] = statefuncs.find_start_and_centre()
    globvars.AllItems['simState'].highlighted(True)
    globvars.AllItems['simCell'] = 0
    globvars.AllItems['tape'].select_cell(0)
    globvars.AllItems['tape'].save_values()
    globvars.AllItems['tape'].allowedits = False
    globvars.AllItems['running'] = False
    
def do_run():
    if globvars.AllItems['running']:
        do_step()

def do_step():
    if globvars.AllItems['inStep']:
        return
    globvars.AllItems['inStep'] = True
    readVal = globvars.AllItems['tape'].get_value(globvars.AllItems['simCell'])
    for t in globvars.AllItems['simState'].transitions:
        if t.startstate == globvars.AllItems['simState']:
            if t.read_value() == readVal:
                globvars.AllItems['tape'].set_value(globvars.AllItems['simCell'], t.write_value())
                globvars.AllItems['simCell'] += t.move_value()
                globvars.AllItems['tape'].select_cell(globvars.AllItems['simCell'])
                t.move_along_line()
                globvars.AllItems['simState'] = t.endstate
                return
            
    globvars.AllItems['inStep'] = False
    globvars.AllItems['pauseButton'].on_press()
    if globvars.AllItems['simState'].final:
        InfoBox(title="Complete", message="Simulation halted with answer 'Yes'").open()
    else:
        InfoBox(title="Complete", message="Simulation halted with answer 'No'").open()
    
def end_simulation():
    globvars.AllItems['simState'] = None
    globvars.AllItems['simCell'] = None
    globvars.AllItems['inStep'] = False
    globvars.AllItems['tape'].select_cell(0)
    globvars.AllItems['tape'].restore_values()
    globvars.AllItems['tape'].allowedits = True
    globvars.AllItems['tape'].reset_position()
    statefuncs.remove_highlight()
    transitionfuncs.remove_highlight()
    transitionfuncs.reset_movement()
    
def reset_simulation():
    end_simulation()
    begin_simulation()
    