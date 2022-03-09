from tkinter import CENTER
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.textinput import TextInput
from data import codes_list


class MyProject(App):
    def build(self):
        self.window = FloatLayout()
        self.window.resizable = False

        self.codes_src = codes_list
        self.codes = []
        for items in self.codes_src:
            self.codes.append(items[1])

        self.convert_button = Button(
            text="Convert", size_hint=(0.2, 0.2), pos=(315, 250)
        )
        # self.convert_button.bind(on_press=self.callback)
        self.window.add_widget(self.convert_button)

        # self.greeting = Label(text="Convert Away!")
        # self.window.add_widget(self.greeting)

        self.dropdown1 = DropDown(width=250, size_hint=(0.2, 0.1), pos=(55, 300))
        for items in self.codes:
            self.btn1 = Button(text=items, height=44, size_hint=(0.2, 0.1))
            self.btn1.bind(on_release=lambda btn: self.dropdown1.select(btn.text))
            self.dropdown1.add_widget(self.btn1)
        self.window.add_widget(self.dropdown1)

        self.dropdown2 = DropDown(width=250, size_hint=(0.2, 0.1), pos=(580, 300))
        for items in self.codes:
            self.btn2 = Button(text=items, height=44, size_hint=(0.2, 0.1))
            self.btn2.bind(on_release=lambda btn: self.dropdown2.select(btn.text))
            self.dropdown1.add_widget(self.btn2)
        self.window.add_widget(self.dropdown2)

        mainbutton1 = Button(
            text="Select Currency",
            size_hint=(0.2, 0.1),
            bold=True,
            width=250,
            pos=(55, 300),
        )
        mainbutton1.bind(on_release=self.dropdown1.open)
        self.dropdown1.bind(
            on_select=lambda instance, x: setattr(mainbutton1, "text", x)
        )
        self.window.add_widget(mainbutton1)

        mainbutton2 = Button(
            text="Select Currency",
            size_hint=(0.2, 0.1),
            bold=True,
            width=250,
            pos=(580, 300),
        )
        mainbutton2.bind(on_release=self.dropdown2.open)
        self.dropdown2.bind(
            on_select=lambda instance, x: setattr(mainbutton2, "text", x)
        )
        self.window.add_widget(mainbutton2)

        self.textinput1 = TextInput(size_hint=(0.2, 0.1), pos=(55, 400))
        self.window.add_widget(self.textinput1)

        self.textinput2 = TextInput(size_hint=(0.2, 0.1), pos=(580, 400))
        self.window.add_widget(self.textinput2)

        return self.window


app = MyProject()

if __name__ == "__main__":
    app.run()

# print(app.codes)
