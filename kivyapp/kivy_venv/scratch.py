from counter import Counter

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
lines2 = []
[lines2.append(item[:][0] + ", " + item[:][-1]) for item in lines]
lines2 = [item[:-1] for item in lines2]
lines3 = [[item] for item in lines2]
codes_lst = lines3

print(Counter(coordinates))
# print(codes_lst)

[[x, coordinates.count(x)] for x in set(coordinates)]
