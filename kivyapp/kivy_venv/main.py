from kivy.config import Config

Config.set("graphics", "width", "1080")
Config.set("graphics", "height", "900")
Config.set("graphics", "resizable", False)
from turtle import onrelease
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy_garden.mapview import (
    MapView,
    MapSource,
    MapMarker,
)
from kivy.app import App
import requests as req

# NATION STATE CURRENCY DATA
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
with open("csv_data/coordinates.csv", "r") as fid:
    lines = fid.readlines()
del lines[0]
lines = [item[3:-4] for item in lines]
lines = [item.split(",") for item in lines]
lines = [item[0:3] for item in lines]
coordinates = lines

# CURRENCY CODES
with open("csv_data/codes.csv", "r") as fid:
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

# CRYPTO DATA
c_api_key = "2d56fa3d1238c54975242d787469176588ff9e34"
crypto_url = f"https://api.nomics.com/v1/currencies/ticker?key={c_api_key}"
c_data_object = req.get(crypto_url)
c_data_json = c_data_object.json()
coins = [[item["symbol"], item["name"], item["price"]] for item in c_data_json]

# PRICE DATA DICTIONARY
coins_price = [[item[:][0], item[:][2]] for item in coins]
coins_price_dict = dict(coins_price)

# SYMBOLS AND NAMES FOR DROPDOWNS
coins_id = [[item[:][0], item[:][1]] for item in coins]
coins_id_list = []
for item in coins_id:
    coins_id_list.append(str(" ".join(item)))


class Actions(MapView):

    # ACTIONS TO BE TAKEN ONCE CURRENCIES ARE SELECTED IN DROPDOWNS (GREETING TEXT, MAP MARKERS, ZOOM TO MARKERS)
    def select_btn1(self, x):
        app.mainbutton1.text = x.text
        app.dropdown1.select(app.mainbutton1.text)
        self.marker1key = app.mainbutton1.text[0:3]
        coins3_split = app.mainbutton3.text.split(" ")
        coins3 = coins3_split[0]
        if app.mainbutton1.text == "From Currency":
            app.mapview.remove_marker(app.marker1)
            app.window.remove_widget(app.moon)
        elif app.mainbutton2.text == "  ":
            app.greeting.text = "FROM " + self.marker1key + " TO " + coins3
            app.marker1.lat = lat_dict[self.marker1key]
            app.marker1.lon = long_dict[self.marker1key]
            app.window.remove_widget(app.moon)
            app.window.add_widget(app.moon)
        elif app.mainbutton3.text == " ":
            app.greeting.text = "From " + self.marker1key + " TO " + self.marker2key
            app.marker1.lat = lat_dict[self.marker1key]
            app.marker1.lon = long_dict[self.marker1key]
            app.window.remove_widget(app.moon)
        elif (
            app.mainbutton2.text == "To Currency"
            and app.mainbutton3.text == "To Cryptocurrency"
        ):
            app.greeting.text = "From " + self.marker1key + " TO ___"
            app.marker1.lat = lat_dict[self.marker1key]
            app.marker1.lon = long_dict[self.marker1key]
            app.window.remove_widget(app.moon)
        app.mapview.remove_marker(app.marker1)
        app.mapview.add_marker(app.marker1)
        app.mapview.center_on(app.marker1.lat, app.marker1.lon)
        app.mapview.zoom = 5
        app.greeting.pos = (5, 330)
        app.mainbutton4.text = ""

    def select_btn2(self, x):
        app.mainbutton2.text = x.text
        app.dropdown2.select(app.mainbutton2.text)
        self.marker2key = app.mainbutton2.text[0:3]
        coins4_split = app.mainbutton4.text.split(" ")
        coins4 = coins4_split[0]
        if (
            app.mainbutton1.text == "From Currency"
            and app.mainbutton4.text == "From Cryptocurrency"
        ):
            app.greeting.text = "FROM ___ TO " + self.marker2key
            app.marker2.lat = lat_dict[self.marker2key]
            app.marker2.lon = long_dict[self.marker2key]
            app.window.remove_widget(app.moon)
        elif app.mainbutton1.text == "   ":
            app.greeting.text = "FROM " + coins4 + " TO " + self.marker2key
            app.marker2.lat = lat_dict[self.marker2key]
            app.marker2.lon = long_dict[self.marker2key]
            app.window.remove_widget(app.moon)
            app.window.add_widget(app.moon)
        else:
            app.greeting.text = (
                "FROM " + app.mainbutton1.text[0:3] + " TO " + self.marker2key
            )
            app.marker2.lat = lat_dict[self.marker2key]
            app.marker2.lon = long_dict[self.marker2key]
            app.window.remove_widget(app.moon)
        app.mapview.remove_marker(app.marker2)
        app.mapview.add_marker(app.marker2)
        app.mapview.center_on(app.marker2.lat, app.marker2.lon)
        app.mapview.zoom = 5
        app.greeting.pos = (5, 330)
        app.mainbutton3.text = " "

    def select_btn3(self, x):
        app.mainbutton3.text = x.text
        app.dropdown3.select(app.mainbutton3.text)
        coins3_split = app.mainbutton3.text.split(" ")
        coins3 = coins3_split[0]
        coins4_split = app.mainbutton4.text.split(" ")
        coins4 = coins4_split[0]
        if (
            app.mainbutton1.text == "From Currency"
            and app.mainbutton4.text == "From Cryptocurrency"
        ):
            app.greeting.text = "FROM ___" + " TO " + coins3
        elif app.mainbutton1.text == "   ":
            app.greeting.text = "FROM " + coins4 + " TO " + coins3
        elif app.mainbutton4.text == "":
            app.greeting.text = "FROM " + app.mainbutton1.text[0:3] + " TO " + coins3
        app.greeting.pos = (5, 330)
        app.mainbutton2.text = "  "
        app.mapview.remove_marker(app.marker2)
        app.window.remove_widget(app.moon)
        app.window.add_widget(app.moon)

    def select_btn4(self, x):
        app.mainbutton4.text = x.text
        app.dropdown4.select(app.mainbutton4.text)
        coins4_split = app.mainbutton4.text.split(" ")
        coins4 = coins4_split[0]
        coins3_split = app.mainbutton3.text.split(" ")
        coins3 = coins3_split[0]
        if (
            app.mainbutton2.text == "To Currency"
            and app.mainbutton3.text == "To Cryptocurrency"
        ):
            app.greeting.text = "FROM " + coins4 + " TO ___"
        elif app.mainbutton2.text == "  ":
            app.greeting.text = "FROM " + coins4 + " TO " + coins3
        elif app.mainbutton3.text == " ":
            app.greeting.text = "FROM " + coins4 + " TO " + app.mainbutton2.text[0:3]
        app.greeting.pos = (5, 330)
        app.mainbutton1.text = "   "
        app.mapview.remove_marker(app.marker1)
        app.window.remove_widget(app.moon)
        app.window.add_widget(app.moon)

    # CONVERT BUTTON FUNCTIONALITY (CONVERT CURRENCIES, PLACE TEXT IN BOX 2, ZOOM MAP OUT)
    def conversion(self, x):
        if (
            app.textinput1.text == ""
            and (
                app.mainbutton1.text == "From Currency"
                or app.mainbutton4.text == "From Cryptocurrency"
            )
            and (
                app.mainbutton2.text == "To Currency"
                or app.mainbutton3.text == "To Cryptocurrency"
            )
        ):
            new_amount = "Choose currencies and enter initial amount!"
            app.text_input_button.font_size = 25
        elif app.textinput1.text == "" and (
            app.mainbutton1.text == "From Currency"
            or app.mainbutton4.text == "From Cryptocurrency"
        ):
            new_amount = "Choose first currency and enter initial amount!"
            app.text_input_button.font_size = 25
        elif app.textinput1.text == "" and (
            app.mainbutton2.text == "To Currency"
            or app.mainbutton3.text == "To Cryptocurrency"
        ):
            new_amount = "Choose second currency and enter initial amount!"
            app.text_input_button.font_size = 25
        elif app.textinput1.text == "":
            new_amount = "Enter initial amount!"
            app.text_input_button.font_size = 30
        elif (
            app.mainbutton1.text == "From Currency"
            or app.mainbutton4.text == "From Cryptocurrency"
        ) and (
            app.mainbutton2.text == "To Currency"
            or app.mainbutton3.text == "To Cryptocurrency"
        ):
            new_amount = "Choose currencies!"
            app.text_input_button.font_size = 30
        elif (
            app.mainbutton1.text == "From Currency"
            or app.mainbutton4.text == "From Cryptocurrency"
        ):
            new_amount = "Choose first currency!"
            app.text_input_button.font_size = 30
        elif (
            app.mainbutton2.text == "To Currency"
            or app.mainbutton3.text == "To Cryptocurrency"
        ):
            new_amount = "Choose second currency!"
            app.text_input_button.font_size = 30
        elif str.isnumeric(app.textinput1.text) == False:
            new_amount = "Not a number!"
            app.text_input_button.font_size = 30
        elif (
            app.mainbutton1.text == app.mainbutton2.text
            or app.mainbutton1.text == app.mainbutton3.text
            or app.mainbutton2.text == app.mainbutton4.text
            or app.mainbutton3.text == app.mainbutton4.text
        ):
            new_amount = "Currencies are the same!"
            app.text_input_button.font_size = 30
        elif len(app.mainbutton4.text) > 4 and len(app.mainbutton3.text) > 4:
            coins4_split = app.mainbutton4.text.split(" ")
            coins4 = coins4_split[0]
            coins3_split = app.mainbutton3.text.split(" ")
            coins3 = coins3_split[0]
            usd = float(app.textinput1.text) * float(coins_price_dict[coins4])
            mid_conversion = usd / float(coins_price_dict[coins3])
            new_amount = round(mid_conversion, 4)
        elif len(app.mainbutton1.text) > 4 and len(app.mainbutton3.text) > 4:
            coins3_split = app.mainbutton3.text.split(" ")
            coins3 = coins3_split[0]
            usd = float(app.textinput1.text) / app.rates[app.mainbutton1.text[0:3]]
            mid_conversion = usd * float(coins_price_dict[coins3])
            new_amount = round(mid_conversion, 4)
        elif len(app.mainbutton4.text) > 4 and len(app.mainbutton2.text) > 4:
            coins4_split = app.mainbutton4.text.split(" ")
            coins4 = coins4_split[0]
            usd = float(app.textinput1.text) * app.rates[app.mainbutton2.text[0:3]]
            mid_conversion = usd * float(coins_price_dict[coins4])
            new_amount = round(mid_conversion, 4)
        else:
            usd = float(app.textinput1.text) / app.rates[app.mainbutton1.text[0:3]]
            mid_conversion = usd * app.rates[app.mainbutton2.text[0:3]]
            new_amount = round(mid_conversion, 4)
            app.text_input_button.font_size = 40

        app.text_input_button.text = ""
        app.text_input_button.text = str(new_amount)
        if len(app.text_input_button.text) > 13:
            app.text_input_button.font_size = 25
        app.mapview.center_on(20, 0)
        app.mapview.zoom = 2

    # MAP ZOOM BUTTONS FUNCTIONALITY
    def zoom_in(self, x):
        if app.mapview.zoom < 12:
            app.mapview.zoom += 1

    def zoom_out(self, x):
        if app.mapview.zoom > 2:
            app.mapview.zoom -= 1


actions = Actions()


# APP STRUCTURE
class TrustyConverto(App):
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
            size_hint=(0.16, 0.19),
            pos=(450, 540),
            on_release=actions.conversion,
            background_color="00FF00",
            font_features="bold",
            font_size=30,
        )
        self.convert_button.bind(on_release=actions.conversion)
        self.window.add_widget(self.convert_button)

        self.greeting = Label(
            text="*BEEP* CONVERTO IS AT YOUR SERVICE *BOOP*",
            bold=True,
            font_size=38,
            outline_width=1,
            outline_color="green",
            pos=(90, 330),
        )
        self.window.add_widget(self.greeting)

        self.converto = Image(
            source="images/chatbot.png",
            keep_ratio=True,
            size=(20, 70),
            size_hint=(0.17, 0.17),
            pos=(20, 710),
        )
        self.window.add_widget(self.converto)

        self.moon = Image(
            source="images/moon.jpg",
            keep_ratio=True,
            size_hint=(0.22, 0.22),
            pos=(785, 705),
        )

        self.dropdown1 = DropDown()
        for items in self.codes:
            self.btn1 = Button(text=items, size_hint_y=None, height=44, font_size=13)
            self.btn1.bind(on_release=actions.select_btn1)
            self.dropdown1.add_widget(self.btn1)
        self.mainbutton1 = Button(
            text="From Currency",
            pos=(20, 540),
            size_hint=(0.19, 0.10),
            background_color="#F67280",
            font_size=14,
        )
        self.mainbutton1.bind(on_release=self.dropdown1.open)
        self.dropdown1.bind(
            on_select=lambda instance, x: setattr(self.mainbutton1, "text", x)
        )
        self.window.add_widget(self.mainbutton1)

        self.dropdown4 = DropDown()
        for items in coins_id_list:
            self.btn4 = Button(text=items, size_hint_y=None, height=44, font_size=13)
            self.btn4.bind(on_release=actions.select_btn4)
            self.dropdown4.add_widget(self.btn4)
        self.mainbutton4 = Button(
            text="From Cryptocurrency",
            pos=(227, 540),
            size_hint=(0.19, 0.10),
            background_color="#F67280",
            font_size=14,
        )
        self.mainbutton4.bind(on_release=self.dropdown4.open)
        self.dropdown4.bind(
            on_select=lambda instance, x: setattr(self.mainbutton4, "text", x)
        )
        self.window.add_widget(self.mainbutton4)

        self.dropdown3 = DropDown()
        for items in coins_id_list:
            self.btn3 = Button(text=items, size_hint_y=None, height=44, font_size=13)
            self.btn3.bind(on_release=actions.select_btn3)
            self.dropdown3.add_widget(self.btn3)
        self.mainbutton3 = Button(
            text="To Cryptocurrency",
            pos=(850, 540),
            size_hint=(0.19, 0.10),
            background_color="#00BFFF",
            font_size=14,
        )
        self.mainbutton3.bind(on_release=self.dropdown3.open)
        self.dropdown3.bind(
            on_select=lambda instance, x: setattr(self.mainbutton3, "text", x)
        )
        self.window.add_widget(self.mainbutton3)

        self.dropdown2 = DropDown(dismiss_on_select=True)
        for items in self.codes:
            self.btn2 = Button(text=items, size_hint_y=None, height=44, font_size=13)
            self.btn2.bind(on_release=actions.select_btn2)
            self.dropdown2.add_widget(self.btn2)
        self.mainbutton2 = Button(
            text="To Currency",
            pos=(643, 540),
            size_hint=(0.19, 0.10),
            background_color="#00BFFF",
            font_size=14,
        )
        self.mainbutton2.bind(on_release=self.dropdown2.open)
        self.dropdown2.bind(
            on_select=lambda instance, x: setattr(self.mainbutton2, "text", x)
        )
        self.window.add_widget(self.mainbutton2)

        self.textinput1 = TextInput(
            halign="center",
            size_hint=(0.375, 0.07),
            pos=(23, 650),
            font_size=40,
            background_normal="#D3D3D3",
        )
        self.window.add_widget(self.textinput1)

        self.text_input_button = Button(
            text_size=(290, 100),
            size_hint=(0.375, 0.07),
            padding_x=0,
            pos=(646.5, 650),
            font_size=40,
            disabled=True,
            halign="center",
            valign="middle",
            disabled_color="000000",
            background_normal="#D3D3D3",
            background_disabled_normal="",
        )
        self.window.add_widget(self.text_input_button)

        self.mapsource = MapSource(
            url="https://tile.thunderforest.com/mobile-atlas/{z}/{x}/{y}.png?apikey=8b1e1df284b444579fc51e41f27672b0",
            image_ext="png",
            max_zoom=12,
            min_zoom=2,
        )
        self.marker1 = MapMarker(source="images/red_dot1.png")
        self.marker2 = MapMarker(source="images/blue_dot1.png")
        self.mapview = MapView(
            zoom=2,
            size_hint=(0.95, 0.55),
            pos=(20, 10),
            lat=20,
            lon=0,
            double_tap_zoom=True,
            _zoom=2,
            snap_to_zoom=False,
            map_source=self.mapsource,
        )

        self.window.add_widget(self.mapview)

        self.plus_button = Button(
            size_hint=(0.04, 0.04),
            pos=(1000, 465),
            on_release=actions.zoom_in,
            background_color="#565051",
            text="+",
            font_size=30,
        )
        self.window.add_widget(self.plus_button)

        self.minus_button = Button(
            size_hint=(0.04, 0.04),
            pos=(1000, 430),
            on_release=actions.zoom_out,
            text="-",
            font_size=30,
            background_color="#565051",
        )
        self.window.add_widget(self.minus_button)

        return self.window


app = TrustyConverto()
app.build()

# RUN
if __name__ == "__main__":
    app.run()
