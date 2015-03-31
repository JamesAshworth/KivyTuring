from inputs import AlphabetTextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
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
        self.labels = [0, 0]
        self.outofbounds = False
        self.allowshift = True
        globvars.AllItems['tape'] = self
        
    def make_cells(self):
        if not len(self.cells):
            self.cells = [TapeUnit(pos = (self.x, self.y), text = "0")]
            self.cells[0].selected(True)
            self.add_widget(self.cells[0])
            return True
        if self.cells[0].x > self.x:
            return self.make_cell(0)
        if self.cells[-1].x + self.cells[-1].width <= self.x + self.width:
            return self.make_cell(1)
        return False
        
    def make_cell(self, end):
        if end == 0:
            self.labels[0] -= 1
            self.cells.insert(0, TapeUnit(pos = ((self.cells[0].x - self.cells[0].width), self.y), text = str(self.labels[0])))
            self.add_widget(self.cells[0])
            return True
        if end == 1:
            self.labels[1] += 1
            self.cells.append(TapeUnit(pos = ((self.cells[-1].x + self.cells[-1].width), self.y), text = str(self.labels[1])))
            self.add_widget(self.cells[-1])
            return True
        return False
        
    def do_layout(self, *args, **kwargs):
        super(Tape, self).do_layout(*args, **kwargs)
        self.fill_cells()
        
    def fill_cells(self):
        while self.make_cells():
            pass
        
    def select_cell(self, location):
        location -= self.labels[0]
        location = self.exists(location)
        for cell in self.cells:
            cell.selected(False)
        self.cells[location].selected(True)
        self.on_screen(location)
        
    def exists(self, index):
        if index == -1:
            self.make_cell(0)
            return 0
        if index == len(self.cells):
            self.make_cell(1)
            return index
        return index
        
    def on_screen(self, index):
        cell = self.cells[index]
        if cell.x + cell.width > self.x + self.width:
            self.move_cells((self.x + self.width) - (cell.x + cell.width))
        if cell.x < self.x:
            self.move_cells((self.x - cell.x))
        
    def get_value(self, location):
        location -= self.labels[0]
        if self.cells[location].cell.text == "":
            return "_"
        return self.cells[location].cell.text
        
    def set_value(self, location, value):
        location -= self.labels[0]
        if value == "_":
            value = ""
        self.cells[location].cell.text = value
        
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
        for i in range(len(self.cells)):
            self.cells[i].update_label(str(self.labels[0] + i))
            self.cells[i].selected(False)
            self.cells[i].move(offset * self.cells[0].width)
        self.fill_cells()
        self.select_cell(0)
        
    def move_cells(self, offset):
        for cell in self.cells:
            cell.move(offset)
        self.offset -= (offset)
        self.fill_cells()
            
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
        for cell in self.cells:
            cell.move(self.offset)
        self.offset = 0