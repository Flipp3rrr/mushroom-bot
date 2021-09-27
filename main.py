import os
import json
import discord
from discord.ext import commands
import random
import pathlib

run_dir = os.path.dirname(__file__)

# Settings are saved in 'settings.json', settings are saved in a dictionary. This function gets the value of a key specified ('name').
def get_setting(name):
    purpose = name
    settings_file_path = os.path.join(run_dir, "settings.json")
    if os.path.exists(settings_file_path):
        with open(settings_file_path) as settings_file:
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
bot_invite = "https://discord.com/api/oauth2/authorize?client_id=890578768849158175&permissions=2147534848&scope=bot"
github_link = "https://github.com/Flipp3rrr/mushroom-bot"
picture_dir = os.path.join(run_dir, "pictures")

intents = discord.Intents.default()

bot_prefix = get_setting("prefix")
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

# Thanks to StackOverflow 'https://stackoverflow.com/questions/7099290/how-to-ignore-hidden-files-using-os-listdir'
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

@bot.event
async def on_ready():
    print("Logged in as {user} ({id})".format(user = bot.user.name, id = bot.user.id))
    presence = discord.Game("prefix is '{prefix}'".format(prefix = bot_prefix))
    await bot.change_presence(status=discord.Status.idle, activity=presence)

@bot.command()
async def list_collections(ctx, description = "List all available collections"):
    collections = listdir_nohidden(picture_dir)
    await ctx.send("Possible collections: {list}".format(list = list(collections)))

@bot.command(pass_context = True)
async def picture(ctx, collection:str, description = "Get a random image from a collection specified"):
    collection_dir = pathlib.Path(picture_dir) / collection

    jpegs = list(collection_dir.glob("**/*.jpg"))
    choice = random.choice(jpegs)

    embed = discord.Embed(title = "{collection} picture".format(collection = collection))
    image = discord.File(choice, filename = choice.name)
    embed.set_image(url = "attachment://{file}".format(file = choice.name))
    embed.set_footer(text = "Requested by {message_author}".format(message_author = ctx.message.author))
    await ctx.send(file = image, embed = embed)

@bot.command()
async def info(ctx, description = "Get information about the bot"):
    await ctx.send("I was made by Flipp3rrr#6969. My code is available at {github} and you can invite me with {invite}".format(github = github_link, invite = bot_invite))

bot.run(token)