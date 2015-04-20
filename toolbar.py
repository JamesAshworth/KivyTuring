from kivy.app import App
from buildtoolbar import BuildToolbar
from runtoolbar import RunToolbar
from kivy.uix.screenmanager import ScreenManager, Screen
import globvars

class Toolbar(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)
        screen = Screen(name = "build")
        screen.add_widget(BuildToolbar())
        self.add_widget(screen)
        screen = Screen(name = "run")
        screen.add_widget(RunToolbar())
        self.add_widget(screen)
        globvars.AllItems['toolbar'] = self
        
class TuringApp(App):
    def build(self):
        return Toolbar()

if __name__ == '__main__':
    globvars.create()
    TuringApp().run()