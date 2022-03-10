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
        self.codes1 = []
        for items in country_codes:
            self.codes1.append(str(items))
        self.codes = self.codes1

        self.rates = current_data

        self.convert_button = Button(
            text="Convert", size_hint=(0.2, 0.2), pos=(315, 250)
        )
        self.convert_button.bind(on_press=self.conversion)
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

        self.textinput1 = TextInput(size_hint=(0.2, 0.1), pos=(55, 400))
        self.window.add_widget(self.textinput1)

        self.textinput2 = TextInput(size_hint=(0.2, 0.1), pos=(580, 400))
        self.window.add_widget(self.textinput2)

        return self.window

    @staticmethod
    def conversion(self):
        textinput1 = self.textinput1.text
        dropdown1 = self.dropdown1.text
        dropdown2 = self.dropdown2.text
        if dropdown1 == dropdown2:
            new_amount = textinput1
        elif dropdown1 == "USD":
            to_curr = dropdown2[2:5]
            new_amount = int(textinput1) / int(self.rates[to_curr])
        else:
            from_curr = dropdown1[2:5]
            to_curr = dropdown2[2:5]
            to_usd = int(textinput1) / int(self.rates[from_curr])
            new_amount = to_usd / int(self.rates[to_curr])

        self.textinput2.insert_text(str(new_amount))


app = MyProject()

if __name__ == "__main__":
    app.run()

print(type(app.codes))
