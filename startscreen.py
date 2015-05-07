from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from glob import glob
import globvars
import fileops

class StartLabel(Label):
    pass
        
class LoadLabel(StartLabel):
    def __init__(self, *args, **kwargs):
        super(LoadLabel, self).__init__(*args, **kwargs)
        self.size_hint = (1, None)
        self.height = 80
        self.halign = 'right'
        self.valign = 'top'
        self.padding = (-20, -20)
        
    def set_text(self, text):
        if text == '':
            self.text = ''
        else:
            self.text = '[ref=' + text + '.xml~]Reopen: ' + text + '[/ref]'
        
    def on_ref_press(self, instance):
        fileops.load_file(filename = instance)
        
class ControlLabel(StartLabel):
    def __init__(self, *args, **kwargs):
        super(ControlLabel, self).__init__(*args, **kwargs)
        self.size_hint = (None, None)
        self.height = 170
        self.width = 190
        
    def on_ref_press(self, ref):
        if ref == 'new':
            fileops.new_file(overwrite = False)
        if ref == 'load':
            fileops.load_file(overwrite = False)
        if ref == 'import':
            fileops.import_file(overwrite = False)
        if ref == 'delete':
            fileops.delete_file()
        
class StartScreen(GridLayout):
    def __init__(self, *args, **kwargs):
        super(StartScreen, self).__init__(*args, **kwargs)
        self.rows = 3
        self.loadlabel = LoadLabel()
        self.topRow = AnchorLayout(anchor_x='right', anchor_y='top')
        self.middleRow = AnchorLayout(anchor_x='center', anchor_y='center')
        self.add_widget(self.topRow)
        self.add_widget(self.middleRow)
        self.add_widget(Widget())
        self.topRow.add_widget(self.loadlabel)
        self.middleRow.add_widget(ControlLabel(text = '[ref=new]New Machine[/ref]\n\n[ref=load]Load Machine[/ref]\n\n[ref=import]Import Machine[/ref]\n\n[ref=delete]Delete Machine[/ref]'))
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