from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from buttons import ExtendButton, StickyButton, SwitchButton, Spacer
import globvars

class CentreButton(ExtendButton):
    def on_press(self):
        globvars.AllItems['stateMachine'].centre_machine()
        
class AlphabetButton(ExtendButton):
    def on_press(self):
        globvars.AllItems['stateMachine'].define_alphabet()
        
class MachineButton(StickyButton):
    def on_press(self):
        super(MachineButton, self).on_press()
        globvars.AllItems['stateMachine'].set_mode(self.mode)
            
class BuildToolbar(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(BuildToolbar, self).__init__(*args, **kwargs)
        self.size_hint = 1, None
        self.height = 60
        globvars.AllItems['move'] = MachineButton(mode = "move", text = "Move\nCanvas", selected = True)
        self.add_widget(globvars.AllItems['move'])
        self.add_widget(MachineButton(mode = "create_s", text = "Create\n/ Move\nState"))
        self.add_widget(MachineButton(mode = "create_t", text = "Create\n/ Move\nTransition"))
        self.add_widget(MachineButton(mode = "edit", text = "Edit\nState /\nTransition"))
        self.add_widget(MachineButton(mode = "delete", text = "Delete\nState /\nTransition"))
        self.add_widget(MachineButton(mode = "start", text = "Set\nStart\nState"))
        self.add_widget(MachineButton(mode = "final", text = "Set\nFinal\nState"))
        self.add_widget(CentreButton(text = "Centre\nState\nMachine"))
        self.add_widget(AlphabetButton(text = "Define\nAlphabet"))
        self.add_widget(Spacer())
        self.add_widget(SwitchButton(mode = "run", text = "Run", direction = "left", newmode = "run", button = None))

class PrototypeApp(App):
    def build(self):
        return BuildToolbar()

if __name__ == '__main__':
    PrototypeApp().run()