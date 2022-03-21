# CLEAN UP AND ORGANIZE DATA FOR MAPPING
# COORDINATES
with open("world_country_and_usa_states_latitude_and_longitude_values.csv", "r") as fid:
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

# MERGING
def find(elem_a, listb):
    for x in listb:
        if elem_a == x[0]:
            return x[1]
    return False


combined = []
for sub_list in coordinates:
    a = find(sub_list[2], codes_lst)
    if a:
        combined.append(sub_list + [a])

print(combined)


while type(app.dropdown1.text) == str:
    app.mapview.add_marker(app.marker1)
    for item in combined:
        app.marker1.lat = item[app.dropdown1.text[0:3]]
        app.marker1.lon = item[app.dropdown1.text[0:3]]

while type(app.dropdown2.text) == str:
    app.mapview.add_marker(app.marker2)
    for item in combined:
        app.marker2.lat = item[app.dropdown2.text[0:3]]
        app.marker2.lon = item[app.dropdown2.text[0:3]]

        ###########################################################
        if self.dropdown1.text == "From Currency":
            self.mapview.remove_marker(self.marker1)
        else:
            self.greeting.text = "From " + self.marker1key + "..."
            self.marker1.lat = lat_dict[self.marker1key]
            self.marker1.lon = long_dict[self.marker1key]

        if self.dropdown2.text == "To Currency":
            self.mapview.remove_marker(self.marker2)
        else:
            self.greeting.text = "FROM " + self.marker1key + " TO " + self.marker2key
            self.marker2.lat = lat_dict[self.marker2key]
            self.marker2.lon = long_dict[self.marker2key]

########################################################################
def placemarker1():
    if app.dropdown1.text == "From Currency":
        app.mapview.remove_marker(app.marker1)
    else:
        app.greeting.text = "From " + app.marker1key + "..."
        app.marker1.lat = lat_dict[app.marker1key]
        app.marker1.lon = long_dict[app.marker1key]
        app.mapview.add_marker(app.marker1)


def placemarker2():
    if app.dropdown2.text == "To Currency":
        app.mapview.remove_marker(app.marker2)
    else:
        app.greeting.text = "FROM " + app.marker1key + " TO " + app.marker2key
        app.marker2.lat = lat_dict[app.marker2key]
        app.marker2.lon = long_dict[app.marker2key]
        app.mapview.add_marker(app.marker2)


######################################################################
def placemarker():
    if app.event.is_touch == True:
        app.mapview.remove_marker(app.marker1)
        app.greeting.text = "From " + app.marker1key + "..."
        app.marker1.lat = lat_dict[app.marker1key]
        app.marker1.lon = long_dict[app.marker1key]
        app.mapview.add_marker(app.marker1)
        app.mapview.remove_marker(app.marker2)
        app.greeting.text = "FROM " + app.marker1key + " TO " + app.marker2key
        app.marker2.lat = lat_dict[app.marker2key]
        app.marker2.lon = long_dict[app.marker2key]
        app.mapview.add_marker(app.marker2)
