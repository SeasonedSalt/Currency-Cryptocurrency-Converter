from asyncore import read
import kivy

from kivy.app import App
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from data import codes_list

class MyProject(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1

        self.codes_src = codes_list
        self.codes = []
        for items in self.codes_src:
            self.codes.append(items[1])

        self.convert_button = Button(text="Convert", size_hint_y=None, height=40)
        # self.convert_button.bind(on_press=self.callback)
        self.window.add_widget(self.convert_button)

        self.from_curr_select = DropDown(height=20)
        self.window.add_widget(self.from_curr_select)

        # self.greeting = Label(text="Convert Away!")
        # self.window.add_widget(self.greeting)

        self.dropdown1 = DropDown(width = 250)
        for items in self.codes:
            self.btn1 = Button(text=items, size_hint_y=None, height=44)
            self.btn1.bind(on_release=lambda btn: self.dropdown1.select(btn.text))
            self.dropdown1.add_widget(self.btn1)
        self.window.add_widget(self.dropdown1)

        mainbutton1 = Button(text="Select Currency", size_hint=(None, None), bold=True, width=250)
        mainbutton1.bind(on_release=self.dropdown1.open)
        self.dropdown1.bind(
            on_select=lambda instance, x: setattr(mainbutton1, "text", x)
        )
        self.window.add_widget(mainbutton1)
        
        return self.window


app = MyProject()

if __name__ == "__main__":
    app.run()

#print(app.codes)
