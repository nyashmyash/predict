import pickle

clients_data = [{"name": "AAAA"}, {"name": "BBBB"}, {"name": "CCCC"}, {"name": "DDDD"}]
products_data = [{"name": "aaaaa"}, {"name": "bbbb"}, {"name": "ccccc"}, {"name": "ddddd"}, {"name": "eeeee"}, {"name": "ggggg"}, {"name": "fffff"}]
purchase_data = [{"client": "AAAA", "product": "aaaaa"},
                 {"client": "BBBB", "product": "bbbb"},
                 {"client": "BBBB", "product": "ccccc"},
                 {"client": "BBBB", "product": "ddddd"},
                 {"client": "BBBB", "product": "eeeee"},
                 {"client": "CCCC", "product": "ggggg"},
                 {"client": "CCCC", "product": "fffff"},
                 {"client": "BBBB", "product": "ddddd"},
                 {"client": "BBBB", "product": "eeeee"},
                 {"client": "CCCC", "product": "ggggg"},
                 {"client": "CCCC", "product": "fffff"}]

with open("clients.pickle", 'wb') as f:
    pickle.dump(clients_data, f)
with open("products.pickle", 'wb') as f:
    pickle.dump(products_data, f)
with open("purchases.pickle", 'wb') as f:
    pickle.dump(purchase_data, f)
