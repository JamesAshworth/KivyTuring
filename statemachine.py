from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Ellipse, Rectangle, Line
from math import sqrt
from sys import maxint
import globvars

class TransitionGrabber(Widget):
    def update(self):
        gs = globvars.AllItems['gs']
        self.canvas.clear()
        self.canvas.add(Color(0, 1, 0))
        self.canvas.add(Rectangle(size = (gs, gs), pos = self.pos))

class Transition(Widget):
    def __init__(self, *args, **kwargs):
        super(Transition, self).__init__(*args, **kwargs)
        gs = globvars.AllItems['gs']
        self.startpoint = None
        self.startstate = None
        self.midpoint   = TransitionGrabber(size = (gs, gs))
        self.endpoint   = None
        self.endstate   = None
        self.display    = True
        self.complete   = False
        
    def update(self):
        pd = globvars.AllItems['linethickness']
        gs = globvars.AllItems['gs']
        self.canvas.clear()
        self.canvas.add(Color(0, 0, 0))
        self.canvas.add(Line(bezier = self.startpoint + [self.midpoint.x + (gs / 2), self.midpoint.y + (gs / 2)] + self.endpoint, width = pd))
        globvars.AllItems['stateMachine'].remove_widget(self.midpoint)
        if self.display:
            self.midpoint.update()
            globvars.AllItems['stateMachine'].add_widget(self.midpoint)
        
    def display_mover(self, display):
        self.display = display
        self.update()
        
    def extend_line(self, touch):
        gs = globvars.AllItems['gs']
        if self.complete:
            self.midpoint.pos = [touch.x - gs / 2, touch.y - gs / 2]
        else:
            self.endpoint = [touch.x, touch.y]
            self.midpoint.pos = [(self.startpoint[0] + touch.x - gs) / 2, (self.startpoint[1] + touch.y - gs) / 2]
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
        self.midpoint.x += diff[0]  
        self.midpoint.y += diff[1]
        self.update()
        
    def destroy_self(self):
        self.startstate.transitions.remove(self)
        self.endstate.transitions.remove(self)
        globvars.AllItems['stateMachine'].remove_widget(self.midpoint)
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
        self.colours = [Color(1, 1, 1), Color(0, 0, 0), Color(1, 1, 1), Color(1, 1, 1), Color(1, 1, 1)]
        self.finalstatecolour = Color(1, 1, 1)
        self.final = False
        self.transitions = []
        self.State_update()
        
    def State_update(self):
        for t in self.transitions:
            t.update_point(self, [self.center_x, self.center_y])
        pd = 2
        self.canvas.clear()
        for i in range(5):
            self.canvas.add(self.colours[i])
            self.canvas.add(Ellipse(pos = (self.x + i * pd, self.y + i * pd), size = (self.width - 2 * i * pd, self.height - 2 * i * pd)))
        
    def highlighted(self, highlighted):
        if highlighted:
            self.colours[0] = Color(1, 1, 0)
        else:
            self.colours[0] = Color(1, 1, 1)
        self.State_update()
        
    def finalstatetoggle(self):
        self.finalstate(not self.final)
        
    def finalstate(self, final):
        self.final = final
        if final:
            self.colours[3] = Color(0, 0, 0)
        else:
            self.colours[3] = Color(1, 1, 1)
        self.State_update()
        
    def distance_centre(self, touch):
        dx = self.center_x - touch.x
        dy = self.center_y - touch.y
        return sqrt((dx ** 2) + (dy ** 2))
        
    def collide_point(self, touch):
        if self.distance_centre(touch) <= (self.height / 2):
            return True
        return False
        
    def collide_State(self, touch):
        if self.distance_centre(touch) <= self.height:
            return True
        return False

    def check_touch(self, touch):
        if self.collide_point(touch):
            touch.ud['touched'] = self
            return True
        return False
        
    def try_move(self, touch):
        for state in globvars.AllItems['states']:
            if state == self:
                pass
            elif state.collide_State(touch):
                return
        self.center = (touch.x, touch.y)
        self.State_update()
        
    def move(self, dx, dy):
        self.pos = (self.x + dx, self.y + dy)
        self.State_update()
        
    def move_to_centre(self):
        dx = globvars.AllItems['stateMachine'].center_x - self.center_x
        dy = globvars.AllItems['stateMachine'].center_y - self.center_y
        for state in globvars.AllItems['states']:
            state.move(dx, dy)
            
    def destroy_self(self):
        while len(self.transitions):
            t = self.transitions[0]
            t.destroy_self()
        globvars.AllItems['stateMachine'].remove_widget(self)
        globvars.AllItems['states'].remove(self)

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
            
        touch.ud['last'] = [touch.x, touch.y]
            
        if self.mode == "create_t":
            if self.identify_transition_on(touch):
                return
        
        if self.identify_state_in(touch):
            if self.mode == "final":
                touch.ud['touched'].finalstatetoggle()
            if self.mode == "delete":
                touch.ud['touched'].destroy_self()
            if self.mode == "create_t":
                self.make_transition(touch)
            return
        
        touch.ud['touched'] = self
                
        if self.mode == "create_s":
            for state in globvars.AllItems['states']:
                if state.collide_State(touch):
                    return
            state = State(pos = (touch.x - 25, touch.y - 25))
            self.add_widget(state)
            globvars.AllItems['states'].append(state)
            touch.ud['touched'] = state
            
    def move_all_touch(self, touch):
        self.move_all(touch.x - touch.ud['last'][0], touch.y - touch.ud['last'][1])
        touch.ud['last'] = [touch.x, touch.y]
        
    def move_all(self, x, y):
        for state in globvars.AllItems['states']:
            state.move(x, y)
            
    def set_mode(self, mode):
        self.mode = mode
        if mode == "create_t":
            display = True
        else:
            display = False
        for t in globvars.AllItems['transitions']:
            t.display_mover(display)
        
    def try_move(self, touch):
        pass
        
    def extend_line(self, touch):
        pass
        
    def make_transition(self, touch):
        touch.ud['touched'].highlighted(True)
        t = Transition()
        t.startpoint = [touch.ud['touched'].center_x, touch.ud['touched'].center_y]
        t.startstate = touch.ud['touched']
        touch.ud['touched'] = t
        self.add_widget(t)
        
    def finish_transition(self, touch):
        if touch.ud['touched'] == self:
            return
        t = touch.ud['touched']
        if t.complete:
            return
        t.startstate.highlighted(False)
        if not self.identify_state_in(touch):
            self.remove_widget(t)
            return
        
        t.endpoint = [touch.ud['touched'].center_x, touch.ud['touched'].center_y]
        t.endstate = touch.ud['touched']
        t.startstate.transitions.append(t)
        t.endstate.transitions.append(t)
        t.complete = True
        t.update()
        globvars.AllItems['transitions'].append(t)
        self.states_to_front()
        
    def states_to_front(self):
        for state in globvars.AllItems['states']:
            self.remove_widget(state)
            self.add_widget(state)
        if self.mode == "create_t":
            for t in globvars.AllItems['transitions']:
                self.remove_widget(t.midpoint)
                self.add_widget(t.midpoint)
    
    def identify_state_in(self, touch):
        for state in globvars.AllItems['states']:
            if state.check_touch(touch):
                return True
        return False
    
    def identify_transition_on(self, touch):
        for t in globvars.AllItems['transitions']:
            if t.check_touch(touch):
                return True
        return False
        
    def on_touch_move(self, touch):
        if self.outofbounds:
            return
        if self.mode == "move":
            self.move_all_touch(touch)
        if self.mode == "create_s":
            touch.ud['touched'].try_move(touch)
        if self.mode == "create_t":
            touch.ud['touched'].extend_line(touch)
        
    def finalstatetoggle(self):
        pass
        
    def on_touch_up(self, touch):
        if self.outofbounds:
            return
        if self.mode == "create_t":
            self.finish_transition(touch)
    
    def centreMachine(self):
        maxx, maxy, minx, miny = -maxint, -maxint, maxint, maxint
        for state in globvars.AllItems['states']:
            maxx = max(maxx, state.center_x)
            maxy = max(maxy, state.center_y)
            minx = min(minx, state.center_x)
            miny = min(miny, state.center_y)
        avgx = (maxx + minx) / 2
        avgy = (maxy + miny) / 2
        self.move_all(self.center_x - avgx, self.center_y - avgy)
        
class StateMachine(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(StateMachine, self).__init__(*args, **kwargs)
        screen = Screen()
        screen.add_widget(_StateMachine())
        self.add_widget(screen)