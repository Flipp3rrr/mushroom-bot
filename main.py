import os
import json
import discord
from discord.ext import commands
import random
import pathlib
import typing

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

# Thanks to StackOverflow 'https://stackoverflow.com/questions/7099290/how-to-ignore-hidden-files-using-os-listdir'
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

picture_dir = os.path.join(run_dir, "pictures")
collections_list = list(listdir_nohidden(picture_dir))
token = get_setting("token")
bot_prefix = get_setting("prefix")
bot_invite = "https://discord.com/api/oauth2/authorize?client_id=890578768849158175&permissions=2147534848&scope=bot"
github_link = "https://github.com/Flipp3rrr/mushroom-bot"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print("Logged in as {user} ({id})".format(user = bot.user.name, id = bot.user.id))
    presence = discord.Game("do '{prefix}help'".format(prefix = bot_prefix))
    await bot.change_presence(status=discord.Status.idle, activity=presence)

@bot.event
async def on_message(message):
    if message.content.startswith("pretty"):
        for collection in collections_list:
            if collection in message.content:
                collection_dir = pathlib.Path(picture_dir) / collection
                
                jpegs = list(collection_dir.glob("**/*.jpg"))
                choice = random.choice(jpegs)

                embed = discord.Embed(title = "{collection} picture".format(collection = collection))
                image = discord.File(choice, filename = choice.name)
                embed.set_image(url = "attachment://{file}".format(file = choice.name))
                embed.set_footer(text = "Requested by {message_author}".format(message_author = message.author))
                await message.channel.send(file = image, embed = embed)
    
    await bot.process_commands(message)

@bot.command()
async def help(ctx, command: typing.Optional[str] = "default_help"):
    if command == "default_help":
        embed = discord.Embed(title = "Help", description = "My prefix is `{prefix}`, get more informations on specific commands with `{prefix}help <command>`.".format(prefix = bot_prefix))
        embed.add_field(name = "Commands", value = "* `collections`\n* `info`\n* `picture`")
        embed.set_footer(text = "Requested by {message_author}".format(message_author = ctx.message.author))
        await ctx.send(embed = embed)

    elif command == "collections":
        embed = discord.Embed(title = "Help (collections)", description = "Sends a message containing a list of available collections.")
        embed.add_field(name = "Example", value = "`{prefix}collections`".format(prefix = bot_prefix))
        embed.set_footer(text = "Requested by {message_author}".format(message_author = ctx.message.author))
        await ctx.send(embed = embed)

    elif command == "info":
        embed = discord.Embed(title = "Help (info)", description = "Sends a message containing relevant information to the bot.")
        embed.add_field(name = "Example", value = "`{prefix}info`".format(prefix = bot_prefix))
        embed.set_footer(text = "Requested by {message_author}".format(message_author = ctx.message.author))
        await ctx.send(embed = embed)

    elif command == "picture":
        embed = discord.Embed(title = "Help (picture)", description = "Sends a random image from the specified collection.")
        embed.add_field(name = "Example", value = "`{prefix}picture <collection>`".format(prefix = bot_prefix), inline = True)
        embed.add_field(name = "Example 2", value = "`pretty <collection>`".format(prefix = bot_prefix), inline = True)
        embed.set_footer(text = "Requested by {message_author}".format(message_author = ctx.message.author))
        await ctx.send(embed = embed)

@bot.command()
async def collections(ctx):
    collections_list.sort()
    # Insert empty item into the list to fix the formatting
    collections_list.insert(0, "")

    embed = discord.Embed(title = "Collections", description = "{list}".format(list = "\n * ".join(collections_list)))
    embed.set_footer(text = "Requested by {message_author}".format(message_author = ctx.message.author))
    await ctx.send(embed = embed)

    # Reset the collections_list, otherwise it would accumulate empty items over time
    collections_list = list(listdir_nohidden(picture_dir))

@bot.command()
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
    embed = discord.Embed(title = "Information", description = "I'm a bot made by Flipp3rrr#6969. I got various picture related commands and some other fun commands! Find out more about my commands with `{prefix}help`".format(prefix = bot_prefix))
    embed.add_field(name = "Invite", value = bot_invite, inline = True)
    embed.add_field(name = "GitHub", value = github_link, inline = True)
    embed.set_footer(text = "Requested by {message_author}".format(message_author = ctx.message.author))
    await ctx.send(embed = embed)

bot.run(token)