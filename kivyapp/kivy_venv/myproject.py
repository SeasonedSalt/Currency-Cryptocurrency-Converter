from turtle import onrelease
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.base import runTouchApp
from kivy.uix.textinput import TextInput
import requests as req
from functools import partial

api_key = "8ab594a86b3faea921595e6f"

# COUNTRY CODES
codes_url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"
codes_object = req.get(codes_url)
codes_json = codes_object.json()
country_codes = codes_json["supported_codes"]

# CONVERSION DATA
data_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
data_object = req.get(data_url)
data_json = data_object.json()
current_data = data_json["conversion_rates"]


class MyProject(App):
    def build(self):
        self.window = FloatLayout()
        self.window.resizable = False

        self.codes_src = country_codes
        self.codes = []
        for items in country_codes:
            self.codes.append(str(" ".join(items)))

        self.rates = current_data

        self.convert_button = Button(
            text="Convert",
            size_hint=(0.2, 0.2),
            pos=(315, 250),
            on_release=conversion,
        )
        self.convert_button.bind(on_release=conversion)
        self.window.add_widget(self.convert_button)

        self.greeting = Label(text="Convert Away!", pos=(0, 250))
        self.window.add_widget(self.greeting)

        self.dropdown1 = Spinner(
            width=500,
            size_hint=(0.38, 0.1),
            pos=(6, 300),
            values=self.codes,
            text="From Currency",
        )
        self.window.add_widget(self.dropdown1)

        self.dropdown2 = Spinner(
            width=500,
            size_hint=(0.38, 0.1),
            pos=(480, 300),
            values=self.codes,
            text="To Currency",
        )
        self.window.add_widget(self.dropdown2)

        self.textinput1 = TextInput(size_hint=(0.2, 0.1), pos=(55, 400), font_size=30)
        self.window.add_widget(self.textinput1)

        self.textinput2 = TextInput(size_hint=(0.2, 0.1), pos=(580, 400), font_size=30)
        self.window.add_widget(self.textinput2)

        return self.window


app = MyProject()


def conversion(self):
    if app.textinput1.text == "":
        new_amount = ""
    elif app.dropdown1.text == app.dropdown2.text:
        new_amount = app.textinput1.text
    elif app.dropdown1.text == "USD, United States Dollar":
        new_amount = int(app.textinput1.text) / app.rates[app.dropdown2.text[0:3]]
    else:
        to_usd = int(app.textinput1.text) / app.rates[app.dropdown1.text[0:3]]
        new_amount = to_usd / app.rates[app.dropdown2.text[0:3]]

    app.textinput2.text = ""
    app.textinput2.insert_text(str(new_amount))


if __name__ == "__main__":
    app.run()

# print(app.dropdown1.text)
