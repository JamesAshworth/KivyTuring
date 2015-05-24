from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from glob import glob
import globvars
import fileops
        
class ControlLabel(Button):
    def __init__(self, text, *args, **kwargs):
        super(ControlLabel, self).__init__(text="[color=#000000]" + text + "[/color]", *args, **kwargs)
        self.markup = True
        self.background_normal = ""
        self.background_down = ""
        self.background_disabled_normal = ""
        globvars.AllItems['application'].bind(width=self.set_width)
        
    def set_width(self, instance, width):
        self.font_size = width / 25
        
class NewMachineLabel(ControlLabel):
    def __init__(self, *args, **kwargs):
        super(NewMachineLabel, self).__init__(text="New Machine", *args, **kwargs)
        
    def on_press(self):
        fileops.new_file(overwrite = False)
        
class LoadMachineLabel(ControlLabel):
    def __init__(self, *args, **kwargs):
        super(LoadMachineLabel, self).__init__(text="Load Machine", *args, **kwargs)
      
    def on_press(self):
        fileops.load_file(overwrite = False)
        
class ImportMachineLabel(ControlLabel):
    def __init__(self, *args, **kwargs):
        super(ImportMachineLabel, self).__init__(text="Import Machine", *args, **kwargs)
      
    def on_press(self):
        fileops.import_file(overwrite = False)
        
class DeleteMachineLabel(ControlLabel):
    def __init__(self, *args, **kwargs):
        super(DeleteMachineLabel, self).__init__(text="Delete Machine", *args, **kwargs)
      
    def on_press(self):
        fileops.delete_file()
        
class ReloadMachineLabel(ControlLabel):
    def __init__(self, *args, **kwargs):
        super(ReloadMachineLabel, self).__init__(text="", *args, **kwargs)
        self.set_text("");
        
    def set_text(self, text):
        if text == '':
            self.text = ''
            self.disabled = True
        else:
            self.text = '[color=#000000]Reopen: ' + text + '[/color]'
            self.instance = text + '.xml~'
            self.disabled = False
        
    def on_press(self):
        fileops.load_file(filename = self.instance)
        
class StartScreen(GridLayout):
    def __init__(self, *args, **kwargs):
        super(StartScreen, self).__init__(*args, **kwargs)
        self.rows = 3
        self.loadlabel = ReloadMachineLabel()
        self.topRow = AnchorLayout(anchor_x='right', anchor_y='top')
        self.middleRow = GridLayout(rows=4)
        self.add_widget(self.topRow)
        self.add_widget(self.middleRow)
        self.add_widget(Widget())
        self.topRow.add_widget(self.loadlabel)
        self.middleRow.add_widget(NewMachineLabel())
        self.middleRow.add_widget(LoadMachineLabel())
        #self.middleRow.add_widget(ImportMachineLabel())
        self.middleRow.add_widget(DeleteMachineLabel())
        self.load_label()
        globvars.AllItems['refreshLabel'] = self.load_label
        globvars.AllItems['refreshLabel']()
        
    def load_label(self, instance = None):
        filenames = glob('*.xml~')
        filenames.append('')
        self.loadlabel.set_text(filenames[0][:-5])
        
class TuringApp(App):
    def build(self):
        return StartScreen()
        
if __name__ == '__main__':
    globvars.create()
    globvars.AllItems['alphabet'] = "_01"
    TuringApp().run()