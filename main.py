import os
import json
import requests

def get_setting(name):
    purpose = name
    if os.path.exists("settings.json"):
        settings = open("settings.json", "r").read()

        if name in settings:
            return_value = settings[name]
            return(return_value)
        else:
            new_key = name
            new_value = input("{purpose}: ".format(purpose = purpose))
            new_dict = {"{key}".format(key = new_key): "{value}".format(value = new_value)}

            settings.update(new_dict)
            settings_file = open("settings.json", "w+")
            json.dump(settings, "settings.json", indent = 4)
    else:
        new_key = name
        new_value = input("{purpose}: ".format(purpose = purpose))
        new_dict = {"{key}".format(key = new_key): "{value}".format(value = new_value)}

        settings = new_dict
        settings_file = open("settings.json", "w+")
        json.dump(settings, settings_file, indent = 4)

id1 = get_setting("id")
print(id1)