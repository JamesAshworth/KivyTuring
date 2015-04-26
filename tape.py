from inputs import AlphabetTextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from math import ceil
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
        if value == "":
            value = "_"
        globvars.AllItems['tape'].set_value(self.parent.get_label(), value)
        
    def on_touch_down(self, touch):
        super(TapeCell, self).on_touch_down(touch)
        self.focus = globvars.AllItems['tape'].allowedits
        
class TapeLabel(Label):
    def collide_point(self, x, y):
        return False
        
class TapeUnit(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(TapeUnit, self).__init__(*args, **kwargs)
        self.orientation = 'vertical'
        self.cell = TapeCell()
        self.add_widget(self.cell)
        self.label = TapeLabel()
        self.add_widget(self.label)
        
    def move(self, dx):
        self.pos = (self.x + dx, self.y)
        
    def collide_point(self, x, y):
        return self.cell.collide_point(x, y)
        
    def set_highlight(self, highlighted):
        self.cell.set_highlight(highlighted)
        
    def set_info(self, text, value):
        text = str(text)
        self.label.font_size = min(80 / len(text), 20)
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
        self.leftmost = 0
        self.zeroposition = 0
        self.savezeroposition = 0
        self.numcells = 0
        self.selected = 0
        self.allowedits = True
        self.cellwidth = TapeUnit().width
        self.tape = []
        self.savetape = []
        self.outofbounds = False
        globvars.AllItems['tape'] = self
        
    def make_cell(self):
        self.cells.append(TapeUnit(pos = (self.x + self.cellwidth * self.numcells, self.y)))
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
        
    def set_value(self, location, value):
        self.exists(location)
        self.tape[self.zeroposition + location] = value
        self.display_tape()
        
    def get_tape(self):
        return list(self.tape)
        
    def load_tape(self, tapestring):
        self.clear_tape()
        try:
            location = tapestring.index('*')
            tapestring.replace('*', '')
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
        
    def shift_cells(self, offset):
        if not self.allowedits:
            return
        self.zeroposition -= offset
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
        self.move_cells(touch)
        
    def reset_position(self):
        self.leftmost = 0
        self.display_tape()