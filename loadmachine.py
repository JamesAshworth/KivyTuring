from statemachine import create_state, create_transition
from xml.etree.ElementTree import parse as xmlparse
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
import globvars
import statefuncs
import undo
        
class FileChooser(Popup):
    def __init__(self, *args, **kwargs):
        super(FileChooser, self).__init__(*args, **kwargs)
        self.auto_dismiss = False
        self.title = "Load file"
        self.content = BoxLayout(orientation = 'vertical')
        filechooser = FileChooserListView(path="~")
        cancel = Button(text = "cancel")
        filechooser.bind(selection=self.on_select)
        cancel.bind(on_press=self.dismiss)
        buttonholder = BoxLayout(orientation = 'horizontal', size_hint_y = None, height = 30)
        buttonholder.add_widget(Widget())
        buttonholder.add_widget(cancel)
        buttonholder.add_widget(Widget())
        self.content.add_widget(filechooser)
        self.content.add_widget(buttonholder)
        
    def on_select(self, instance, selection):
        load_machine(selection[0])
        self.dismiss()

def load_machine(filename):
    machineSpecs = xmlparse(filename).getroot()
     
    blank = machineSpecs.find('blank').attrib['char']
    
    alphabetstring = machineSpecs.find('alphabet').text.replace(blank, '_')
    globvars.AllItems['alphabet'] = alphabetstring
    
    tapestring = machineSpecs.find('initialtape').text.replace(blank, '_')
    globvars.AllItems['tape'].load_tape(tapestring)
    
    states = {}
    transitions = []
    
    for xmlstate in machineSpecs.find('states'):
        try:
            name = xmlstate.attrib['name']
        except:
            name = None
            
        try:
            x = xmlstate.attrib['x']
            y = xmlstate.attrib['y']
            if statefuncs.collide_state(x, y):
                x, y = nextposition()
        except:
            x, y = nextposition()
            
        state = create_state(x = x, y = y, name = name)
        name = state.name
        states[name] = state
        
        for xmltran in xmlstate:
            xmltran.attrib['oldstate'] = name
            transitions.append(xmltran)
            
    states[machineSpecs.find('initialstate').attrib['name']].set_start_state()
    
    for xmlstate in machineSpecs.find('finalstates'):
        states[xmlstate.attrib['name']].final_state(True)
    
    for xmltran in transitions:
        read = xmltran.attrib['seensym'].replace(blank, '_')
        write = xmltran.attrib['writesym'].replace(blank, '_')
        move = xmltran.attrib['move'].upper()
        if (read in alphabetstring) and (write in alphabetstring) and (move in "LR"):
            info = read + "/" + write + "/" + move
            try:
                x = xmltran.attrib['x']
                y = xmltran.attrib['y']
            except:
                x, y = None, None
            
            try:
                startstate = states[xmltran.attrib['oldstate']]
                endstate = states[xmltran.attrib['newstate']]
                create_transition(startstate = startstate, endstate = endstate, info = info, x = x, y = y)
            except:
                #log failure
                pass
        else:
            #log failure
            pass
            
    undo.clear_undo()
    globvars.AllItems['stateMachine'].centre_machine()
    globvars.AllItems['move'].on_press()
        
def nextposition():
    machine = globvars.AllItems['stateMachine']
    x, y = machine.x + machine.width / 2, machine.y + machine.height / 2
    dx, dy = 0, 100
    count, iter = 1, 1
    while statefuncs.collide_state(x, y):
        x += dx
        y += dy
        iter -= 1
        if iter == 0:
            dx, dy = dy, -dx
            if dx == 0:
                count += 1
            iter = count
    #log that position has been changed
    return x, y
            