from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from buttons import ExtendButton, StickyButton, SwitchButton, Spacer
import globvars
import logic

class StepButton(ExtendButton):
    def on_press(self):
        logic.do_step()
        
class BuildButton(SwitchButton):
    def on_press(self):
        logic.end_simulation()
        super(BuildButton, self).on_press()
        
class RunButton(StickyButton):
    def on_press(self):
        globvars.AllItems['running'] = True
        logic.do_step()
        super(RunButton, self).on_press()
        
class PauseButton(StickyButton):
    def on_press(self):
        globvars.AllItems['running'] = False
        super(PauseButton, self).on_press()
        # Sticky buttons leave themselves selected on press, so we deselect
        self.selected(False)
        
class ResetButton(StickyButton):
    def on_press(self):
        # If we're midway through a transition, stop the movement callback
        Clock.unschedule(globvars.AllItems['movementClock'])
        globvars.AllItems['running'] = False
        logic.reset_simulation()
        super(ResetButton, self).on_press()
        self.selected(False)
            
class RunToolbar(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(RunToolbar, self).__init__(*args, **kwargs)
        self.size_hint = 1, None
        self.height = 60
        self.add_widget(BuildButton(mode = "build", text = "Build", direction = "right", newmode = "move", button = globvars.AllItems['move']))
        self.add_widget(Spacer())
        self.add_widget(StepButton(text = "Step"))
        self.add_widget(RunButton(text = "Run"))
        self.add_widget(PauseButton(text = "Pause"))
        self.add_widget(ResetButton(text = "Reset"))
        self.add_widget(Spacer())

class TuringApp(App):
    def build(self):
        return RunToolbar()

if __name__ == '__main__':
    TuringApp().run()