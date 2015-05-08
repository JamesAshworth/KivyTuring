from kivy.uix.button import Button
from kivy.uix.widget import Widget
import globvars
import undo
        
#----------------------------------------------------------
# Name: Spacer
# 
# Widget with the selected proc, to space items nicely
#----------------------------------------------------------
class Spacer(Widget):
    def selected(self, selected):
        pass
        
#----------------------------------------------------------
# Name: ExtendButton
# 
# Button with the selected proc, to build from
#----------------------------------------------------------
class ExtendButton(Button):
    def selected(self, selected):
        pass
        
#----------------------------------------------------------
# Name: ModeButton
# 
# Button which has a mode, for buttons which might want 
# some sort of mode
#----------------------------------------------------------
class ModeButton(ExtendButton):
    def __init__(self, mode = None, *args, **kwargs):
        super(ModeButton, self).__init__(*args, **kwargs)
        self.mode = mode
        
#----------------------------------------------------------
# Name: StickyButton
# 
# Button which leaves itself pressed when it's touched
# Also ensures that it is the only button left pressed
#----------------------------------------------------------
class StickyButton(ModeButton):
    def __init__(self, selected = False, *args, **kwargs):
        super(StickyButton, self).__init__(*args, **kwargs)
        self.default = self.background_normal
        self.selected(selected)
        
    def on_press(self):
        for button in self.parent.children:
            button.selected(False)
        self.selected(True)
        
    def selected(self, selected):
        if selected:
            self.background_normal = self.background_down
        else:
            self.background_normal = self.default
        
#----------------------------------------------------------
# Name: SwitchButton
# 
# Button to switch screens on the target screen manager
# Also sets the mode of the state machine, and will deny
# the switch if it's not allowed
#----------------------------------------------------------
class SwitchButton(ModeButton):
    def __init__(self, direction, newmode, button, target, *args, **kwargs):
        super(SwitchButton, self).__init__(*args, **kwargs)
        self.direction = direction
        self.newmode = newmode
        self.button = button
        self.target = target
        
    def on_press(self):
        if not globvars.AllItems['stateMachine'].set_mode(self.newmode):
            return
        globvars.AllItems[self.target].transition.direction = self.direction
        globvars.AllItems[self.target].current = self.mode
        if not (self.button is None):
            globvars.AllItems[self.button].on_press()
        
#----------------------------------------------------------
# Name: UndoButton
# 
# Either calls undo or redo
# The buttons are enabled and disabled elsewhere, so we 
# can't undo or redo with nothing to undo or redo
#----------------------------------------------------------
class UndoButton(ModeButton):
    def __init__(self, *args, **kwargs):
        super(UndoButton, self).__init__(*args, **kwargs)
        self.disabled = True
        
    def on_press(self):
        if self.mode == 'undo':
            undo.do_undo()
        elif self.mode == 'redo':
            undo.do_redo()