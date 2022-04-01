import requests as req

c_api_key = "2d56fa3d1238c54975242d787469176588ff9e34"
crypto_url = f"https://api.nomics.com/v1/currencies/ticker?key={c_api_key}"
c_data_object = req.get(crypto_url)
c_data_json = c_data_object.json()
coins = [[item["symbol"], item["name"], item["price"]] for item in c_data_json]

coins_price = [[item[:][0], item[:][2]] for item in coins]
coins_price_dict = dict(coins_price)

coins_id = [[item[:][0], item[:][1]] for item in coins]
coins_id_list = []
for item in coins_id:
    coins_id_list.append(str(" ".join(item)))

coins1 = coins_id_list[0]
coins1 = coins1.split(" ")
coins1 = coins1[0]

print(coins1)
