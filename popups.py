from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.label import Label
from inputs import LeftRightTextInput, AlphabetTextInput, StateTextInput, AlphabetDefinitionTextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
import globvars
        
class SpacedContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(SpacedContent, self).__init__(*args, **kwargs)
        self.size_hint = (1, None)
        self.height = 30
        super(SpacedContent, self).add_widget(Widget())
        self.lastwidget = Widget()
        super(SpacedContent, self).add_widget(self.lastwidget)
        
    def add_widget(self, *args, **kwargs):
        self.remove_widget(self.lastwidget)
        super(SpacedContent, self).add_widget(*args, **kwargs)
        super(SpacedContent, self).add_widget(self.lastwidget)

class CommonPopup(Popup):
    def __init__(self, *args, **kwargs):
        super(CommonPopup, self).__init__(*args, **kwargs)
        self.auto_dismiss = False
        self.content = BoxLayout(orientation = 'vertical')
        self.message = Label(height = 30, size_hint = (1, None))
        self.entry = SpacedContent()
        self.feedback = Label()
        self.buttonholder = SpacedContent()
        self.button = Button()
        self.buttonholder.add_widget(self.button)
        self.button.bind(on_press=self.dismiss)
        self.bind(on_dismiss=self.post_process)
        
    def assemble(self):
        self.content.add_widget(self.message)
        self.content.add_widget(self.entry)
        self.content.add_widget(self.feedback)
        self.content.add_widget(self.buttonholder)
        
    def open(self, *args, **kwargs):
        super(CommonPopup, self).open(*args, **kwargs)
        Clock.schedule_once(self.set_focus_text)
        
    def set_focus_text(self, instance):
        pass
        
    def post_process(self, instance):
        pass

class StateNamer(CommonPopup):
    def __init__(self, object, *args, **kwargs):
        # Forward send
        super(StateNamer, self).__init__(*args, **kwargs)
        # Set the key info for the user
        self.title = "State Name?"
        self.message.text = "Please provide a unique name for this state:"
        self.button.text = "Set Name"
        # Create the user input section
        self.textinput = StateTextInput(width = 80, size_hint = (None, 1), multiline = False, length = 4)
        self.textinput.bind(on_text_validate=self.dismiss)
        # Add this to the correct area
        self.entry.add_widget(self.textinput)
        # Set the parent and assemble the popup
        self.object = object
        self.assemble()
    
    def post_process(self, instance):
        if self.textinput.text == "":
            self.feedback.text = "State name can not be blank"
            Clock.schedule_once(self.set_focus_text)
            return True
        for state in globvars.AllItems['states']:
            if state == self.object:
                pass
            elif state.name == self.textinput.text:
                self.feedback.text = "State name is not unique"
                Clock.schedule_once(self.set_focus_text)
                return True
        self.object.set_text(self.textinput.text)
        return False
        
    def set_focus_text(self, instance):
        self.textinput.focus = True

class TransitionIdentifier(CommonPopup):
    def __init__(self, object, *args, **kwargs):
        # Forward send
        super(TransitionIdentifier, self).__init__(*args, **kwargs)
        # Set the key info for the user
        self.title = "Transition Details?"
        self.message.text = "Please provide read/write/movement info for this transition:"
        self.button.text = "Set Info"
        # Create the user input section
        self.textread = AlphabetTextInput(width = 30, size_hint = (None, 1), multiline = False)
        self.textwrite = AlphabetTextInput(width = 30, size_hint = (None, 1), multiline = False)
        self.textmove = LeftRightTextInput(width = 30, size_hint = (None, 1), multiline = False)
        self.textread.bind(on_text_validate=self.set_focus_text2)
        self.textwrite.bind(on_text_validate=self.set_focus_text3)
        self.textmove.bind(on_text_validate=self.dismiss)
        # Add this to the correct area
        self.entry.add_widget(self.textread)
        self.entry.add_widget(Label(width = 10, size_hint = (None, 1), text = "/"))
        self.entry.add_widget(self.textwrite)
        self.entry.add_widget(Label(width = 10, size_hint = (None, 1), text = "/"))
        self.entry.add_widget(self.textmove)
        # Set the parent and assemble the popup
        self.object = object
        self.assemble()
    
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
        # Forward send
        super(AlphabetEntry, self).__init__(*args, **kwargs)
        # Set the key info for the user
        self.title = "Alphabet Definition"
        self.message.text = "Please define the alphabet for this machine:"
        self.button.text = "Define"
        # Create the user input section
        # Add this to the correct area
        self.entry = AlphabetDefinitionTextInput(feedback = self.feedback, text = globvars.AllItems['alphabet'], multiline = False)
        self.entry.bind(on_text_validate=self.dismiss)
        # Set the parent and assemble the popup
        self.assemble()
        
    def set_focus_text(self, instance):
        self.entry.focus = True
        
    def post_process(self, instance):
        if self.entry.text == "":
            self.feedback.text = "Alphabet cannot be empty"
            return True
        globvars.AllItems['alphabet'] = self.entry.text
        return False
        
class ErrorBox(CommonPopup):
    def __init__(self, message, *args, **kwargs):
        # Forward send
        super(ErrorBox, self).__init__(*args, **kwargs)
        # Set the key info for the user
        self.title = "Error"
        self.message.text = message
        self.button.text = "Ok"
        self.size = (450, 150)
        # Create the user input section
        # Add this to the correct area
        # Set the parent and assemble the popup
        self.assemble()
        
    def assemble(self):
        self.content.add_widget(self.message)
        self.content.add_widget(self.buttonholder)
        