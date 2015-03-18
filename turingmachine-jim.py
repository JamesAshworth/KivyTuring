# Name: Jim Ashworth
# ID: 26164035

# If the last line (main()) is uncommented, when run from the command prompt, 
# the script will request a file to process.
# If the provided file does not exist, the script will keep asking.
# The given XML file is then parsed by xml.etree.ElementTree.parse.
# If at any point an error is thrown (due to a non-xml file being provided,
# or an incorrect format of xml file), the simulation fails gracefully with a
# message to please try again.
# The object from parsing is then further deconstructed into more basic python
# constructs, to make the code more legible and maintainable.
# States and transitions are packaged into objects with easier access methods,
# and a logging object is created to output the final result.
# The simulation then runs (as documented within the code) and the log file
# then produces the final trace file. The user is informed, and the process exits.

import xml.etree.ElementTree as ET
from copy import copy
from os.path import isfile

class logging:
    def __init__(self, filename, state, tape, prints=True, writes=True):
        # Properties
        self.prints = prints
        self.writes = writes
        self.steps = 0
        if writes:
            self.fname = filename.replace('.xml', '.txt')
            self.f = open(self.fname, 'w')
        self.log(state, tape, 0)

    def log(self, state, tape, position):
        # Don't affect the original
        tape = copy(tape)
        # Highlight the current position
        tape.insert(position + 1, '*')
        tape.insert(position, '*')

        if self.steps == 0:
            # Header with initial states
            self.printWrite('initial state = ' + str(state)             )
            self.printWrite('initial tape  = ' + ''.join(map(str, tape)))
            self.printWrite('')
        else:
            # Info for each step
            self.printWrite('steps = ' + str(self.steps)        )
            self.printWrite('state = ' + str(state)             )
            self.printWrite('tape  = ' + ''.join(map(str, tape)))
            self.printWrite('')

        # Next step
        self.steps = self.steps + 1

    def printWrite(self, text):
        if self.prints:
            print(text)
        if self.writes:
            self.f.write(text + '\n')

    def complete(self, final):
        # The final result of the simulation
        if final:
            self.printWrite('halted with answer yes')
        else:
            self.printWrite('halted with answer no')

        if self.writes:
            # Close the file, and clear the handle
            self.f.close()
            self.f = None
            print('Simulation complete - trace created in ' + self.fname)
        else:
            print('Simulation complete')

# Class for transitions, just to allow for easier access and extensibility
class turingTransition:
    def __init__(self, read, write, next, move):
        # Properties
        self.read = read
        # Allow for blank write (write what was read - same thing)
        if write == '':
            self.write = read
        else:
            self.write = write
        self.next = next
        self.move = move

# Class for states, to allow for easier access and methods
class turingState:
    def __init__(self, XMLobject, final=False):
        # Properties
        self.final = final
        self.transitions = []
        # Parse the transitions into their respective objects
        self.processTransitions(XMLobject)

    def processTransitions(self, XMLobject):
        # For each transition from the XML, make a new object and add it
        for t in XMLobject:
            self.addTransition(t.attrib['seensym'], t.attrib['writesym'], t.attrib['newstate'], t.attrib['move'])

    def addTransition(self, read, write, next, move):
        # Append the new transition object to the list
        self.transitions.append(turingTransition(read, write, next, move))

    def getTransition(self, read):
        # Find a transition from this state for the current symbol
        for transition in self.transitions:
            if transition.read == read:
                return transition
        # If there is no transition, explicitly return None (which we can change later if needs be)
        return None


def run_turing(filename):
    # Parse the XML file into an object
    machineSpecs = ET.parse(filename).getroot()
    # Create the start parameters
    position = 0
    states = {}
    # Get the alphabet (currently just for interest)
    alphabet = list(machineSpecs.find('alphabet').text)
    # Get the tape, and turn it into a navigable list rather than a string
    tape = list(machineSpecs.find('initialtape').text)
    # Get the blank character for padding the tape when we go past the end
    blank = machineSpecs.find('blank').attrib['char']
    # Find the first state
    initialState = machineSpecs.find('initialstate').attrib['name']
    # Package states into objects in a dictionary by name
    for s in machineSpecs.find('states'):
        states[s.attrib['name']] = turingState(s)
    # Mark each final state
    for f in machineSpecs.find('finalstates'):
        states[f.attrib['name']].final = True

    # Set up the log file
    log = logging(filename, initialState, tape)

    # Set up for the loop
    currState = states[initialState]
    currSym = tape[position]

    t = currState.getTransition(currSym)


    # While there is a valid transition
    while t:
        # Write the new symbol
        tape[position] = t.write
        # Get the new state
        currState = states[t.next]
        # Move (and pad if needs be) (allows for no movement, in case it's ever relevant)
        if t.move == 'L':
            position -= 1
            if position < 0:
                position = 0
                tape.insert(0, blank)
        if t.move == 'R':
            position += 1
            if position == len(tape):
                tape.append(blank)
        # Get the new symbol
        currSym = tape[position]
        # Log which state and position we've moved to, and any changes made to the tape
        log.log(t.next, tape, position)
        # Get the transition for this symbol in this state (if there is one)
        t = currState.getTransition(currSym)

    # Loop complete - simulation over. Tell the logging object to spit out the trace, and tell the user.
    log.complete(currState.final)

def main():
    # Ask for a filename
    filename = raw_input('Please enter filename for the Turing Machine to process:\n>>> ')
    
    # No really, ask for a filename
    while not isfile(filename):
        filename = raw_input(filename + ' does not exist - please enter another filename:\n>>> ')
    
    # Try, just in case the wrong file was input to avoid an ugly failure
    try:
        run_turing(filename)
    except:
        print('Simulation has failed - please try again\n')
        
# main()