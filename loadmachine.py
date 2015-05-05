from statemachine import create_state, create_transition
from xml.etree.ElementTree import parse as xmlparse
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from popups import InfoBox
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
        globvars.AllItems['undoDisabled'] = True
        try:
            load_machine(selection[0])
            #switch screen
        except ValueError as err:
            globvars.AllItems['stateMachine'].clear_machine()
            InfoBox(title="Load Failed", message=err.args[0]).open()
        globvars.AllItems['undoDisabled'] = False
        self.dismiss()

def load_machine(filename):
    globvars.AllItems['stateMachine'].clear_machine()
    machineSpecs = xmlparse(filename).getroot()
    
    try:
        blank = machineSpecs.find('blank').attrib['char']
    except:
        raise ValueError('No blank character specified')
    
    try:
        alphabetstring = machineSpecs.find('alphabet').text.replace(blank, '_')
    except:
        raise ValueError('No alphabet specified')
    globvars.AllItems['alphabet'] = alphabetstring
    
    try:
        tapestring = machineSpecs.find('initialtape').text.replace(blank, '_')
    except:
        raise ValueError('No initialtape specified')
    globvars.AllItems['tape'].load_tape(tapestring)
    
    states = {}
    transitions = []
    
    try:
        xmlstatelist = machineSpecs.find('states')
    except:
        raise ValueError('No states list specified')
    
    for xmlstate in xmlstatelist:
        try:
            name = xmlstate.attrib['name']
        except:
            name = None
            
        try:
            x = float(xmlstate.attrib['x'])
            y = float(xmlstate.attrib['y'])
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
            
    if len(states):
        try:
            states[machineSpecs.find('initialstate').attrib['name']].set_start_state()
        except:
            raise ValueError('No initialstate specified')
        
    try:
        xmlfinalstateslist = machineSpecs.find('finalstates')
    except:
        raise ValueError('No final states list specified')
    
    for xmlstate in xmlfinalstateslist:
        states[xmlstate.attrib['name']].final_state(True)
    
    for xmltran in transitions:
        try:
            read = xmltran.attrib['seensym'].replace(blank, '_')
            write = xmltran.attrib['writesym'].replace(blank, '_')
            move = xmltran.attrib['move'].upper()
            if (read in alphabetstring) and (write in alphabetstring) and (move in "LR"):
                info = read + "/" + write + "/" + move
                try:
                    x = float(xmltran.attrib['x']) - globvars.AllItems['gs'] / 2
                    y = float(xmltran.attrib['y']) - globvars.AllItems['gs'] / 2
                except:
                    x, y = None, None
            
                startstate = states[xmltran.attrib['oldstate']]
                endstate = states[xmltran.attrib['newstate']]
                create_transition(startstate = startstate, endstate = endstate, info = info, x = x, y = y)
            else:
                raise ValueError()
        except:
            raise ValueError('Invalid transition')
            
    undo.clear_undo()
    globvars.AllItems['stateMachine'].centre_machine()
    globvars.AllItems['move'].on_press()
    globvars.AllItems['saveFile'] = filename.replace('.xml~', '.xml')
        
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
            