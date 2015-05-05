import xml.etree.ElementTree as ET
import statefuncs
import globvars

# cribbed from: http://effbot.org/zone/element-lib.htm#prettyprint
# via: http://stackoverflow.com/a/4590052
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def save_machine(filename):
    root = ET.Element('turingmachine')
    
    alphabet = ET.SubElement(root, 'alphabet')
    initialtape = ET.SubElement(root, 'initialtape')
    blank = ET.SubElement(root, 'blank')
    initialstate = ET.SubElement(root, 'initialstate')
    finalstates = ET.SubElement(root, 'finalstates')
    states = ET.SubElement(root, 'states')
    
    alphabet.text = globvars.AllItems['alphabet']
    
    initialtape.text = ''.join(map(str, globvars.AllItems['tape'].get_tape()))
    
    blank.set('char', '_')
    
    if statefuncs.find_start_state() != None:
        initialstate.set('name', str(statefuncs.find_start_state().name))
        
    for state in globvars.AllItems['states']:
        if state.final:
            ET.SubElement(finalstates, 'finalstate').set('name', str(state.name))
            
        xmlstate = ET.SubElement(states, 'state')
        xmlstate.set('name', str(state.name))
        xmlstate.set('x', str(state.center_x))
        xmlstate.set('y', str(state.center_y))
        
        for transition in state.transitions:
            if transition.startstate == state:
                xmltransition = ET.SubElement(xmlstate, 'transition')
                xmltransition.set('seensym', str(transition.read_value()))
                xmltransition.set('writesym', str(transition.write_value()))
                xmltransition.set('newstate', str(transition.endstate.name))
                xmltransition.set('move', str(transition.move_symbol()))
                xmltransition.set('x', str(transition.midpoint.x + globvars.AllItems['gs'] / 2))
                xmltransition.set('y', str(transition.midpoint.y + globvars.AllItems['gs'] / 2))
                
    indent(root)
    tree = ET.ElementTree(root)
    tree.write(filename)