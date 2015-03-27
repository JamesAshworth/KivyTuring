from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.label import Label
from inputs import LeftRightTextInput, AlphabetTextInput, StateTextInput
from kivy.uix.widget import Widget
import globvars

class StateNamer(Popup):
    def __init__(self, object, *args, **kwargs):
        super(StateNamer, self).__init__(*args, **kwargs)
        self.auto_dismiss = False
        self.title = "State Name?"
        self.content = BoxLayout()
        self.content.orientation = 'vertical'
        self.content.add_widget(Label(height = 30, size_hint = (1, None), text = "Please provide a unique name for this state:"))
        info = BoxLayout(height = 30, size_hint = (1, None))
        info.add_widget(Widget())
        self.textinput = StateTextInput(width = 80, size_hint = (None, 1), multiline = False, length = 4)
        info.add_widget(self.textinput)
        info.add_widget(Widget())
        self.textinput.bind(on_text_validate=self.dismiss)
        self.content.add_widget(info)
        self.feedback = Label()
        self.content.add_widget(self.feedback)
        self.object = object
        self.bind(on_dismiss=self.post_process)
        
    def open(self, *args, **kwargs):
        super(StateNamer, self).open(*args, **kwargs)
        Clock.schedule_once(self.set_focus_text)
    
    def post_process(self, instance):
        if self.textinput.text == "":
            self.feedback.text = "State name can not be blank"
            Clock.schedule_once(self.set_focus_text)
            return True
        for state in globvars.AllItems['states']:
            if state == self.object:
                pass
            elif state.text == self.textinput.text:
                self.feedback.text = "State name is not unique"
                Clock.schedule_once(self.set_focus_text)
                return True
        self.object.set_text(self.textinput.text)
        return False
        
    def set_focus_text(self, instance):
        self.textinput.focus = True

class TransitionIdentifier(Popup):
    def __init__(self, object, *args, **kwargs):
        super(TransitionIdentifier, self).__init__(*args, **kwargs)
        self.auto_dismiss = False
        self.title = "Transition Details?"
        self.content = BoxLayout()
        self.content.orientation = 'vertical'
        self.content.add_widget(Label(height = 30, size_hint = (1, None), text = "Please provide read/write/movement info for this transition:"))
        info = BoxLayout(height = 30, size_hint = (1, None))
        info.add_widget(Widget())
        self.textread = AlphabetTextInput(width = 30, size_hint = (None, 1), multiline = False)
        info.add_widget(self.textread)
        info.add_widget(Label(width = 10, size_hint = (None, 1), text = "/"))
        self.textwrite = AlphabetTextInput(width = 30, size_hint = (None, 1), multiline = False)
        info.add_widget(self.textwrite)
        info.add_widget(Label(width = 10, size_hint = (None, 1), text = "/"))
        self.textmove = LeftRightTextInput(width = 30, size_hint = (None, 1), multiline = False)
        info.add_widget(self.textmove)
        info.add_widget(Widget())
        self.textread.bind(on_text_validate=self.set_focus_text2)
        self.textwrite.bind(on_text_validate=self.set_focus_text3)
        self.textmove.bind(on_text_validate=self.dismiss)
        self.content.add_widget(info)
        self.feedback = Label()
        self.content.add_widget(self.feedback)
        self.object = object
        self.bind(on_dismiss=self.post_process)
        
    def open(self, *args, **kwargs):
        super(TransitionIdentifier, self).open(*args, **kwargs)
        Clock.schedule_once(self.set_focus_text)
    
    def post_process(self, instance):
        if self.textread.text == "":
            self.feedback.text = "Read character required"
            Clock.schedule_once(self.set_focus_text)
            return True
        for t in globvars.AllItems['transitions']:
            if t == self.object:
                pass
            elif t.startstate == self.object.startstate:
                if ("~" + self.textread.text + "/") in ("~" + t.info.label.text):
                    self.feedback.text = "Transition is not unique"
                    Clock.schedule_once(self.set_focus_text)
                    return True
        if self.textwrite.text == "":
            self.feedback.text = "Write character required"
            Clock.schedule_once(self.set_focus_text2)
            return True
        if self.textmove.text == "":
            self.feedback.text = "Movement must be [L]eft or [R]ight"
            Clock.schedule_once(self.set_focus_text2)
            return True
        self.object.set_info(self.textread.text + "/" + self.textwrite.text + "/" + self.textmove.text)
        return False
        
    def set_focus_text(self, instance):
        self.textread.focus = True
        
    def set_focus_text2(self, instance):
        self.textwrite.focus = True
        
    def set_focus_text3(self, instance):
        self.textmove.focus = True