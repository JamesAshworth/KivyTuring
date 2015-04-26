from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from buttons import ExtendButton, StickyButton, SwitchButton, Spacer
from logicthread import LogicThread
import globvars
import logic

class StepButton(StickyButton):
    def on_press(self):
        super(StepButton, self).on_press()
        # Sticky buttons leave themselves selected on press, so we deselect
        self.selected(False)
        globvars.AllItems['running'] = False
        logic.do_step()
        
class SpeedSlider(Slider):
    def __init__(self, *args, **kwargs):
        super(SpeedSlider, self).__init__(*args, **kwargs)
        self.bind(value=self.update_speed)
        self.max = 9
        
    def update_speed(self, instance, value):
        position = int(round(self.value))
        self.value = position
        globvars.AllItems['animationStep'] = 1.0 / (10 - position)
        
    def selected(self, selected):
        pass
        
class BuildButton(SwitchButton):
    def on_press(self):
        Clock.unschedule(globvars.AllItems['movementClock'])
        globvars.AllItems['running'] = False
        logic.end_simulation()
        for button in self.parent.children:
            button.selected(False)
        super(BuildButton, self).on_press()
        
class RunButton(StickyButton):
    def on_press(self):
        super(RunButton, self).on_press()
        globvars.AllItems['running'] = True
        logic.do_step()
        
class PauseButton(StickyButton):
    def on_press(self):
        super(PauseButton, self).on_press()
        # Sticky buttons leave themselves selected on press, so we deselect
        self.selected(False)
        globvars.AllItems['running'] = False
        
class CompletionButton(StickyButton):
    def on_press(self):
        super(CompletionButton, self).on_press()
        # Sticky buttons leave themselves selected on press, so we deselect
        self.selected(False)
        LogicThread().start()
        
class ResetButton(StickyButton):
    def on_press(self):
        super(ResetButton, self).on_press()
        self.selected(False)
        # If we're midway through a transition, stop the movement callback
        Clock.unschedule(globvars.AllItems['movementClock'])
        globvars.AllItems['running'] = False
        logic.reset_simulation()
            
class RunToolbar(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(RunToolbar, self).__init__(*args, **kwargs)
        globvars.AllItems['pauseButton'] = PauseButton(text = "Pause")
        self.add_widget(BuildButton(mode = "build", text = "Build", direction = "right", newmode = "move", button = globvars.AllItems['move']))
        self.add_widget(Spacer())
        self.add_widget(StepButton(text = "Step"))
        self.add_widget(RunButton(text = "Run"))
        self.add_widget(globvars.AllItems['pauseButton'])
        self.add_widget(ResetButton(text = "Reset"))
        self.add_widget(CompletionButton(text = "Run\nto\nFinish"))
        self.add_widget(Spacer())
        self.add_widget(SpeedSlider())
        self.add_widget(Spacer())

class TuringApp(App):
    def build(self):
        return RunToolbar()

if __name__ == '__main__':
    TuringApp().run()