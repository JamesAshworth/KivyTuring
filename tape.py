from inputs import AlphabetTextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from math import ceil
from undo import UndoTapeEdit, UndoTapeShift
import globvars

class TapeCell(AlphabetTextInput):
    def __init__(self, *args, **kwargs):
        super(TapeCell, self).__init__(*args, **kwargs)
        self.bind(text=self.on_text)

    def set_highlight(self, highlighted):
        if highlighted:
            self.background_color = [1, 1, 0.5, 1]
        else:
            self.background_color = [1, 1, 1, 1]
            
    def on_text(self, instance, value):
        # Replace blank values with underscores
        if value == "":
            value = "_"
        globvars.AllItems['tape'].set_value(self.parent.get_label(), value)
        
    def on_touch_down(self, touch):
        super(TapeCell, self).on_touch_down(touch)
        self.select_all()
        # If we're not allowed to be editing the cell, we defocus immediately
        self.focus = globvars.AllItems['tape'].allowedits
        
class TapeLabel(Label):
    def collide_point(self, x, y):
        # Labels don't exist, for the purposes of clicking
        return False
        
class TapeUnit(BoxLayout):
    def __init__(self, index, *args, **kwargs):
        super(TapeUnit, self).__init__(*args, **kwargs)
        self.orientation = 'vertical'
        self.cell = TapeCell()
        self.add_widget(self.cell)
        self.label = TapeLabel()
        self.add_widget(self.label)
        self.size_hint = (None, 1)
        self.index = index
        self.set_width(None, globvars.AllItems['application'].width)
        globvars.AllItems['application'].bind(width=self.set_width)
        
    def set_width(self, instance, width):
        self.width = width / 18
        self.pos = (self.width * self.index, 0)
        self.label.font_size = width / 48
        self.cell.font_size = width / 48
        self.cell.padding_x = width / 48
        if ((len(self.label.text)) > 4):
            self.label.font_size = width / (12 * (len(self.label.text)))
        
    def move(self, dx):
        self.pos = (self.x + dx, self.y)
        
    def collide_point(self, x, y):
        return self.cell.collide_point(x, y)
        
    def set_highlight(self, highlighted):
        self.cell.set_highlight(highlighted)
        
    def set_info(self, text, value):
        text = str(text)
        width = globvars.AllItems['application'].width / 12
        self.label.font_size = min(width / len(text), width / 4)
        self.label.text = text
        if value == "_":
            value = ""
        self.cell.text = value
        
    def get_value(self):
        value = self.cell.text
        if value == "":
            value = "_"
        return value
        
    def get_label(self):
        if self.label.text == "":
            return 0
        return int(self.label.text)
        
    def defocus(self):
        self.cell.focus = False
        
class Tape(FloatLayout):
    def __init__(self, *args, **kwargs):
        super(Tape, self).__init__(*args, **kwargs)
        self.cells = []
        # Default to cell 0 on the far left
        self.leftmost = 0
        # Zero position refers to the index of cell 0 in the tape list
        self.zeroposition = 0
        self.savezeroposition = 0
        # The number of cells (and partial cells) displayed on screen
        self.numcells = 0
        # Default to cell 0 highlighted
        self.selected = 0
        self.allowedits = True
        # Cell width will be set later
        self.cellwidth = 0
        # Tape is empty when we first start the app - if a machine is loaded, we'll get a populated tape
        self.tape = []
        self.savetape = []
        self.outofbounds = False
        globvars.AllItems['tape'] = self
        self.set_width(None, globvars.AllItems['application'].width)
        globvars.AllItems['application'].bind(width=self.set_width)
        
    def set_width(self, instance, width):
        self.cellwidth = width / 18
        
    def make_cell(self):
        self.cells.append(TapeUnit(index = self.numcells))
        self.add_widget(self.cells[-1])
        
    def do_layout(self, *args, **kwargs):
        super(Tape, self).do_layout(*args, **kwargs)
        numcells = int(ceil(float(self.width) / float(self.cellwidth)))
        while self.numcells < numcells:
            self.make_cell()
            self.numcells += 1
        self.display_tape()
            
    def exists(self, location):
        index = self.zeroposition + location
        while index < 0:
            self.tape.insert(0, '_')
            self.zeroposition += 1
            index = self.zeroposition + location
        while index >= len(self.tape):
            self.tape.append('_')
            
    def display_tape(self):
        location = self.leftmost
        for cell in self.cells:
            self.exists(location)
            cell.set_info(location, self.tape[self.zeroposition + location])
            cell.set_highlight(location == self.selected)
            cell.defocus()
            location += 1
        
    def select_cell(self, location, shift = True):
        self.selected = location
        if shift:
            self.center_cell(location)
        else:
            self.display_tape()
        
    def center_cell(self, location):
        self.leftmost = (location - self.numcells / 2 + 1)
        self.display_tape()
        
    def get_value(self, location):
        self.exists(location)
        return self.tape[self.zeroposition + location]
        
    def set_value(self, location, value, undoPossible = True):
        self.exists(location)
        if self.tape[self.zeroposition + location] != value:
            oldtape = list(self.tape)
            self.tape[self.zeroposition + location] = value
            if undoPossible:
                UndoTapeEdit(oldtape, self.zeroposition)
        self.display_tape()
        
    def get_tape(self):
        return list(self.tape)
        
    def get_tape_string(self):
        tape = self.get_tape()
        tape.insert(self.zeroposition + 1, '*')
        tape.insert(self.zeroposition, '*')
        while tape[0] == '_':
            tape.pop(0)
        while tape[-1] == '_':
            tape.pop()
        return ''.join(map(str, tape))
        
    def load_tape(self, tapestring):
        self.clear_tape()
        try:
            location = tapestring.index('*')
            tapestring = tapestring.replace('*', '')
        except:
            location = 0
        self.tape = list(tapestring)
        self.zeroposition = location
        self.display_tape()
            
    def clear_tape(self):
        self.tape = []
        self.display_tape()
        
    def save_values(self):
        self.savetape = list(self.tape)
        self.savezeroposition = self.zeroposition
            
    def restore_values(self):
        self.tape = list(self.savetape)
        self.zeroposition = self.savezeroposition
        self.display_tape()
        
    def shift_cells(self, offset, undoPossible = True):
        if not self.allowedits:
            return
        self.zeroposition -= offset
        if undoPossible:
            UndoTapeShift(offset)
        self.display_tape()
        
    def move_cells(self, touch):
        self.leftmost = touch.ud['leftmost'] - int(round(float(touch.x - touch.ud['last']) / float(self.cellwidth)))
        self.display_tape()
            
    def on_touch_down(self, touch):
        self.outofbounds = False
        if not self.collide_point(touch.x, touch.y):
            self.outofbounds = True
            return False
        touch.ud['last'] = touch.x
        touch.ud['leftmost'] = self.leftmost
        for cell in self.cells:
            if cell.collide_point(touch.x, touch.y):
                cell.on_touch_down(touch)
                return False
        touch.ud['touched'] = self
        
    def on_touch_move(self, touch):
        if self.outofbounds:
            return False
        for cell in self.cells:
            if cell.collide_point(touch.x, touch.y):
                touch.ud['last'] = touch.x
                touch.ud['leftmost'] = self.leftmost
                cell.on_touch_down(touch)
                return False
        self.move_cells(touch)
        
    def reset_position(self):
        self.leftmost = 0
        self.display_tape()