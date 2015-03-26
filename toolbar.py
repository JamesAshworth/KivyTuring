from kivy.app import App
from buildtoolbar import BuildToolbar
from runtoolbar import RunToolbar
from kivy.uix.screenmanager import ScreenManager, Screen
import globvars

class Toolbar(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)
        self.size_hint = (1, None)
        self.height = 60
        screen = Screen(name = "build")
        screen.add_widget(BuildToolbar())
        self.add_widget(screen)
        screen = Screen(name = "run")
        screen.add_widget(RunToolbar())
        self.add_widget(screen)
        globvars.AllItems['toolbar'] = self
        
class PrototypeApp(App):
    def build(self):
        return Toolbar()

if __name__ == '__main__':
    globvars.create()
    PrototypeApp().run()