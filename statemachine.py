from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Ellipse, Rectangle, Line, Triangle
from kivy.uix.label import Label
from kivy.uix.scatterlayout import ScatterLayout
from kivy.clock import Clock
from math import sqrt, degrees, atan2
from sys import maxint
from popups import StateNamer, TransitionIdentifier, AlphabetEntry, ErrorBox
import globvars
import statefuncs
import transitionfuncs
import logic
from undo import *

def create_state(x, y, name = None):
    state = State(pos = (x - 25, y - 25))
    globvars.AllItems['stateMachine'].add_widget(state)
    globvars.AllItems['states'].append(state)
    if name is not None:
        state.set_text(name)
    return state
        
def create_transition(startstate, endstate, info, x, y):
    t = Transition()
    t.startstate = startstate
    t.endstate = endstate
    t.finish_transition()
    t.set_info(info)
    if not((x is None) or (y is None)):
        t.update_midpoint_pos(x, y)
    return t

class StateLabel(Label):
    pass
    
class RotateLabel(Label):
    pass
    
class TransitionInfo(ScatterLayout):
    def __init__(self, *args, **kwargs):
        super(TransitionInfo, self).__init__(*args, **kwargs)
        self.label = RotateLabel()
        self.add_widget(self.label)
        
    def update_info(self, text):
        text += "\n\n"
        if self.label.text != "":
            if self.label.text != text:
                UndoTransitionInfo(self, self.label.text)
            self.label.text = text
        else:
            self.label.text = text
            
    def set_rotation(self, angle):
        if angle == 180 or angle == -180:
            angle = 0
            self.label.text = "\n\n" + self.label.text.replace("\n", "")
        else:
            self.label.text = self.label.text.replace("\n", "") + "\n\n"
        self.rotation = angle

class TransitionGrabber(Widget):
    def update(self):
        gs = globvars.AllItems['gs']
        self.canvas.clear()
        self.canvas.add(Color(0, 1, 0))
        self.canvas.add(Rectangle(size = (gs / 2, gs / 2), pos = (self.x + gs / 4, self.y + gs / 4)))

class Transition(Widget):
    def __init__(self, *args, **kwargs):
        super(Transition, self).__init__(*args, **kwargs)
        gs = globvars.AllItems['gs']
        self.startpoint = None
        self.startstate = None
        self.midpoint   = TransitionGrabber()
        self.info       = TransitionInfo(size = (60, 60), size_hint = (None, None))
        self.endpoint   = None
        self.endstate   = None
        self.display    = True
        self.complete   = False
        self.alongline  = 0
        self.linecolour = Color(0, 0, 0)
        
    def on_touch_down(self, touch):
        if touch.ud['mode'] == "create_t":
            touch.ud['transitionPos'] = [self.midpoint.x, self.midpoint.y]
            if touch.is_double_tap:
                self.edit_info(read = self.read_value(), write = self.write_value(), move = self.move_symbol())
        elif touch.ud['mode'] == "delete":
            UndoTransitionDelete(self)
            self.destroy_self()
        else:
            return False
        return True
        
    def on_touch_move(self, touch):
        if touch.ud['touched'] != self:
            return False
        if touch.ud['mode'] != "create_t":
            return True
        gs = globvars.AllItems['gs']
        if self.complete:
            self.midpoint.pos = [touch.x - gs / 2, touch.y - gs / 2]
        else:
            self.endpoint = [touch.x, touch.y]
            self.midpoint.pos = [(self.startpoint[0] + touch.x - gs) / 2, (self.startpoint[1] + touch.y - gs) / 2]
        self.update()
        return True
        
    def on_touch_up(self, touch):
        if self.complete:
            if touch.ud['mode'] == "create_t":
                if touch.ud['transitionPos'] == [self.midpoint.x, self.midpoint.y]:
                    return True
                UndoTransitionMove(self, self.midpoint.x - touch.ud['transitionPos'][0], self.midpoint.y - touch.ud['transitionPos'][1])
            return True
        self.unfinished_on_touch_up(touch)
        
    def unfinished_on_touch_up(self, touch):
        self.startstate.highlighted(False)
        globvars.AllItems['stateMachine'].remove_widget(self)
        globvars.AllItems['stateMachine'].remove_widget(self.midpoint)
        if not statefuncs.identify_state_in(touch):
            return True
        self.endstate = touch.ud['touched']
        self.edit_info()
        
    def unfinished_on_touch_up_after_name(self):
        UndoTransitionCreate(self)
        self.finish_transition()
            
    def finish_transition(self, resetMidpoint = True):
        if resetMidpoint:
            gs = globvars.AllItems['gs']
            self.complete = True
            self.startpoint = [self.startstate.center_x, self.startstate.center_y]
            self.endpoint = [self.endstate.center_x, self.endstate.center_y]
            self.midpoint.pos = [(self.startpoint[0] + self.endpoint[0] - gs) / 2, (self.startpoint[1] + self.endpoint[1] - gs) / 2]
            if self.startstate == self.endstate:
                self.midpoint.y += 100
        self.startstate.transitions.append(self)
        self.endstate.transitions.append(self)
        globvars.AllItems['stateMachine'].add_widget(self.midpoint)
        globvars.AllItems['stateMachine'].add_widget(self.info)
        globvars.AllItems['stateMachine'].add_widget(self)
        globvars.AllItems['transitions'].append(self)
        self.update()
        globvars.AllItems['stateMachine'].states_to_front()
        
    def edit_info(self, read = "", write = "", move = ""):
        TransitionIdentifier(object = self, read = read, write = write, move = move).open()
        
    def set_info(self, text):
        self.info.update_info(text)
        
    def set_initial_info(self, text):
        self.set_info(text)
        if not self.complete:
            self.unfinished_on_touch_up_after_name()
        
    def read_value(self):
        return self.info.label.text.replace("\n", "")[0]
        
    def write_value(self):
        return self.info.label.text.replace("\n", "")[2]
        
    def move_symbol(self):
        return self.info.label.text.replace("\n", "")[4]
    
    def move_value(self):
        if self.move_symbol() == "L":
            return -1
        if self.move_symbol() == "R":
            return 1
        return 0
        
    def line_middle(self):
        return self.find_point_on_line(0.5)
        
    def direction_triangle(self):
        gs = globvars.AllItems['gs']
        fpoint = self.line_middle()
        if self.startstate == self.endstate:
            dx = fpoint[1] - self.startpoint[1] 
            dy = self.startpoint[0] - fpoint[0]
        else:
            dx = self.endpoint[0] - self.startpoint[0]
            dy = self.endpoint[1] - self.startpoint[1]
        length = sqrt((dx ** 2) + (dy ** 2))
        if not length:
            length = 1
        dx *= 10 / length
        dy *= 10 / length
        bpoint1 = list(fpoint)
        fpoint[0] += dx
        fpoint[1] += dy
        bpoint1[0] -= dx
        bpoint1[1] -= dy
        bpoint2 = list(bpoint1)
        bpoint1[0] -= dy
        bpoint1[1] += dx
        bpoint2[0] += dy
        bpoint2[1] -= dx
        return fpoint + bpoint1 + bpoint2
        
    def move_along_line(self):
        globvars.AllItems['movementClock'] = self.do_move_along_line
        self.linecolour = Color(0.5, 0.5, 0)
        self.update()
        Clock.schedule_interval(self.do_move_along_line, 0.05)
        
    def find_point_on_line(self, a):
        p = self.midpoints_calc()
        z = (1 - a)
        if len(p) == 2:
            x = self.startpoint[0] * (z ** 2) + p[0] * z * a * 2 + self.endpoint[0] * (a ** 2)
            y = self.startpoint[1] * (z ** 2) + p[1] * z * a * 2 + self.endpoint[1] * (a ** 2)
        else:
            x = self.startpoint[0] * (z ** 4) + p[0] * 4 * (z ** 3) * a + p[2] * 6 * (z ** 2) * (a ** 2) + p[4] * 4 * z * (a ** 3) + self.endpoint[0] * (a ** 4)
            y = self.startpoint[1] * (z ** 4) + p[1] * 4 * (z ** 3) * a + p[3] * 6 * (z ** 2) * (a ** 2) + p[5] * 4 * z * (a ** 3) + self.endpoint[1] * (a ** 4)
        return [x, y]
        
    def do_move_along_line(self, instance):
        old = self.find_point_on_line(self.alongline)
        self.alongline += globvars.AllItems['animationStep']
        if self.alongline > 1:
            self.alongline = 1
        new = self.find_point_on_line(self.alongline)
        statefuncs.move_all(old[0] - new[0], old[1] - new[1])
        if self.alongline >= 0.25:
            self.startstate.highlighted(False)
        if self.alongline >= 0.75:
            self.endstate.highlighted(True)
        if self.alongline < 1:
            return True
        self.alongline = 0
        self.linecolour = Color(0, 0, 0)
        self.update()
        globvars.AllItems['inStep'] = False
        logic.do_run()
        return False
        
    def rotation_angle(self):
        points = self.direction_triangle()
        points[2] += points[4]
        points[3] += points[5]
        points[2] /= 2
        points[3] /= 2
        dx = points[0] - points[2]
        dy = points[1] - points[3]
        return ((degrees(atan2(dy, dx)) + 45) // 90 * 90)
        
    def update(self):
        pd = globvars.AllItems['linethickness']
        self.canvas.clear()
        self.canvas.add(self.linecolour)
        self.canvas.add(Line(bezier = self.startpoint + self.midpoints_calc() + self.endpoint, width = pd))
        centre = self.line_middle()
        self.canvas.add(Triangle(center = (centre[0] - 10, centre[1] - 10), points = self.direction_triangle()))
        self.info.pos = (centre[0] - 30, centre[1] - 30)
        self.info.set_rotation(self.rotation_angle())
        globvars.AllItems['stateMachine'].remove_widget(self.midpoint)
        if self.display:
            self.midpoint.update()
            globvars.AllItems['stateMachine'].add_widget(self.midpoint)
            
    def midpoints_calc(self):
        gs = globvars.AllItems['gs']
        midpoints = [self.midpoint.x + (gs / 2), self.midpoint.y + (gs / 2)]
        if self.startstate != self.endstate:
            return midpoints
        dx = (self.midpoint.x - self.startstate.center_x + (gs / 2)) / 2
        dy = (self.midpoint.y - self.startstate.center_y + (gs / 2)) / 2
        midpoint1 = [self.startstate.center_x + dx - dy, self.startstate.center_y + dy + dx]
        midpoint2 = [self.startstate.center_x + dx + dy, self.startstate.center_y + dy - dx]
        return midpoint1 + midpoints + midpoint2
        
    def display_mover(self, display):
        self.display = display
        self.update()
        
    def update_midpoint_pos(self, x, y):  
        self.midpoint.x = x
        self.midpoint.y = y
        self.update()
        
    def update_point(self, state, point):
        diff = [0, 0]
        if self.startstate == state:
            diff[0] += (point[0] - self.startpoint[0]) / 2
            diff[1] += (point[1] - self.startpoint[1]) / 2
            self.startpoint = point
        if self.endstate == state:
            diff[0] += (point[0] - self.endpoint[0]) / 2
            diff[1] += (point[1] - self.endpoint[1]) / 2
            self.endpoint = point
        self.update_midpoint_pos(self.midpoint.x + diff[0], self.midpoint.y + diff[1])
        
    def destroy_self(self):
        self.startstate.transitions.remove(self)
        self.endstate.transitions.remove(self)
        globvars.AllItems['stateMachine'].remove_widget(self.midpoint)
        globvars.AllItems['stateMachine'].remove_widget(self.info)
        globvars.AllItems['stateMachine'].remove_widget(self)
        globvars.AllItems['transitions'].remove(self)

    def check_touch(self, touch):
        gs = globvars.AllItems['gs']
        if touch.x < self.midpoint.x:
            return False
        if touch.x >= self.midpoint.x + gs:
            return False
        if touch.y < self.midpoint.y:
            return False
        if touch.y >= self.midpoint.y + gs:
            return False
        touch.ud['touched'] = self
        return True

class State(Widget):
    def __init__(self, *args, **kwargs):
        super(State, self).__init__(*args, **kwargs)
        self.size_hint = None, None
        self.size = 50, 50
        self.colours = [Color(1, 1, 1, 0), Color(0, 0, 0), Color(1, 1, 1), Color(1, 1, 1), Color(1, 1, 1)]
        self.final = False
        self.start = False
        self.transitions = []
        self.name = ""
        self.label = StateLabel(pos = self.pos, size = self.size)
        self.default_name()
        self.state_update()

    def check_touch(self, touch):
        if self.collide_point(touch.x, touch.y):
            touch.ud['touched'] = self
            return True
        return False
        
    def on_touch_down(self, touch):
        if touch.ud['mode'] == "final":
            self.final_state_toggle(undoPossible = True)
        if touch.ud['mode'] == "start":
            self.set_start_state(undoPossible = True)
        if touch.ud['mode'] == "delete":
            self.destroy_self()
        if touch.ud['mode'] == "create_t":
            globvars.AllItems['stateMachine'].make_transition(touch)
        if touch.ud['mode'] == "create_s":
            touch.ud['statePos'] = [self.x, self.y]
            if touch.is_double_tap:
                touch.ud['touched'].edit_name()
        return True
        
    def on_touch_move(self, touch):
        if touch.ud['mode'] != "create_s":
            return True
        for state in globvars.AllItems['states']:
            if state == self:
                pass
            elif state.collide_state(touch.x, touch.y):
                return True
        self.center = (touch.x, touch.y)
        self.state_update()
        return True
        
    def on_touch_up(self, touch):
        if touch.ud['mode'] != "create_s":
            return True
        if touch.ud['statePos'] == [self.x, self.y]:
            return True
        UndoStateMove(self, self.x - touch.ud['statePos'][0], self.y - touch.ud['statePos'][1])
        
    def edit_name(self):
        StateNamer(object = self, text = self.name).open()
        
    def default_name(self):
        i = 0
        while statefuncs.state_named(str(i)):
            i += 1
        self.set_text(text = str(i), undoPossible = False)
        
    def state_update(self):
        for t in self.transitions:
            t.update_point(self, [self.center_x, self.center_y])
        pd = 2
        self.remove_widget(self.label)
        self.canvas.clear()
        for i in range(5):
            self.canvas.add(self.colours[i])
            self.canvas.add(Ellipse(pos = (self.x + i * pd, self.y + i * pd), size = (self.width - 2 * i * pd, self.height - 2 * i * pd)))
        self.label.pos = self.pos
        self.add_widget(self.label)
        
    def highlighted(self, highlighted):
        if highlighted:
            self.colours[0] = Color(1, 1, 0)
        else:
            self.colours[0] = Color(1, 1, 1, 0)
        self.state_update()
        
    def set_text(self, text, undoPossible = True):
        if text != self.name:
            if undoPossible:
                UndoStateName(self, self.name)
        self.name = text
        self.label.text = text
        
    def final_state_toggle(self, undoPossible = False):
        if undoPossible:
            UndoStateFinal(self)
        self.final_state(not self.final)
        
    def final_state(self, final):
        self.final = final
        if final:
            self.colours[3] = Color(0, 0, 0)
        elif self.start:
            self.colours[3] = Color(1, 0.5, 0.5)
        else:
            self.colours[3] = Color(1, 1, 1)
        self.state_update()
        
    def start_state(self, start):
        self.start = start
        if start:
            self.colours[2] = Color(1, 0.5, 0.5)
            self.colours[4] = Color(1, 0.5, 0.5)
        else:
            self.colours[2] = Color(1, 1, 1)
            self.colours[4] = Color(1, 1, 1)
        self.final_state(self.final)
        
    def set_start_state(self, undoPossible = False):
        if not self.start:
            if undoPossible:
                UndoStateStart(statefuncs.find_start_state(), self)
        statefuncs.remove_start_state()
        self.start_state(True)
        
    def distance_centre(self, x, y):
        dx = self.center_x - x
        dy = self.center_y - y
        return sqrt((dx ** 2) + (dy ** 2))
        
    def collide_point(self, x, y):
        if self.distance_centre(x, y) <= (self.height / 2):
            return True
        return False
        
    def collide_state(self, x, y):
        if self.distance_centre(x, y) <= self.height:
            return True
        return False
        
    def move(self, dx, dy):
        self.pos = (self.x + dx, self.y + dy)
        self.state_update()
        
    def move_to_centre(self):
        dx = globvars.AllItems['stateMachine'].center_x - self.center_x
        dy = globvars.AllItems['stateMachine'].center_y - self.center_y
        statefuncs.move_all(dx, dy)
            
    def destroy_self(self):
        UndoStateDeleteStop()
        while len(self.transitions):
            t = self.transitions[0]
            UndoTransitionDelete(t)
            t.destroy_self()
        globvars.AllItems['stateMachine'].remove_widget(self)
        index = globvars.AllItems['states'].index(self)
        globvars.AllItems['states'].remove(self)
        if self.start:
            if len(globvars.AllItems['states']):
                globvars.AllItems['states'][0].set_start_state(undoPossible = True)
        UndoStateDeleteStart(self, index)

class _StateMachine(FloatLayout):
    def __init__(self, *args, **kwargs):
        super(_StateMachine, self).__init__(*args, **kwargs)
        self.mode = "move"
        self.outofbounds = True
        globvars.AllItems['stateMachine'] = self
    
    def on_touch_down(self, touch):
        self.outofbounds = False
        
        if not self.collide_point(touch.x, touch.y):
            self.outofbounds = True
            return
            
        if (touch.is_double_tap and self.mode == "move"):
            self.centre_machine()
            
        touch.ud['last'] = [touch.x, touch.y]
        touch.ud['mode'] = self.mode
            
        if transitionfuncs.handled_by_transition(touch):
            return
        
        if statefuncs.handled_by_state(touch):
            return
        
        touch.ud['touched'] = self
                
        if self.mode == "create_s":
            start = (len(globvars.AllItems['states']) == 0)
            state = create_state(touch.x, touch.y)
            state.start_state(start)
            if state is not None:
                touch.ud['touched'] = state
                touch.ud['statePos'] = [state.x, state.y]
                UndoStateCreate(state)
            
    def move_all_touch(self, touch):
        statefuncs.move_all(touch.x - touch.ud['last'][0], touch.y - touch.ud['last'][1])
        touch.ud['last'] = [touch.x, touch.y]
        
    def check_mode(self, mode):
        if mode == "run":
            if not len(globvars.AllItems['states']):
                ErrorBox("Cannot run with no states").open()
                return False
            logic.begin_simulation()
        return True
            
    def set_mode(self, mode):
        if not self.check_mode(mode):
            return False
        self.mode = mode
        display = (mode in globvars.AllItems['moverDisplayModes'])
        transitionfuncs.display_mover(display)
        return True
        
    def make_transition(self, touch):
        touch.ud['touched'].highlighted(True)
        t = Transition()
        t.startpoint = [touch.ud['touched'].center_x, touch.ud['touched'].center_y]
        t.startstate = touch.ud['touched']
        touch.ud['touched'] = t
        self.add_widget(t)
        
    def states_to_front(self):
        statefuncs.states_to_front()
        if self.mode in globvars.AllItems['moverDisplayModes']:
            transitionfuncs.movers_to_front()
        
    def on_touch_move(self, touch):
        if self.outofbounds:
            return False
        if touch.ud['touched'] != self:
            return touch.ud['touched'].on_touch_move(touch)
        if self.mode == "move":
            self.move_all_touch(touch)
            
    def on_touch_up(self, touch):
        if self.outofbounds:
            return False
        if not 'touched' in touch.ud:
            return False
        if touch.ud['touched'] != self:
            return touch.ud['touched'].on_touch_up(touch)
        return True
    
    def centre_machine(self):
        maxx, maxy, minx, miny = -maxint, -maxint, maxint, maxint
        for state in globvars.AllItems['states']:
            maxx = max(maxx, state.center_x)
            maxy = max(maxy, state.center_y)
            minx = min(minx, state.center_x)
            miny = min(miny, state.center_y)
        avgx = (maxx + minx) / 2
        avgy = (maxy + miny) / 2
        statefuncs.move_all(self.center_x - avgx, self.center_y - avgy)
        
    def clear_machine(self):
        self.clear_widgets()
        globvars.AllItems['states'] = []
        globvars.AllItems['transitions'] = []
        
    def define_alphabet(self):
        AlphabetEntry().open()
        
class StateMachine(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(StateMachine, self).__init__(*args, **kwargs)
        screen = Screen()
        screen.add_widget(_StateMachine())
        self.add_widget(screen)