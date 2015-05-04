from kivy.uix.widget import Widget
import savemachine
import globvars

def do_undo():
    record = globvars.AllItems['undo'].pop()
    globvars.AllItems['redo'].append(record)
    record.do_undo()
    globvars.AllItems['redoButton'].disabled = False
    if not len(globvars.AllItems['undo']):
        globvars.AllItems['undoButton'].disabled = True
        
def do_redo():
    record = globvars.AllItems['redo'].pop()
    globvars.AllItems['undo'].append(record)
    record.do_redo()
    globvars.AllItems['undoButton'].disabled = False
    if not len(globvars.AllItems['redo']):
        globvars.AllItems['redoButton'].disabled = True
        
def clear_undo():
    globvars.AllItems['redo'] = []
    globvars.AllItems['redoButton'].disabled = True
    globvars.AllItems['undo'] = []
    globvars.AllItems['undoButton'].disabled = True
        
#----------------------------------------------------------
# Name: UndoRecord
# 
# Base class for creating records for undoing
#----------------------------------------------------------
class UndoRecord(Widget):
    def __init__(self):
        globvars.AllItems['redo'] = []
        globvars.AllItems['redoButton'].disabled = True
        globvars.AllItems['undo'].append(self)
        globvars.AllItems['undoButton'].disabled = False
        try:
            savemachine.save_machine(globvars.AllItems['saveFile'] + "~")
        except KeyError:
            pass
        
    def do_undo(self):
        self.undo()
        savemachine.save_machine(globvars.AllItems['saveFile'] + "~")
        
    def do_redo(self):
        self.redo()
        savemachine.save_machine(globvars.AllItems['saveFile'] + "~")
        
#----------------------------------------------------------
# Name: UndoStateName
# 
# Holds the old name. When required, switches old and new
#----------------------------------------------------------
class UndoStateName(UndoRecord):
    def __init__(self, state, name):
        super(UndoStateName, self).__init__()
        self.state = state
        self.name = name
        
    def undo(self):
        self.name, self.state.name = self.state.name, self.name
        self.state.label.text = self.state.name
        
    def redo(self):
        self.name, self.state.name = self.state.name, self.name
        self.state.label.text = self.state.name
        
#----------------------------------------------------------
# Name: UndoStateMove
# 
# Moves the state back and forth, for undo and redo
#----------------------------------------------------------
class UndoStateMove(UndoRecord):
    def __init__(self, state, dx, dy):
        super(UndoStateMove, self).__init__()
        self.state = state
        self.dx = dx
        self.dy = dy
    
    def undo(self):
        self.state.move(- self.dx, - self.dy)
        
    def redo(self):
        self.state.move(self.dx, self.dy)
        
#----------------------------------------------------------
# Name: UndoStateCreate
# 
# Hides and shows the state widget (given that this is the
# create, we know there are no existing transactions at
# this point)
#----------------------------------------------------------
class UndoStateCreate(UndoRecord):
    def __init__(self, state):
        super(UndoStateCreate, self).__init__()
        self.state = state
    
    def undo(self):
        globvars.AllItems['stateMachine'].remove_widget(self.state)
        globvars.AllItems['states'].remove(self.state)
        
    def redo(self):
        globvars.AllItems['stateMachine'].add_widget(self.state)
        globvars.AllItems['states'].append(self.state)
        
#----------------------------------------------------------
# Name: UndoStateDeleteStart
# 
# When a state is deleted, first all of its transitions are
# deleted, and it's possible the start state will change.
# To facilitate this we cascade the undos and redos through
# the transition deletions and start changes
#----------------------------------------------------------
class UndoStateDeleteStart(UndoRecord):
    def __init__(self, state, index):
        super(UndoStateDeleteStart, self).__init__()
        self.state = state
        self.index = index
        
    def undo(self):
        globvars.AllItems['stateMachine'].add_widget(self.state)
        globvars.AllItems['states'].insert(self.index, self.state)
        while not type(globvars.AllItems['undo'][-1]) is UndoStateDeleteStop:
            do_undo()
        do_undo()
        
    def redo(self):
        globvars.AllItems['stateMachine'].remove_widget(self.state)
        globvars.AllItems['states'].remove(self.state)
        
#----------------------------------------------------------
# Name: UndoStateDeleteStop
# 
# This record stops the undo cascade and starts the redo
# cascade as above
#----------------------------------------------------------
class UndoStateDeleteStop(UndoRecord):
    def undo(self):
        pass
    
    def redo(self):
        while not type(globvars.AllItems['redo'][-1]) is UndoStateDeleteStart:
            do_redo()
        do_redo()
        
#----------------------------------------------------------
# Name: UndoStateFinal
# 
# Flips the final state backwards and forwards
#----------------------------------------------------------
class UndoStateFinal(UndoRecord):
    def __init__(self, state):
        super(UndoStateFinal, self).__init__()
        self.state = state
        
    def undo(self):
        self.state.final_state_toggle()
        
    def redo(self):
        self.state.final_state_toggle()
        
#----------------------------------------------------------
# Name: UndoStateStart
# 
# Flips the start state between the old state and the new
# state
#----------------------------------------------------------
class UndoStateStart(UndoRecord):
    def __init__(self, oldState, newState):
        super(UndoStateStart, self).__init__()
        self.oldState = oldState
        self.newState = newState
        
    def undo(self):
        self.oldState.set_start_state()
        
    def redo(self):
        self.newState.set_start_state()
        
#----------------------------------------------------------
# Name: UndoTransitionInfo
# 
# Flips the old and new info
#----------------------------------------------------------
class UndoTransitionInfo(UndoRecord):
    def __init__(self, transitionInfo, info):
        super(UndoTransitionInfo, self).__init__()
        self.transitionInfo = transitionInfo
        self.info = info
        
    def undo(self):
        self.info, self.transitionInfo.label.text = self.transitionInfo.label.text, self.info
        
    def redo(self):
        self.info, self.transitionInfo.label.text = self.transitionInfo.label.text, self.info
        
#----------------------------------------------------------
# Name: UndoTransitionMove
# 
# Moves the midpoint backwards and forwards
#----------------------------------------------------------
class UndoTransitionMove(UndoRecord):
    def __init__(self, transition, dx, dy):
        super(UndoTransitionMove, self).__init__()
        self.transition = transition
        self.dx = dx
        self.dy = dy
    
    def undo(self):
        self.transition.midpoint.x -= self.dx
        self.transition.midpoint.y -= self.dy
        self.transition.update()
        
    def redo(self):
        self.transition.midpoint.x += self.dx
        self.transition.midpoint.y += self.dy
        self.transition.update()
        
#----------------------------------------------------------
# Name: UndoTransitionCreate
# 
# Destroy self removes its traces, so is good for undo.
# Finish transition uses information within the transition
# to insinuate itself into the states, so is also fit for
# purpose
#----------------------------------------------------------
class UndoTransitionCreate(UndoRecord):
    def __init__(self, transition):
        super(UndoTransitionCreate, self).__init__()
        self.transition = transition
        
    def undo(self):
        self.transition.destroy_self()
        
    def redo(self):
        self.transition.finish_transition()
        
#----------------------------------------------------------
# Name: UndoTransitionDelete
# 
# More complex, because finish_transition resets the
# midpoint. Changed to avoid resetting the midpoint in this
# instance. Done like this to minimise duplication
#----------------------------------------------------------
class UndoTransitionDelete(UndoRecord):
    def __init__(self, transition):
        super(UndoTransitionDelete, self).__init__()
        self.transition = transition
        
    def undo(self):
        self.transition.finish_transition(resetMidpoint = False)
    
    def redo(self):
        self.transition.destroy_self()
        