from kivy.config import Config

Config.set("graphics", "width", "800")
Config.set("graphics", "height", "1000")
Config.set("graphics", "resizable", False)
from turtle import onrelease
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.animation import Animation
from kivy.base import runTouchApp
from kivy.input import MotionEvent
from kivy_garden.mapview import MapView, MapSource, MapMarker
from kivy.app import App
import numpy as np
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

# CLEAN UP AND ORGANIZE DATA FOR MAP MARKERS
# COORDINATES
with open("coordinates.csv", "r") as fid:
    lines = fid.readlines()
del lines[0]
lines = [item[3:-4] for item in lines]
lines = [item.split(",") for item in lines]
lines = [item[0:3] for item in lines]
coordinates = lines

# CURRENCY CODES
with open("codes.csv", "r") as fid:
    lines = fid.readlines()
lines = [item.split(",") for item in lines]
lines1 = []
[lines1.append([item[:][0]] + [item[:][-1][0:3]]) for item in lines]
codes_lst = lines1

# MERGING TO DICTIONARY
codes_dict = dict(codes_lst)
combined = [[*v, k, codes_dict.get(k)] for [*v, k] in coordinates if k in codes_dict]
for item in combined:
    del item[2]
combined = [item[-1:] + item[:-1] for item in combined]
combined = [[item[0], [item[1], item[2]]] for item in combined]
[float(item[1][0]) and float(item[1][1]) for item in combined]
lat_list = [[item[0], item[1][0]] for item in combined]
long_list = [[item[0], item[1][1]] for item in combined]
lat_dict = dict(lat_list)
long_dict = dict(long_list)


class TrustyConverto(App):
    def build(self):
        self.window = FloatLayout()
        self.window.resizable = False

        # self.event = MotionEvent(device=click, id=str, args=list)

        self.codes_src = country_codes
        self.codes = []
        for items in country_codes:
            self.codes.append(str(" ".join(items)))

        self.rates = current_data

        self.convert_button = Button(
            text="Convert",
            size_hint=(0.15, 0.12),
            pos=(337, 650),
            on_release=conversion,
            background_color="00FF00",
        )
        self.convert_button.bind(on_release=conversion)
        self.window.add_widget(self.convert_button)

        self.greeting = Label(
            text="BEEP CONVERTO IS AT YOUR SERVICE BOOP",
            bold=True,
            font_size=30,
            outline_width=1,
            outline_color="green",
            pos=(0, 425),
        )
        self.window.add_widget(self.greeting)

        self.dropdown1 = Spinner(
            width=500,
            size_hint=(0.38, 0.1),
            pos=(10, 580),
            values=self.codes,
            text="From Currency",
            on_release=placemarker1
            # text_autoupdate=True,
        )
        self.window.add_widget(self.dropdown1)

        self.dropdown2 = Spinner(
            width=500,
            size_hint=(0.38, 0.1),
            pos=(482, 580),
            values=self.codes,
            text="To Currency",
            on_release=placemarker2
            # text_autoupdate=True,
        )
        self.window.add_widget(self.dropdown2)

        self.textinput1 = TextInput(
            halign="center",
            padding_y=45,
            size_hint=(0.38, 0.13),
            pos=(10, 700),
            font_size=30,
            background_normal="#D3D3D3",
        )
        self.window.add_widget(self.textinput1)

        self.text_input_button = Button(
            text_size=(290, 100),
            size_hint=(0.38, 0.13),
            pos=(482, 700),
            font_size=30,
            disabled=True,
            halign="center",
            valign="middle",
            disabled_color="000000",
            background_normal="#D3D3D3",
            background_disabled_normal="",
        )
        self.window.add_widget(self.text_input_button)

        self.mapview = MapView(
            zoom=2, size_hint=(0.95, 0.55), pos=(20, 10), lat=0, lon=0
        )
        self.marker1 = MapMarker(source="red_dot1.png")
        self.marker2 = MapMarker(source="blue_dot1.png")
        self.marker1key = self.dropdown1.text[0:3]
        self.marker2key = self.dropdown2.text[0:3]
        self.window.add_widget(self.mapview)

        return self.window


app = TrustyConverto()

# MAP MARKER PLACEMENT FUNCTIONS
def placemarker1(self):
    if app.dropdown1.text == "From Currency":
        app.mapview.remove_marker(app.marker1)
    else:
        app.greeting.text = "From " + app.marker1key + "..."
        app.marker1.lat = lat_dict[app.marker1key]
        app.marker1.lon = long_dict[app.marker1key]
        app.mapview.add_marker(app.marker1)


def placemarker2(self):
    if app.dropdown2.text == "To Currency":
        app.mapview.remove_marker(app.marker2)
    else:
        app.greeting.text = "FROM " + app.marker1key + " TO " + app.marker2key
        app.marker2.lat = lat_dict[app.marker2key]
        app.marker2.lon = long_dict[app.marker2key]
        app.mapview.add_marker(app.marker2)


# CURRENCY CONVERSION FUNCTION
def conversion(self):
    if (
        app.textinput1.text == ""
        and app.dropdown1.text == "From Currency"
        and app.dropdown2.text == "To Currency"
    ):
        new_amount = "Choose currencies and enter initial amount!"
    elif app.textinput1.text == "" and app.dropdown1.text == "From Currency":
        new_amount = "Choose first currency and enter initial amount!"
    elif app.textinput1.text == "" and app.dropdown2.text == "To Currency":
        new_amount = "Choose second currency and enter initial amount!"
    elif app.textinput1.text == "":
        new_amount = "Enter initial amount!"
    elif app.dropdown1.text == "From Currency" and app.dropdown2.text == "To Currency":
        new_amount = "Choose currencies!"
    elif app.dropdown1.text == "From Currency":
        new_amount = "Choose first currency!"
    elif app.dropdown2.text == "To Currency":
        new_amount = "Choose second currency!"
    elif app.dropdown1.text == app.dropdown2.text:
        new_amount = "Currencies are the same!"
    elif app.dropdown1.text == "USD, United States Dollar":
        mid_conversion = float(app.textinput1.text) / app.rates[app.dropdown2.text[0:3]]
        new_amount = round(mid_conversion, 4)
    else:
        to_usd = float(app.textinput1.text) / app.rates[app.dropdown1.text[0:3]]
        mid_conversion = to_usd / app.rates[app.dropdown2.text[0:3]]
        new_amount = round(mid_conversion, 4)

    app.text_input_button.text = ""
    app.text_input_button.text = str(new_amount)


# RUN PROGRAM
if __name__ == "__main__":
    app.run()
