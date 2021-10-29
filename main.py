# mushroom-bot, a Discord bot written in Python
#
# pylint configuration
# pylint: disable=C0116, C0325, R0914, R1705, R1732, W0621, W0622

import os
import json
import random
import pathlib
import typing
import re
import discord                   # pylint: disable=E0401
from discord.ext import commands # pylint: disable=E0401

run_dir = os.path.dirname(__file__)

# Settings are saved in 'settings.json', settings are saved in a dictionary. This function gets the
# value of a key specified ('name').
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
            new_value = input(f"{purpose}: ")
            new_dict = {f"{new_key}": f"{new_value}"}

            settings.update(new_dict)
            settings_file = open(settings_file_path, "w+")
            json.dump(settings, settings_file, indent = 4)

            return_value = settings[name]
            return(return_value)

    else:
        new_key = name
        new_value = input(f"{purpose}: ")
        new_dict = {f"{new_key}": f"{new_value}"}

        settings = new_dict
        settings_file = open(settings_file_path, "w+")
        json.dump(settings, settings_file, indent = 4)

        return_value = settings[name]
        return(return_value)

# Thanks to StackOverflow
# https://stackoverflow.com/questions/7099290/how-to-ignore-hidden-files-using-os-listdir
def listdir_nohidden(path):
    for filename in os.listdir(path):
        if not filename.startswith('.'):
            yield filename

picture_dir = os.path.join(run_dir, "pictures")
collections_list = list(listdir_nohidden(picture_dir))
bot_token = get_setting("bot_token")
bot_prefix = get_setting("bot_prefix")
bot_invite = get_setting("bot_invite")
github_link = get_setting("github_link")
discord_server = get_setting("discord_server")

intents = discord.Intents.default()
intents.members = True

member_cache_flags = discord.MemberCacheFlags.from_intents(intents)

bot = commands.Bot(command_prefix = bot_prefix, intents = intents,
    member_cache_flags = member_cache_flags)
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    presence = discord.Game(f"do '{bot_prefix}help'")
    await bot.change_presence(status=discord.Status.idle, activity=presence)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_lowercase = message.content.lower()
    if message_lowercase.startswith("pretty"):
        # Reset the collections_list, otherwise it would accumulate empty items over time
        collections_list = list(listdir_nohidden(picture_dir))

        message_for_check_list = re.split("<", message_lowercase)
        message_for_check = message_for_check_list[0]
        message_for_check = message_for_check.strip()

        if message_for_check[-1] != "s" and len(message_for_check_list) != 1:
            message_edited = message_for_check + "s" + message_for_check_list[1]

        elif message_for_check[-1] != "s" and len(message_for_check_list) == 1:
            message_edited = message_for_check + "s"

        else:
            message_edited = message_lowercase

        for collection in collections_list:
            if collection in message_edited:
                collection_dir = pathlib.Path(picture_dir) / collection

                jpegs = list(collection_dir.glob("**/*.jpg"))
                choice = random.choice(jpegs)
                author = bot.get_user(choice.parent.name)
                if author is None:
                    author = await bot.fetch_user(choice.parent.name)

                message_split = re.split("@!", message_lowercase)
                message_split_length = len(message_split)

                if message_split_length != 1:
                    mention_id1 = message_split[message_split_length - 1]
                    mention_id = mention_id1[:-1]

                    embed = discord.Embed(title = f"{collection[:-1]} picture",
                        description = f"Hey <@!{mention_id}>, {message.author} gave you a pretty \
                        {collection[:-1]}!")
                    image = discord.File(choice, filename = choice.name)
                    embed.set_image(url = f"attachment://{choice.name}")
                    embed.set_footer(text = f"Image submitted by {author}")
                    await message.channel.send(file = image, embed = embed)

                else:
                    embed = discord.Embed(title = f"{collection[:-1]} picture")
                    image = discord.File(choice, filename = choice.name)
                    embed.set_image(url = f"attachment://{choice.name}")
                    embed.set_footer(text = f"Image submitted by {author}")
                    await message.channel.send(file = image, embed = embed)

    await bot.process_commands(message)

@bot.command()
async def help(ctx, command: typing.Optional[str] = "default_help"):
    if command == "default_help":
        embed = discord.Embed(title = "Help",
            description = f"My prefix is `{bot_prefix}`, get more informations on specific \
            commands with `{bot_prefix}help <command>`.")
        embed.add_field(name = "Commands", value = "* `collections`\n* `info`\n* `picture`")
        await ctx.send(embed = embed)

    elif command == "collections":
        embed = discord.Embed(title = "Help (collections)",
            description = "Sends a message containing a list of available collections.")
        embed.add_field(name = "Example", value = f"`{bot_prefix}collections`")
        await ctx.send(embed = embed)

    elif command == "info":
        embed = discord.Embed(title = "Help (info)",
            description = "Sends a message containing relevant information to the bot.")
        embed.add_field(name = "Example", value = f"`{bot_prefix}info`")
        await ctx.send(embed = embed)

    elif command == "picture":
        embed = discord.Embed(title = "Help (picture)",
            description = "Sends a random image from the specified collection.")
        embed.add_field(name = "Example", value = f"`{bot_prefix}picture <collection>`",
            inline = True)
        embed.add_field(name = "Example 2", value = "`pretty <collection>`", inline = True)
        await ctx.send(embed = embed)

@bot.command()
async def collections(ctx):
    # Reset the collections_list, otherwise it would accumulate empty items over time
    collections_list = list(listdir_nohidden(picture_dir))
    collections_list.sort()
    # Insert empty item into the list to fix the formatting
    collections_list.insert(0, "")
    # Remove z.misc folder, since you can't acces it with the 'picture' command
    del collections_list[-1]

    pretty_list = "\n * ".join(collections_list)

    embed = discord.Embed(title = "Collections",
        description = f"Collections can be specified with or without the 's' at the end.\n \
        {pretty_list}")
    await ctx.send(embed = embed)

@bot.command()
async def picture(ctx, collection:str, mention: typing.Optional[str] = "no_mention"):
    collection_lowercase = collection.lower()
    if collection_lowercase[-1] != "s":
        collection_lowercase = collection_lowercase + "s"

    collection_dir = pathlib.Path(picture_dir) / collection_lowercase

    jpegs = list(collection_dir.glob("**/*.jpg"))
    choice = random.choice(jpegs)
    author = bot.get_user(choice.parent.name)

    if author is None:
        author = await bot.fetch_user(choice.parent.name)

    if mention != "no_mention":
        embed = discord.Embed(title = f"{collection[:-1]}", description = f"Hey {mention}, \
            {ctx.message.author} gave you a pretty {collection[:-1]}")
        image = discord.File(choice, filename = choice.name)
        embed.set_image(url = f"attachment://{choice.name}")
        embed.set_footer(text = f"Image submitted by {author}")

    else:
        embed = discord.Embed(title = f"{collection[:-1]} picture")
        image = discord.File(choice, filename = choice.name)
        embed.set_image(url = f"attachment://{choice.name}")
        embed.set_footer(text = f"Image submitted by {author}")

    await ctx.send(file = image, embed = embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title = "Information",
        description = f"I'm a bot made by Flipp3rrr#6969. I got various picture related commands \
        and some other fun commands! Find out more about my commands with `{bot_prefix}help`")
    embed.add_field(name = "Invite", value = bot_invite, inline = False)
    embed.add_field(name = "Discord Server", value = discord_server, inline = True)
    embed.add_field(name = "GitHub", value = github_link, inline = True)
    await ctx.send(embed = embed)

@bot.command()
async def stop(ctx):
    bot_author_id = get_setting("bot_author_id")
    if int(ctx.message.author.id) == int(bot_author_id):
        await ctx.send("Stopping bot...")
        await bot.logout()
    else:
        await ctx.send(f"Invalid permissions! Your ID is `{ctx.message.author.id}`, the correct ID \
            is `{bot_author_id}`.")

bot.run(bot_token)
