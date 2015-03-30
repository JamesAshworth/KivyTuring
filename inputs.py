from kivy.uix.textinput import TextInput
from string import ascii_letters, digits
import globvars

class LengthConstrainedTextInput(TextInput):
    def __init__(self, length = 1, *args, **kwargs):
        super(LengthConstrainedTextInput, self).__init__(*args, **kwargs)
        self.length = length
        
    def insert_text(self, substring, from_undo=False):
        substring = substring[0:self.length - len(self.text)]
        return super(LengthConstrainedTextInput, self).insert_text(substring, from_undo = from_undo)

class LeftRightTextInput(LengthConstrainedTextInput):
    def insert_text(self, substring, from_undo=False):
        substring = substring.upper()
        for s in substring:
            if s == "L" or s == "R":
                return super(LeftRightTextInput, self).insert_text(s, from_undo = from_undo)
        return super(LeftRightTextInput, self).insert_text("", from_undo=from_undo)

class StateTextInput(LengthConstrainedTextInput):
    pass

class AlphabetTextInput(LengthConstrainedTextInput):
    def insert_text(self, substring, from_undo=False):
        for s in substring:
            if s in globvars.AllItems['alphabet']:
                return super(AlphabetTextInput, self).insert_text(s, from_undo = from_undo)
        return super(AlphabetTextInput, self).insert_text("", from_undo=from_undo)
        
class AlphabetDefinitionTextInput(TextInput):
    def __init__(self, feedback, *args, **kwargs):
        super(AlphabetDefinitionTextInput, self).__init__(*args, **kwargs)
        self.feedback = feedback
        
    def _tokenize(self, text):
        #We know we only have alphanumeric, but we want to break on a per character basis
        #So we overwrite this function
        if text is None:
            return
        oldindex = 0
        for index, char in enumerate(text):
            yield text[index]
            oldindex = index + 1
        yield text[oldindex:]
        
    def _split_smart(self, text):
        self.multiline = True
        lines, linesflags = super(AlphabetDefinitionTextInput, self)._split_smart(text)
        self.multiline = False
        return lines, linesflags
        
    def insert_text(self, substring, from_undo=False):
        self.feedback.text = ""
        newstring = ""
        for s in substring:
            if s not in ascii_letters + digits:
                self.feedback.text = "Alphabet is restricted to alphanumeric characters"
                s = ""
            elif s in self.text:
                self.feedback.text = "'" + s + "' is already in the alphabet"
                s = ""
            newstring += s
        return super(AlphabetDefinitionTextInput, self).insert_text(newstring, from_undo=from_undo)