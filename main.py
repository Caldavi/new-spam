import re
import os
import asyncio
import random
import string
import discord
print(discord.__version__)
import time
import datetime
from discord.ext import commands, tasks

user_token = os.environ['token']
spam_id = os.environ['spam_id']
version = 'v2.3'
prefix = "."

P2Assistant = 854233015475109888
poketwo = 716390085896962058
Pokename = 874910942490677270
authorized_ids = [Pokename, poketwo, P2Assistant]
client = commands.Bot(command_prefix=prefix)
intervals = [3.6, 2.8, 3.0, 3.2, 3.4]

@client.event
async def on_ready():
    print(f'*'*30)
    print(f'Logged in as {client.user.name} ✅:')
    print(f'With ID: {client.user.id}')
    print(f'*'*30)
    print(f'Poketwo Auto Collection {version}')
    print(f'Created by PlayHard')
    print(f'*'*30)


# Define the background task
@tasks.loop(seconds=random.choice(intervals))
async def spam():
    channel = client.get_channel(int(spam_id))
    if channel is None:
        print(f"Could not find channel with ID {spam_id}")
        return

    # Generate a random message
    message_content = ''.join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 7) * 5)
    
    try:
        await channel.send(message_content)
    except discord.errors.HTTPException as e:
        if e.status == 429:  # Rate limit error
            print("Rate limit exceeded. Waiting and retrying...")
            await asyncio.sleep(5)
            await spam()  # Retry sending the message
        else:
            print(f"Error sending message: {e}. Retrying in 60 seconds...")
            await asyncio.sleep(60)
            await spam()  # Retry sending the message
    except discord.errors.DiscordServerError as e:
        print(f"Error sending message: {e}. Retrying in 60 seconds...")
        await asyncio.sleep(60)
        await spam_recursive(channel, message_content, 1)

async def spam_recursive(channel, message_content, attempt):
    """Handle retries with exponential backoff."""
    if attempt <= 3:  # Limit retries to 3 attempts
        try:
            await channel.send(message_content)
        except discord.errors.DiscordServerError as e:
            print(f"Attempt {attempt} failed. Error: {e}. Retrying in {60 * 2 ** (attempt - 1)} seconds...")
            await asyncio.sleep(60 * 2 ** (attempt - 1))  # Exponential backoff
            await spam_recursive(channel, message_content, attempt + 1)
    else:
        print("All attempts failed. Giving up.")

# This function will run before the spam task starts, ensuring the bot is ready
@spam.before_loop
async def before_spam():
    await client.wait_until_ready()

# This event runs when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    spam.start()  # Start the spam loop after the bot is ready
    
@client.command()
@commands.has_permissions(administrator=True)
async def start(ctx):
    spam.start()
    await ctx.send('Started Spammer!')
    print(f'Started Spammer! ✅:')

@client.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    spam.cancel()
    await ctx.send('Stopped Spammer!')
    print(f'Stopped Spammer! ✅:')
    
