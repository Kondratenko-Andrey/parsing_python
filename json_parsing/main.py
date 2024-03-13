import requests


def messages(collection, data={}):
    if isinstance(collection, list):
        for el in collection:
            if isinstance(el, (dict, list)):
                data = messages(el, data=data)

    elif isinstance(collection, dict):
        for k, v in collection.items():
            if k == 'username':
                data[v] = data.get(v, 0) + 1

            elif isinstance(v, (dict, list)):
                data = messages(v, data=data)

    return data


link = 'https://parsinger.ru/3.4/3/dialog.json'

response = requests.get(link)
json_data = response.json()
message_data = messages(json_data)
sorted_data = sorted(sorted(message_data.keys()), key=lambda x: message_data[x], reverse=True)
print({k: message_data[k] for k in sorted_data})
