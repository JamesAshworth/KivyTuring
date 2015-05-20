from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from inputs import LeftRightTextInput, AlphabetTextInput, LengthConstrainedTextInput, AlphabetDefinitionTextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from os.path import isfile
import globvars
        
class SpacedContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(SpacedContent, self).__init__(*args, **kwargs)
        super(SpacedContent, self).add_widget(Widget(size_hint = (0.01, 1)))
        self.lastwidget = Widget(size_hint = (0.01, 1))
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
        self.message = Label(height = 120, size_hint = (1, None))
        self.entry = SpacedContent(height = 120, size_hint = (1, None))
        self.feedback = Label(height = 120, size_hint = (1, None), valign = 'top', halign = 'center')
        self.feedback.bind(size = self.feedback.setter('text_size')) 
        self.buttonholder = SpacedContent(height = 120, size_hint = (1, None))
        self.button = Button()
        self.cancel = Button(text = "Cancel")
        self.buttonholder.add_widget(self.button)
        self.buttonholder.add_widget(self.cancel)
        self.button.bind(on_press=self.dismiss)
        self.cancel.bind(on_press=self.on_cancel)
        self.bind(on_dismiss=self.post_process)
        self.content.add_widget(self.message)
        self.content.add_widget(self.entry)
        self.content.add_widget(self.feedback)
        self.content.add_widget(self.buttonholder)
        self.content.add_widget(Widget())
        
    def on_cancel(self, instance):
        self.unbind(on_dismiss=self.post_process)
        self.dismiss()
        
    def open(self, *args, **kwargs):
        super(CommonPopup, self).open(*args, **kwargs)
        Clock.schedule_once(self.set_focus_text)
        
    def set_focus_text(self, instance):
        pass
        
    def post_process(self, instance):
        pass

class StateNamer(CommonPopup):
    def __init__(self, object, text, *args, **kwargs):
        # Forward send
        super(StateNamer, self).__init__(*args, **kwargs)
        # Set the key info for the user
        self.title = "State Name?"
        self.message.text = "Please provide a unique name for this state:"
        self.button.text = "Set Name"
        # Create the user input section
        self.textinput = LengthConstrainedTextInput(width = 160, size_hint = (None, 1), multiline = False, length = 4, text = text)
        self.textinput.bind(on_text_validate=self.dismiss)
        # Add this to the correct area
        self.entry.add_widget(self.textinput)
        # Set the parent
        self.object = object
        
    def open(self):
        super(StateNamer, self).open()
        self.textinput.select_all()
    
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
    def __init__(self, object, read, write, move, *args, **kwargs):
        # Forward send
        super(TransitionIdentifier, self).__init__(*args, **kwargs)
        # Set the key info for the user
        self.title = "Transition Details?"
        self.message.text = "Please provide read/write/movement info for this transition:"
        self.button.text = "Set Info"
        # Create the user input section
        self.textread = AlphabetTextInput(width = 60, size_hint = (None, 1), multiline = False, text = read)
        self.textwrite = AlphabetTextInput(width = 60, size_hint = (None, 1), multiline = False, text = write)
        self.textmove = LeftRightTextInput(width = 60, size_hint = (None, 1), multiline = False, text = move)
        self.textread.bind(on_text_validate=self.set_focus_text2)
        self.textwrite.bind(on_text_validate=self.set_focus_text3)
        self.textmove.bind(on_text_validate=self.dismiss)
        # Add this to the correct area
        self.entry.add_widget(self.textread)
        self.entry.add_widget(Label(width = 20, size_hint = (None, 1), text = "/"))
        self.entry.add_widget(self.textwrite)
        self.entry.add_widget(Label(width = 20, size_hint = (None, 1), text = "/"))
        self.entry.add_widget(self.textmove)
        # Set the parent
        self.object = object
        
    def open(self):
        super(TransitionIdentifier, self).open()
        self.textread.select_all()
    
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
        self.object.set_initial_info(self.textread.text + "/" + self.textwrite.text + "/" + self.textmove.text)
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
        self.entry.height = 120
        input = AlphabetDefinitionTextInput(feedback = self.feedback, text = globvars.AllItems['alphabet'], multiline = False)
        input.bind(on_text_validate=self.dismiss)
        # Add this to the correct area
        self.entry.add_widget(input)
        
    def set_focus_text(self, instance):
        self.entry.focus = True
        
    def post_process(self, instance):
        if self.entry.text == "":
            self.feedback.text = "Alphabet cannot be empty"
            return True
        if "_" not in self.entry.text:
            self.entry.text = "_" + self.entry.text
        globvars.AllItems['alphabet'] = self.entry.text
        return False
        
class InfoBox(CommonPopup):
    def __init__(self, message, title, *args, **kwargs):
        # Forward send
        super(InfoBox, self).__init__(*args, **kwargs)
        # Set the key info for the user
        self.title = title
        self.message.text = message
        self.button.text = "Ok"
        self.buttonholder.remove_widget(self.cancel)
        self.content.remove_widget(self.entry)
        self.content.remove_widget(self.feedback)
        
class ErrorBox(InfoBox):
    def __init__(self, message, *args, **kwargs):
        super(ErrorBox, self).__init__(message=message, title="Error", *args, **kwargs)
        
class FileChooser(Popup):
    def __init__(self, proc, *args, **kwargs):
        super(FileChooser, self).__init__(*args, **kwargs)
        self.continuer = proc
        self.auto_dismiss = False
        self.title = "Choose file"
        self.content = BoxLayout(orientation = 'vertical')
        filechooser = FileChooserListView(filters=['*.xml'], filter_dirs=True, path="./")
        cancel = Button(text = "Cancel")
        filechooser.bind(selection=self.on_select)
        cancel.bind(on_press=self.dismiss)
        buttonholder = BoxLayout(orientation = 'horizontal', size_hint_y = None, height = 30)
        buttonholder.add_widget(Widget())
        buttonholder.add_widget(cancel)
        buttonholder.add_widget(Widget())
        self.content.add_widget(filechooser)
        self.content.add_widget(buttonholder)
        
    def on_select(self, instance, selection):
        self.continuer(filename = selection[0])
        self.dismiss()

class FileNamer(CommonPopup):
    def __init__(self, proc, *args, **kwargs):
        self.continuer = proc
        # Forward send
        super(FileNamer, self).__init__(*args, **kwargs)
        # Set the key info for the user
        self.title = "New Turing Machine"
        self.message.text = "Please provide a name for this turing machine:"
        self.button.text = "Create"
        # Create the user input section
        input = TextInput(multiline = False)
        input.bind(on_text_validate=self.dismiss)
        self.entry.add_widget(input)
        # Assemble the popup
    
    def post_process(self, instance):
        if self.entry.text == "":
            self.feedback.text = "Name cannot be blank"
            Clock.schedule_once(self.set_focus_text)
            return True
        if isfile(self.entry.text + '.xml'):
            self.feedback.text = "Machine already exists"
            Clock.schedule_once(self.set_focus_text)
            return True
        self.continuer(filename = (self.entry.text + '.xml'))
        return False
        
    def set_focus_text(self, instance):
        self.entry.focus = True

class FileOverwriter(CommonPopup):
    def __init__(self, filename, delproc, proc, *args, **kwargs):
        super(FileOverwriter, self).__init__(*args, **kwargs)
        self.filename = filename
        self.deleter = delproc
        self.continuer = proc
        self.title = "Overwrite?"
        self.feedback.text = ("If you continue, you could lose information from %s.\nAre you sure you wish to continue?" % filename.replace('.xml~', ''))
        self.button.text = "Continue"
        # Assemble the popup
        self.content.add_widget(self.feedback)
        self.content.add_widget(self.buttonholder)
    
    def post_process(self, instance):
        self.deleter(self.filename)
        self.continuer()