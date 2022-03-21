

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
  for x in codes_lst:
    if elem_a == x[0]:
      return x[1]
  return False

combined = []
for sub_list in coordinates:
  a = find(sub_list[2], codes_lst)
  if a:
    combined.append(sub_list + [a])

print(combined)