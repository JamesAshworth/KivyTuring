from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.label import Label
from inputs import LeftRightTextInput, AlphabetTextInput, StateTextInput, AlphabetDefinitionTextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
import globvars

class CommonPopup(Popup):
    def __init__(self, *args, **kwargs):
        super(CommonPopup, self).__init__(*args, **kwargs)
        self.bind(on_dismiss=self.post_process)
        
    def open(self, *args, **kwargs):
        super(CommonPopup, self).open(*args, **kwargs)
        Clock.schedule_once(self.set_focus_text)
        
    def set_focus_text(self, instance):
        pass
        
    def post_process(self, instance):
        pass

class StateNamer(CommonPopup):
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

class TransitionIdentifier(CommonPopup):
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
    
    def post_process(self, instance):
        if self.textread.text == "":
            self.feedback.text = "Read character required"
            Clock.schedule_once(self.set_focus_text)
            return True
        for t in globvars.AllItems['transitions']:
            if t == self.object:
                pass
            elif t.startstate == self.object.startstate:
                if self.textread.text == t.info.label.text[0]:
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
        
class AlphabetEntry(CommonPopup):
    def __init__(self, *args, **kwargs):
        super(AlphabetEntry, self).__init__(*args, **kwargs)
        self.auto_dismiss = False
        self.title = "Alphabet Definition"
        self.content = BoxLayout()
        self.content.orientation = 'vertical'
        self.feedback = Label(size_hint = (1, None), height = 30)
        self.textinput = AlphabetDefinitionTextInput(feedback = self.feedback, text = globvars.AllItems['alphabet'])
        self.button = Button(text = "Define")
        self.button.bind(on_press=self.dismiss)
        buttonholder = BoxLayout(size_hint = (1, None), height = 30)
        buttonholder.add_widget(Widget())
        buttonholder.add_widget(self.button)
        buttonholder.add_widget(Widget())
        self.content.add_widget(Label(height = 30, size_hint = (1, None), text = "Please define the alphabet for this machine:"))
        self.content.add_widget(self.textinput)
        self.content.add_widget(self.feedback)
        self.content.add_widget(buttonholder)
        
    def set_focus_text(self, instance):
        self.textinput.focus = True
        
    def post_process(self, instance):
        if self.textinput.text == "":
            self.feedback.text = "Alphabet cannot be blank"
            return True
        globvars.AllItems['alphabet'] = self.textinput.text
        return False