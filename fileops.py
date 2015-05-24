from popups import FileChooser, FileNamer, FileOverwriter, InfoBox
from glob import glob
import os
import os.path
import filecmp
import loadmachine
import savemachine
import globvars

def check_overwrite(callback):
    filenames = glob('*.xml~')
    if (len(filenames)):
        if not filecmp.cmp(filenames[0], filenames[0][:-1]):
            FileOverwriter(filenames[0], delete_file, callback).open()
            return
        else:
            delete_file(filenames[0])
    callback()
    
def import_file(filename = '', overwrite = True):
    pass

def load_file(filename = '', overwrite = True):
    if not overwrite:
        check_overwrite(load_file)
        return
    if filename == '':
        FileChooser(load_file).open()
        return
    globvars.AllItems['undoDisabled'] = True
    complete = loadmachine.load_machine(filename)
    globvars.AllItems['undoDisabled'] = False
    if complete:
        move_to_machine()

def delete_file(filename = '', silentDeletion = True):
    if filename == '':
        FileChooser(delete_file, confirmDelete = True).open()
        return
    os.remove(filename)
    if os.path.isfile(filename + '~'):
        os.remove(filename + '~')
    if not silentDeletion:
        InfoBox(title="Delete Complete", message=filename + " deleted successfully").open()
    globvars.AllItems['refreshLabel']()
    
def new_file(filename = '', overwrite = True):
    if not overwrite:
        check_overwrite(new_file)
        return
    if filename == '':
        FileNamer(new_file).open()
        return
    globvars.AllItems['stateMachine'].clear_machine()
    globvars.AllItems['alphabet'] = "_01"
    globvars.AllItems['stateMachine'].define_alphabet()
    globvars.AllItems['saveFile'] = filename
    savemachine.save_machine(auto = False)
    move_to_machine()
    
def move_to_machine():
    globvars.AllItems['application'].transition.direction = 'left'
    globvars.AllItems['application'].current = 'machine'