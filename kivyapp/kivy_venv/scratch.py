import myproject
from myproject import *

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

lat_dict_keys = list(lat_dict.keys())

codes_src = country_codes
codes = []
for items in country_codes:
    codes.append(str(" ".join(items)))


codes_short = [item[0:3] for item in codes]


inboth = []
notinboth = []
for item in codes_short:
    if item in lat_dict_keys:
        inboth.append(item)
    else:
        notinboth.append(item)

inboth2 = []
notinboth2 = []
for item in lat_dict_keys:
    if item in codes_short:
        inboth2.append(item)
    else:
        notinboth2.append(item)

inboth3 = []
notinboth3 = []
for item in notinboth:
    if item in notinboth2:
        inboth3.append(item)
    else:
        notinboth3.append(item)

print(notinboth2)
