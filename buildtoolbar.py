from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from buttons import ToolbarButton, StickyButton, SwitchButton, Spacer, UndoButton
import globvars
import savemachine
        
#----------------------------------------------------------
# Name: AlphabetButton
# 
# Button to define the alphabet on the current machine
#----------------------------------------------------------
class AlphabetButton(ToolbarButton):
    def on_press(self):
        globvars.AllItems['stateMachine'].define_alphabet()
        
#----------------------------------------------------------
# Name: SaveButton
# 
# Button to explicitly save the current machine (ie .xml 
# not .xml~)
#----------------------------------------------------------
class SaveButton(ToolbarButton):
    def on_press(self):
        savemachine.save_machine(auto = False)
        
#----------------------------------------------------------
# Name: MachineButton
# 
# Button to change the mode of the state machine, as well
# as being a sticky button for the purpose of the toolbar
#----------------------------------------------------------
class MachineButton(StickyButton):
    def on_press(self):
        super(MachineButton, self).on_press()
        globvars.AllItems['stateMachine'].set_mode(self.mode)
        
#----------------------------------------------------------
# Name: BuildToolbar
# 
# Toolbar for the build screen
#----------------------------------------------------------
class BuildToolbar(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(BuildToolbar, self).__init__(*args, **kwargs)
        # These buttons need to be accessible externally, so we'll explicitly store references to them in the global area
        globvars.AllItems['move'] = MachineButton(mode = "move", background_normal = "./resources/move_button.png", background_down = "./resources/move_button_pressed.png", selected = True)
        globvars.AllItems['undoButton'] = UndoButton(mode = "undo", background_normal = "./resources/undo_button.png", background_disabled_normal = "./resources/undo_button_disabled.png", background_down = "./resources/undo_button_pressed.png")
        globvars.AllItems['redoButton'] = UndoButton(mode = "redo", background_normal = "./resources/redo_button.png", background_disabled_normal = "./resources/redo_button_disabled.png", background_down = "./resources/redo_button_pressed.png")
        # Now we add all of the widgets, mostly anonymous
        self.add_widget(SwitchButton(mode = "menu", text = "Menu", direction = "right", newmode = "move", button = 'move', target = 'application'))
        self.add_widget(Spacer())
        self.add_widget(globvars.AllItems['move'])
        self.add_widget(MachineButton(mode = "create_s", background_normal = "./resources/state_button.png", background_down = "./resources/state_button_pressed.png"))
        self.add_widget(MachineButton(mode = "create_t", background_normal = "./resources/transition_button.png", background_down = "./resources/transition_button_pressed.png"))
        self.add_widget(MachineButton(mode = "delete", background_normal = "./resources/delete_button.png", background_down = "./resources/delete_button_pressed.png"))
        self.add_widget(MachineButton(mode = "start", background_normal = "./resources/start_button.png", background_down = "./resources/start_button_pressed.png"))
        self.add_widget(MachineButton(mode = "final", background_normal = "./resources/final_button.png", background_down = "./resources/final_button_pressed.png"))
        self.add_widget(AlphabetButton(background_normal = "./resources/alphabet_button.png", background_down = "./resources/alphabet_button_pressed.png"))
        self.add_widget(Spacer())
        self.add_widget(globvars.AllItems['undoButton'])
        self.add_widget(SaveButton(background_normal = "./resources/save_button.png", background_down = "./resources/save_button_pressed.png"))
        self.add_widget(globvars.AllItems['redoButton'])
        self.add_widget(Spacer())
        self.add_widget(SwitchButton(mode = "run", text = "Run", direction = "left", newmode = "run", button = None, target = 'toolbar'))

# DEBUG SECTION
class TuringApp(App):
    def build(self):
        return BuildToolbar()

if __name__ == '__main__':
    globvars.create()
    TuringApp().run()