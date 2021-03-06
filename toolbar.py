from kivy.app import App
from buildtoolbar import BuildToolbar
from runtoolbar import RunToolbar
from kivy.uix.screenmanager import ScreenManager, Screen
import globvars
        
#----------------------------------------------------------
# Name: Toolbar
# 
# Entire toolbar subsystem, with screens for the build and
# run toolbars
#----------------------------------------------------------
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
        self.size_hint = (1, None)
        globvars.AllItems['application'].bind(width=self.set_height)
        
    def set_height(self, instance, width):
        self.height = width / 15
        
# DEBUG SECTION
class TuringApp(App):
    def build(self):
        return Toolbar()

if __name__ == '__main__':
    globvars.create()
    TuringApp().run()