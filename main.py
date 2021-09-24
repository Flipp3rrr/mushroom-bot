import os
import json
import requests

# Settings are saved in 'settings.json', settings are saved in a dictionary. This function gets the value of a key specified ('name').
def get_setting(name):
    purpose = name
    if os.path.exists("settings.json"):
        with open("settings.json") as settings_file:
            settings = json.load(settings_file)

        if name in settings:
            return_value = settings[name]
            return(return_value)
        else:
            new_key = name
            new_value = input("{purpose}: ".format(purpose = purpose))
            new_dict = {"{key}".format(key = new_key): "{value}".format(value = new_value)}

            settings.update(new_dict)
            settings_file = open("settings.json", "w+")
            json.dump(settings, settings_file, indent = 4)

            return_value = settings[name]
            return(return_value)
    else:
        new_key = name
        new_value = input("{purpose}: ".format(purpose = purpose))
        new_dict = {"{key}".format(key = new_key): "{value}".format(value = new_value)}

        settings = new_dict
        settings_file = open("settings.json", "w+")
        json.dump(settings, settings_file, indent = 4)

        return_value = settings[name]
        return(return_value)

app_id = get_setting("app_id")
token = get_setting("token")

api_url = "https://discord.com/api/v8/applications/{id}/commands".format(id = app_id)

rand_pict_slash_command = {
    "name": "random-picture",
    "type": 1,
    "description": "Send a random picture from a specified collection",
    "options":[
        {
            "name": "collection",
            "description": "The collection you want a picture from",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "Flowers",
                    "value": "collection_flowers"
                },
                {
                    "name": "Frogs",
                    "value": "collection_frogs"
                },
                {
                    "name": "Insects",
                    "value": "collection_insects"
                },
                {
                    "name": "Mushrooms",
                    "value": "collection_mushrooms"
                },
                {
                    "name": "Plants",
                    "value": "collection_plants"
                },
                {
                    "name": "Snakes",
                    "value": "collection_snakes"
                }
            ]
        }
    ]
}

authorization_headers = {
    "Authorization": "Bot {token}".format(token = token)
}

register_slash_commands = input("Do you wish to register the slash commands now? [y/n] ")

if register_slash_commands == "y":
    requests.post(api_url, headers=authorization_headers, json=rand_pict_slash_command)
    print("Slash commands registered")

elif register_slash_commands == "n":
    print("Slash commands not registered")

else:
    print("Invalid answer, slash commands not registered")

