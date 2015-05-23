__version__ = '1.8'

from kivy.app import App
from startscreen import StartScreen
from machinescreen import MachineScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.utils import platform
from kivy.clock import Clock
import globvars

android = None

class _Application(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(_Application, self).__init__(*args, **kwargs)
        globvars.AllItems['application'] = self
        screen = Screen(name = "menu")
        startScreen = StartScreen()
        screen.add_widget(startScreen)
        screen.bind(on_pre_enter=startScreen.load_label)
        self.add_widget(screen)
        screen = Screen(name = "machine")
        screen.add_widget(MachineScreen())
        self.add_widget(screen)
        
class Application(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.orientation = 'vertical'
        self.add_widget(_Application())
        self.keyboardSpacer = Widget(size_hint = (1, None), height = 0)
        self.add_widget(self.keyboardSpacer)
        Clock.schedule_interval(self._upd_kbd_height, .5)

    def _upd_kbd_height(self, *kargs):
        self.keyboardSpacer.height = self._get_kheight()
    
    def _get_android_kheight(self):
        global android
        if not android:
            import android
        return android.get_keyboard_height()

    def _get_kheight(self):
        if platform == 'android':
            return self._get_android_kheight()
        return 0
        
class TuringApp(App):
    def open_settings(self, *largs):
        pass
        
    def build(self):
        return Application()

if __name__ == '__main__':
    globvars.create()
    TuringApp().run()