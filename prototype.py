from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from math import sqrt
from kivy.uix.screenmanager import ScreenManager, Screen

handle = None
machine = None
oldx = None
oldy = None
outofbounds = True

class State(Widget):
    def collide_point(self, touch):
        dx = self.center_x - touch.x
        dy = self.center_y - touch.y
        dist = sqrt((dx ** 2) + (dy ** 2))
        if dist <= (self.height / 2):
            return True
        return False
        
    def collide_widget(self, new):
        dx = self.center_x - new.center_x
        dy = self.center_y - new.center_y
        dist = sqrt((dx ** 2) + (dy ** 2))
        if dist <= self.height:
            return True
        return False

    def on_touch_down(self, touch):
        global handle
        if self.collide_point(touch):
            handle = self
            return True
        return False
            
    def on_touch_move(self, touch):
        global handle
        if handle != self:
            return False
        oldx = handle.x
        oldy = handle.y
        handle.x = touch.x - 25
        handle.y = touch.y - 25
        for other in machine.children:
            if other == handle:
                pass
            elif handle.collide_widget(other):
                handle.x = oldx
                handle.y = oldy
        return True
        
    def move(self, dx, dy):
        oldx = self.x
        oldy = self.y
        self.x = oldx + dx
        self.y = oldy + dy

class StateMachine(FloatLayout):
    def __init__(self):
        super(StateMachine, self).__init__()
        self.mode = "create"
        self.outofbounds = True
    
    def on_touch_down(self, touch):
        self.outofbounds = False
        if ((touch.x < self.x) or (touch.x > self.x + self.width) or (touch.y < self.y) or (touch.y > self.y + self.height)):
            self.outofbounds = True
            return
        for states in self.children:
            if states.on_touch_down(touch):
                return
                
        global oldx, oldy
        oldx = touch.x
        oldy = touch.y
                
        if self.mode == "create":
            state = State(x = touch.x - 25, y = touch.y - 25)
            for states in self.children:
                if state.collide_widget(states):
                    return
            self.add_widget(state,-1)
            global handle
            handle = state
        
    def on_touch_move(self, touch):
        if self.outofbounds:
            return
        for states in self.children:
            if states.on_touch_move(touch):
                return
        global oldx, oldy
        for states in self.children:
            states.move(touch.x - oldx, touch.y - oldy)
        oldx = touch.x
        oldy = touch.y
        
    def on_touch_up(self, touch):
        global handle
        handle = None
        
class CreateButton(Button):
    def on_press(self):
        global machine
        machine.mode = "create"
        
class MoveButton(Button):
    def on_press(self):
        global machine
        machine.mode = "move"
        
class Toolbar(BoxLayout):
    def __init__(self):
        super(Toolbar, self).__init__()
        self.size_hint = 1, None
        self.height = 60
        self.add_widget(CreateButton())
        self.add_widget(MoveButton())
        self.add_widget(Widget())
        
class Container(BoxLayout):
    def __init__(self):
        super(Container, self).__init__()
        self.orientation = 'vertical'
        global machine
        self.add_widget(Toolbar())
        machine = StateMachine()
        screen = Screen()
        screen.add_widget(machine)
        sm = ScreenManager()
        sm.add_widget(screen)
        self.add_widget(sm)

class PrototypeApp(App):
    def build(self):
        return Container()

if __name__ == '__main__':
    PrototypeApp().run()