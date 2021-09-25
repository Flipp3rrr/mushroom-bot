import os
import json
import discord
from discord.ext import commands
import random

run_dir = os.path.dirname(__file__)

# Settings are saved in 'settings.json', settings are saved in a dictionary. This function gets the value of a key specified ('name').
def get_setting(name):
    purpose = name
    settings_file_path = os.path.join(run_dir, "settings.json")
    if os.path.existssettings_file_path):
        with opensettings_file_path) as settings_file:
            settings = json.load(settings_file)

        if name in settings:
            return_value = settings[name]
            return(return_value)
        else:
            new_key = name
            new_value = input("{purpose}: ".format(purpose = purpose))
            new_dict = {"{key}".format(key = new_key): "{value}".format(value = new_value)}

            settings.update(new_dict)
            settings_file = open(settings_file_path, "w+")
            json.dump(settings, settings_file, indent = 4)

            return_value = settings[name]
            return(return_value)
    else:
        new_key = name
        new_value = input("{purpose}: ".format(purpose = purpose))
        new_dict = {"{key}".format(key = new_key): "{value}".format(value = new_value)}

        settings = new_dict
        settings_file = open(settings_file_path, "w+")
        json.dump(settings, settings_file, indent = 4)

        return_value = settings[name]
        return(return_value)

token = get_setting("token")
picture_dir = os.path.join(run_dir, "pictures")

intents = discord.Intents.default()

bot = commands.Bot(command_prefix=";;", intents=intents)

# Thanks to StackOverflow 'https://stackoverflow.com/questions/7099290/how-to-ignore-hidden-files-using-os-listdir'
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

@bot.event
async def on_ready():
    print("Logged in as {user} ({id})".format(user = bot.user.name, id = bot.user.id))

@bot.command()
async def list_collections(ctx, description = "List all available collections"):
    collections = listdir_nohidden(picture_dir)
    await ctx.send("Possible collections: {list}".format(list = collections))

@bot.command()
async def picture(ctx, collection:str, description = "Get a random image from a collection specified"):
    collection_dir = os.path.join(picture_dir, collection)

    author_choices = list(listdir_nohidden(collection_dir))
    author_choice_index = random.randrange(len(author_choices))
    author_chosen = author_choices[author_choice_index]
    author_dir = os.path.join(collection_dir, author_chosen)

    image_choices = list(listdir_nohidden(author_dir))
    image_choice_index = random.randrange(len(image_choices))
    image_chosen = image_choices[image_choice_index]
    image_path = os.path.join(author_dir, image_chosen)

    await ctx.send("Here's an image from the '{collection}' collection, submitted by {author}".format(collection = collection, author = author_chosen), file=discord.File(image_path))

bot.run(token)