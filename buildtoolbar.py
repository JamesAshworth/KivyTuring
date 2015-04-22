from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from buttons import ExtendButton, StickyButton, SwitchButton, Spacer, UndoButton
from loadmachine import FileChooser
import globvars

class CentreButton(ExtendButton):
    def on_press(self):
        globvars.AllItems['stateMachine'].centre_machine()
        
class LoadButton(ExtendButton):
    def on_press(self):
        FileChooser().open()
        
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
        self.add_widget(Spacer())
        globvars.AllItems['move'] = MachineButton(mode = "move", background_normal = "./resources/move_button.png", background_down = "./resources/move_button_pressed.png", selected = True)
        globvars.AllItems['undoButton'] = UndoButton(mode = "undo", text = "Undo")
        globvars.AllItems['redoButton'] = UndoButton(mode = "redo", text = "Redo")
        self.add_widget(globvars.AllItems['move'])
        self.add_widget(MachineButton(mode = "create_s", background_normal = "./resources/state_button.png", background_down = "./resources/state_button_pressed.png"))
        self.add_widget(MachineButton(mode = "create_t", background_normal = "./resources/transition_button.png", background_down = "./resources/transition_button_pressed.png"))
        self.add_widget(MachineButton(mode = "delete", background_normal = "./resources/delete_button.png", background_down = "./resources/delete_button_pressed.png"))
        self.add_widget(MachineButton(mode = "start", background_normal = "./resources/start_button.png", background_down = "./resources/start_button_pressed.png"))
        self.add_widget(MachineButton(mode = "final", background_normal = "./resources/final_button.png", background_down = "./resources/final_button_pressed.png"))
        self.add_widget(AlphabetButton(background_normal = "./resources/alphabet_button.png", background_down = "./resources/alphabet_button_pressed.png"))
        self.add_widget(Spacer())
        self.add_widget(globvars.AllItems['undoButton'])
        self.add_widget(globvars.AllItems['redoButton'])
        self.add_widget(LoadButton(text = "Load"))
        self.add_widget(Spacer())
        self.add_widget(SwitchButton(mode = "run", text = "Run", direction = "left", newmode = "run", button = None))

class TuringApp(App):
    def build(self):
        return BuildToolbar()

if __name__ == '__main__':
    TuringApp().run()