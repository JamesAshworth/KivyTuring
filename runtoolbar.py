from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from buttons import SwitchButton, Spacer
import globvars
            
class RunToolbar(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(RunToolbar, self).__init__(*args, **kwargs)
        self.size_hint = 1, None
        self.height = 60
        self.add_widget(SwitchButton(mode = "build", text = "Build", direction = "right", newmode = "move", button = globvars.AllItems['move']))
        self.add_widget(Spacer())

class PrototypeApp(App):
    def build(self):
        return RunToolbar()

if __name__ == '__main__':
    PrototypeApp().run()