from kivy.uix.button import Button
from kivy.uix.widget import Widget
import globvars
import undo

class Spacer(Widget):
    def selected(self, selected):
        pass
        
class ExtendButton(Button):
    def selected(self, selected):
        pass
        
class ModeButton(ExtendButton):
    def __init__(self, mode = None, *args, **kwargs):
        super(ModeButton, self).__init__(*args, **kwargs)
        self.mode = mode
        
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
        
class SwitchButton(ModeButton):
    def __init__(self, direction, newmode, button, *args, **kwargs):
        super(SwitchButton, self).__init__(*args, **kwargs)
        self.direction = direction
        self.newmode = newmode
        self.button = button
        
    def on_press(self):
        if not globvars.AllItems['stateMachine'].set_mode(self.newmode):
            return
        globvars.AllItems['toolbar'].transition.direction = self.direction
        globvars.AllItems['toolbar'].current = self.mode
        if not (self.button is None):
            self.button.on_press()
            
class UndoButton(ModeButton):
    def __init__(self, *args, **kwargs):
        super(UndoButton, self).__init__(*args, **kwargs)
        self.disabled = True
        
    def on_press(self):
        if self.mode == 'undo':
            undo.do_undo()
        elif self.mode == 'redo':
            undo.do_redo()