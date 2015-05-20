__version__ = '1.8'

from kivy.app import App
from startscreen import StartScreen
from machinescreen import MachineScreen
from kivy.uix.screenmanager import ScreenManager, Screen
import globvars

class Application(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        screen = Screen(name = "menu")
        startScreen = StartScreen()
        screen.add_widget(startScreen)
        screen.bind(on_pre_enter=startScreen.load_label)
        self.add_widget(screen)
        screen = Screen(name = "machine")
        screen.add_widget(MachineScreen())
        self.add_widget(screen)
        globvars.AllItems['application'] = self
        
class TuringApp(App):
    def open_settings(self, *largs):
        pass
        
    def build(self):
        return Application()

if __name__ == '__main__':
    globvars.create()
    TuringApp().run()