from inputs import AlphabetTextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from math import ceil
import globvars

class TapeCell(AlphabetTextInput):
    def selected(self, selected):
        if selected:
            self.background_color = [1, 1, 0.5, 1]
        else:
            self.background_color = [1, 1, 1, 1]
        
class TapeLabel(Label):
    def collide_point(self, x, y):
        return False
        
class TapeUnit(BoxLayout):
    def __init__(self, text, *args, **kwargs):
        super(TapeUnit, self).__init__(*args, **kwargs)
        self.orientation = 'vertical'
        self.cell = TapeCell()
        self.add_widget(self.cell)
        self.label = TapeLabel(text = text)
        self.add_widget(self.label)
        self.savevalue = ""
        
    def move(self, dx):
        self.pos = (self.x + dx, self.y)
        
    def collide_point(self, x, y):
        return self.cell.collide_point(x, y)
        
    def selected(self, selected):
        self.cell.selected(selected)
        
    def update_label(self, text):
        self.label.text = text
        
class Tape(FloatLayout):
    def __init__(self, *args, **kwargs):
        super(Tape, self).__init__(*args, **kwargs)
        self.offset = 0
        self.cells = []
        self.labels = [0, -1]
        self.leftmost = 0
        self.numcells = 0
        self.cellwidth = TapeUnit("").width
        self.outofbounds = False
        self.allowshift = True
        globvars.AllItems['tape'] = self
        
    def make_cell(self, end):
        if end == 0:
            self.labels[0] -= 1
            self.cells.insert(0, TapeUnit(pos = (self.x + self.width, self.y), text = str(self.labels[0])))
            self.add_widget(self.cells[0])
            return True
        if end == 1:
            self.labels[1] += 1
            self.cells.append(TapeUnit(pos = (self.x + self.width, self.y), text = str(self.labels[1])))
            self.add_widget(self.cells[-1])
            return True
        return False
        
    def do_layout(self, *args, **kwargs):
        super(Tape, self).do_layout(*args, **kwargs)
        numcells = int(ceil(float(self.width) / float(self.cellwidth)))
        if self.numcells != numcells:
            self.numcells = numcells
            self.fill_cells()
            self.select_cell(0)
            self.reset_position()
        
    def fill_cells(self):
        self.move_cells(0)
            
    def get_cell(self, location):
        location -= self.labels[0]
        return self.exists(location)
        
    def select_cell(self, location, shift = True):
        location -= self.labels[0]
        location = self.exists(location)
        for cell in self.cells:
            cell.selected(False)
        self.cells[location].selected(True)
        if shift:
            self.center_cell(location + self.labels[0])
        
    def exists(self, index):
        while index < 0:
            self.make_cell(0)
            index += 1
        while index >= len(self.cells):
            self.make_cell(1)
        return index
        
    def center_cell(self, location):
        self.offset = (location - self.numcells / 2 + 1) * self.cellwidth
        self.move_cells(0)
        
    def get_value(self, location):
        location -= self.labels[0]
        location = self.exists(location)
        if self.cells[location].cell.text == "":
            return "_"
        return self.cells[location].cell.text
        
    def set_value(self, location, value):
        location -= self.labels[0]
        location = self.exists(location)
        if value == "_":
            value = ""
        self.cells[location].cell.text = value
        
    def load_tape(self, tapestring):
        try:
            location = tapestring.index('*')
            tapestring.replace('*', '')
        except:
            location = 0
        for value in list(tapestring):
            self.set_value(location, value)
            location += 1
        
    def save_values(self):
        for cell in self.cells:
            cell.savevalue = cell.cell.text
            
    def restore_values(self):
        for cell in self.cells:
            cell.cell.text = cell.savevalue
            cell.savevalue = ""
        
    def shift_cells(self, offset):
        if not self.allowshift:
            return
        self.labels[0] += offset
        self.labels[1] += offset
        self.offset += offset * self.cellwidth
        self.leftmost += offset
        for i in range(len(self.cells)):
            self.cells[i].update_label(str(self.labels[0] + i))
            self.cells[i].selected(False)
        self.move_cells(offset * self.cellwidth)
        self.select_cell(0, shift = False)
        
    def move_cells(self, offset):
        self.offset -= offset
        for i in range(self.numcells):
            self.cells[self.get_cell(self.leftmost + i)].pos = (self.x - self.cellwidth, self.y)
        self.leftmost = int(round(float(self.offset) / float(self.cellwidth)))
        for i in range(self.numcells):
            self.cells[self.get_cell(self.leftmost + i)].pos = (self.x + (self.cellwidth * i), self.y)
            
    def on_touch_down(self, touch):
        self.outofbounds = False
        if not self.collide_point(touch.x, touch.y):
            self.outofbounds = True
            return False
        touch.ud['last'] = touch.x
        for cell in self.cells:
            if cell.collide_point(touch.x, touch.y):
                cell.on_touch_down(touch)
                return False
        touch.ud['touched'] = self
        touch.ud['last'] = touch.x
        
    def on_touch_move(self, touch):
        if self.outofbounds:
            return False
        self.move_cells(touch.x - touch.ud['last'])
        touch.ud['last'] = touch.x
        
    def reset_position(self):
        self.move_cells(self.offset)