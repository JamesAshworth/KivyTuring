from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from buttons import ExtendButton, StickyButton, SwitchButton, Spacer
from logicthread import LogicThread
import globvars
import logic
        
#----------------------------------------------------------
# Name: StepButton
# 
# Button to do one step on the machine while running
# Acts as if pause has been pressed as well, to stop the
# machine if it is running
#----------------------------------------------------------
class StepButton(StickyButton):
    def on_press(self):
        super(StepButton, self).on_press()
        # Sticky buttons leave themselves selected on press, so we deselect
        self.selected(False)
        globvars.AllItems['running'] = False
        logic.do_step()
        
#----------------------------------------------------------
# Name: SpeedSlider
# 
# Slider widget used to adjust the speed of animation (and
# thus the speed of simulation)
# Can change the speed from 1 to 10 steps per second
#----------------------------------------------------------
class SpeedSlider(Slider):
    def __init__(self, *args, **kwargs):
        super(SpeedSlider, self).__init__(*args, **kwargs)
        self.bind(value=self.update_speed)
        self.max = 9
        
    def update_speed(self, instance, value):
        position = int(round(self.value))
        self.value = position
        # We do one animation step every 0.1 seconds, so we adjust the size of the step from 0.1 to 1 to change the speed
        globvars.AllItems['animationStep'] = 1.0 / (10 - position)
        
    def selected(self, selected):
        # All elements on the toolbar have this, so we can deselect everything easily
        pass
        
#----------------------------------------------------------
# Name: BuildButton
# 
# Switch button to change the toolbar back to build config
# but we also need to end a simulation if it's running and
# deselect all the buttons
#----------------------------------------------------------
class BuildButton(SwitchButton):
    def on_press(self):
        Clock.unschedule(globvars.AllItems['movementClock'])
        globvars.AllItems['running'] = False
        logic.end_simulation()
        for button in self.parent.children:
            button.selected(False)
        super(BuildButton, self).on_press()
        
#----------------------------------------------------------
# Name: RunButton
# 
# Like step, but each step triggers the next step, so we
# get continuous operation
#----------------------------------------------------------
class RunButton(StickyButton):
    def on_press(self):
        super(RunButton, self).on_press()
        globvars.AllItems['running'] = True
        logic.do_step()
        
#----------------------------------------------------------
# Name: PauseButton
# 
# Stops each step from triggering the next step, to pause
#----------------------------------------------------------
class PauseButton(StickyButton):
    def on_press(self):
        super(PauseButton, self).on_press()
        # Sticky buttons leave themselves selected on press, so we deselect
        self.selected(False)
        globvars.AllItems['running'] = False
        
#----------------------------------------------------------
# Name: CompletionButton
# 
# Creates a new thread and runs the machine to completion
# from initial state with no animation (much faster)
#----------------------------------------------------------
class CompletionButton(StickyButton):
    def on_press(self):
        super(CompletionButton, self).on_press()
        # Sticky buttons leave themselves selected on press, so we deselect
        self.selected(False)
        LogicThread().start()
        
#----------------------------------------------------------
# Name: ResetButton
# 
# Does a super pause, stopping movement midway through a
# transition, then returns everything to initial values
#----------------------------------------------------------
class ResetButton(StickyButton):
    def on_press(self):
        super(ResetButton, self).on_press()
        self.selected(False)
        # If we're midway through a transition, stop the movement callback
        Clock.unschedule(globvars.AllItems['movementClock'])
        globvars.AllItems['running'] = False
        logic.reset_simulation()
        
#----------------------------------------------------------
# Name: BuildToolbar
# 
# Toolbar for the simulation screen
#----------------------------------------------------------
class RunToolbar(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(RunToolbar, self).__init__(*args, **kwargs)
        # These buttons need to be accessible externally, so we'll explicitly store references to them in the global area
        globvars.AllItems['pauseButton'] = PauseButton(text = "Pause")
        # Now we add all of the widgets, mostly anonymous
        self.add_widget(BuildButton(mode = "build", text = "Build", direction = "right", newmode = "move", button = 'move', target = 'toolbar'))
        self.add_widget(Spacer())
        self.add_widget(StepButton(text = "Step"))
        self.add_widget(RunButton(text = "Run"))
        self.add_widget(globvars.AllItems['pauseButton'])
        self.add_widget(ResetButton(text = "Reset"))
        self.add_widget(CompletionButton(text = "Run\nto\nFinish"))
        self.add_widget(Spacer())
        self.add_widget(SpeedSlider())
        self.add_widget(Spacer())

# DEBUG SECTION
class TuringApp(App):
    def build(self):
        return RunToolbar()

if __name__ == '__main__':
    globvars.create()
    TuringApp().run()