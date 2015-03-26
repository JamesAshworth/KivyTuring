from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from toolbar import Toolbar
from statemachine import StateMachine
from tapebar import Tapebar
import globvars
        
class MachineScreen(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(MachineScreen, self).__init__(*args, **kwargs)
        self.orientation = 'vertical'
        self.add_widget(Toolbar())
        self.add_widget(StateMachine())
        self.add_widget(Tapebar())
        
class TuringApp(App):
    def build(self):
        return MachineScreen()
        
if __name__ == '__main__':
    globvars.create()
    TuringApp().run()