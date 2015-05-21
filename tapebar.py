from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from buttons import ToolbarButton
from tape import Tape
import globvars
        
class ResetButton(ToolbarButton):
    def on_press(self):
        globvars.AllItems['tape'].reset_position()
        
class ShiftButton(ToolbarButton):
    def __init__(self, direction, *args, **kwargs):
        super(ShiftButton, self).__init__(*args, **kwargs)
        self.direction = direction
        
    def on_press(self):
        globvars.AllItems['tape'].shift_cells(self.direction)
        
class Tapebar(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Tapebar, self).__init__(*args, **kwargs)
        self.add_widget(ResetButton(text = "Reset\nTape\nPosition"))
        self.add_widget(ShiftButton(direction = -1))
        screen = Screen()
        screen.add_widget(Tape())
        sm = ScreenManager()
        sm.add_widget(screen)
        self.add_widget(sm)
        self.add_widget(ShiftButton(direction = +1))
        self.size_hint = (1, None)
        globvars.AllItems['application'].bind(width=self.set_height)
        
    def set_height(self, instance, width):
        self.height = width / 9

class TuringApp(App):
    def build(self):
        return Tapebar()
        
if __name__ == '__main__':
    globvars.create()
    TuringApp().run()