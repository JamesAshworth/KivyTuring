from threading import *
from popups import CommonPopup, InfoBox
from kivy.uix.progressbar import ProgressBar
import statefuncs
import globvars
import logic

class ProgressPopup(CommonPopup):
    def __init__(self, thread, *args, **kwargs):
        super(ProgressPopup, self).__init__(*args, **kwargs)
        self.thread = thread
        self.title = "State Machine Running..."
        self.progress = ProgressBar()
        self.content.add_widget(self.progress)
        self.content.add_widget(self.message)
        self.content.add_widget(self.buttonholder)
        self.buttonholder.remove_widget(self.button)
        
    def on_cancel(self, instance):
        self.thread.running = False
        self.dismiss()

class LogicThread(Thread):
    def __init__(self, *args, **kwargs):
        super(LogicThread, self).__init__(*args, **kwargs)
        globvars.AllItems['logicThread'] = self
        self.running = True
        self.states = {}
        self.tape = []
        self.position = 0
        self.steps = 0
        self.zero = 0
        self.state = ""
        self.symbol = ""
        self.progress = ProgressPopup(thread = self)
        
    def load_machine(self):
        for state in globvars.AllItems['states']:
            sname = state.name
            if state.start:
                self.state = sname
            self.states[sname] = {}
            if state.final:
                self.states[sname]['final'] = True
            else:
                self.states[sname]['final'] = False
            for transition in state.transitions:
                if (transition.startstate == state):
                    tread = transition.read_value()
                    self.states[sname][tread] = {}
                    self.states[sname][tread]['wr'] = transition.write_value()
                    self.states[sname][tread]['mv'] = transition.move_value()
                    self.states[sname][tread]['to'] = transition.endstate.name
        
        self.tape = globvars.AllItems['tape'].get_tape()
        self.position = (- globvars.AllItems['tape'].labels[0])
        self.symbol = self.tape[self.position]
        self.zero = self.position
        
    def run(self):
        logic.reset_simulation()
        self.load_machine()
        self.progress.open()
        while self.running:
            self.do_run()
    
    def do_run(self):
        self.steps += 1
        if not (self.steps % 1000):
            self.progress.progress.value = (self.progress.progress.value + 1) % 100
            self.progress.message.text = str(self.steps)
        try:
            self.tape[self.position] = self.states[self.state][self.symbol]['wr']
            self.position += self.states[self.state][self.symbol]['mv']
            self.state = self.states[self.state][self.symbol]['to']
            if self.position < 0:
                self.position += 1
                self.zero += 1
                self.tape.insert(0, '_')
            if self.position == len(self.tape):
                self.tape.append('_')
            self.symbol = self.tape[self.position]
        except KeyError:
            self.progress.dismiss()
            if self.states[self.state]['final']:
                InfoBox(title="Complete", message=("Simulation halted with answer 'Yes' in " + str(self.steps - 1) + " steps")).open()
            else:
                InfoBox(title="Complete", message=("Simulation halted with answer 'No' in " + str(self.steps - 1) + " steps")).open()
            self.running = False
"""         tapestring = ""
            self.position -= self.zero
            for symbol in self.tape:
                if not self.zero:
                    tapestring += "*"
                tapestring += symbol
                self.zero -= 1
            globvars.AllItems['tape'].load_tape(tapestring)
            globvars.AllItems['tape'].select_cell(self.position)
            for state in globvars.AllItems['states']:
                state.highlighted(False)
                if state.name == self.state:
                    state.highlighted(True)
                    state.move_to_centre()"""