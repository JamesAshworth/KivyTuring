from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Ellipse, Rectangle, Line, Triangle
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from math import sqrt, degrees, atan2
from sys import maxint
import globvars

class StateLabel(Label):
    pass
    
class RotateLabel(Label):
    pass
    
class StateNamer(Popup):
    def __init__(self, object, *args, **kwargs):
        super(StateNamer, self).__init__(*args, **kwargs)
        self.auto_dismiss = False
        self.title = "State Name?"
        self.content = BoxLayout()
        self.content.orientation = 'vertical'
        self.content.add_widget(Label(height = 30, size_hint = (1, None), text = "Please provide a unique name for this state:"))
        self.textinput = TextInput(height = 30, size_hint = (1, None), multiline = False)
        self.textinput.bind(on_text_validate=self.dismiss)
        self.content.add_widget(self.textinput)
        self.feedback = Label()
        self.content.add_widget(self.feedback)
        self.object = object
        self.bind(on_dismiss=self.post_process)
        
    def open(self, *args, **kwargs):
        super(StateNamer, self).open(*args, **kwargs)
        Clock.schedule_once(self.set_focus_text)
    
    def post_process(self, instance):
        if self.textinput.text == "":
            self.feedback.text = "State name can not be blank"
            Clock.schedule_once(self.set_focus_text)
            return True
        for state in globvars.AllItems['states']:
            if state == self.object:
                pass
            elif state.text == self.textinput.text:
                self.feedback.text = "State name is not unique"
                Clock.schedule_once(self.set_focus_text)
                return True
        self.object.set_text(self.textinput.text)
        return False
        
    def set_focus_text(self, instance):
        self.textinput.focus = True
    
class TransitionInfo(ScatterLayout):
    def __init__(self, *args, **kwargs):
        super(TransitionInfo, self).__init__(*args, **kwargs)
        self.label = RotateLabel(text = "info\n\n")
        self.add_widget(self.label)
        
    def update_info(self, text):
        self.label.text = text

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
        self.midpoint   = TransitionGrabber()
        self.info       = TransitionInfo(size = (60, 60), size_hint = (None, None))
        self.endpoint   = None
        self.endstate   = None
        self.display    = True
        self.complete   = False
        
    def line_middle(self):
        gs = globvars.AllItems['gs']
        points = self.midpoints_calc()
        if len(points) == 2:
            x = self.startpoint[0] / 4 + points[0] / 2 + self.endpoint[0] / 4
            y = self.startpoint[1] / 4 + points[1] / 2 + self.endpoint[1] / 4
        else:
            x = self.startpoint[0] / 16 + points[0] / 4 + points[2] * 3 / 8 + points[4] / 4 + self.endpoint[0] / 16
            y = self.startpoint[1] / 16 + points[1] / 4 + points[3] * 3 / 8 + points[5] / 4 + self.endpoint[1] / 16
        return [x, y]
        
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
        self.canvas.add(Color(0, 0, 0))
        self.canvas.add(Line(bezier = self.startpoint + self.midpoints_calc() + self.endpoint, width = pd))
        centre = self.line_middle()
        self.canvas.add(Triangle(center = (centre[0] - 10, centre[1] - 10), points = self.direction_triangle()))
        self.info.pos = (centre[0] - 30, centre[1] - 30)
        self.info.rotation = self.rotation_angle()
        globvars.AllItems['stateMachine'].remove_widget(self.midpoint)
        if self.display:
            self.midpoint.update()
            globvars.AllItems['stateMachine'].add_widget(self.midpoint)
            
    def finish_transition(self):
        gs = globvars.AllItems['gs']
        self.complete = True
        self.endpoint = [self.endstate.center_x, self.endstate.center_y]
        self.midpoint.pos = [(self.startpoint[0] + self.endpoint[0] - gs) / 2, (self.startpoint[1] + self.endpoint[1] - gs) / 2]
        if self.startstate == self.endstate:
            self.midpoint.y += 100
        self.update()
        globvars.AllItems['stateMachine'].add_widget(self.info)
            
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
        self.colours = [Color(1, 1, 1), Color(0, 0, 0), Color(1, 1, 1), Color(1, 1, 1), Color(1, 1, 1)]
        self.finalstatecolour = Color(1, 1, 1)
        self.final = False
        self.transitions = []
        self.name = ""
        self.label = StateLabel(pos = self.pos, size = self.size)
        self.edit_name()
        self.State_update()
        
    def edit_name(self):
        popup = StateNamer(self)
        popup.open()
        
    def State_update(self):
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
            self.colours[0] = Color(1, 1, 1)
        self.State_update()
        
    def set_text(self, text):
        self.text = text
        self.label.text = text
        
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
            
        if self.identify_transition_on(touch):
            if self.mode == "create_t":
                return
            if self.mode == "delete":
                touch.ud['touched'].destroy_self()
                return
        
        if self.identify_state_in(touch):
            if self.mode == "final":
                touch.ud['touched'].finalstatetoggle()
            if self.mode == "delete":
                touch.ud['touched'].destroy_self()
            if self.mode == "create_t":
                self.make_transition(touch)
            if self.mode == "edit":
                touch.ud['touched'].edit_name()
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
        display = False
        if mode == "create_t":
            display = True
        if mode == "delete":
            display = True
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
            self.remove_widget(t.midpoint)
            return
        
        t.endstate = touch.ud['touched']
        t.finish_transition()
        t.startstate.transitions.append(t)
        t.endstate.transitions.append(t)
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