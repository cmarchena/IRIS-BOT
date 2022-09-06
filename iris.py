# This example requires the 'message_content' intent.

import discord
from discord import app_commands
from chapter_downloader import download_new_chapters, list_files
from chapter_sender import send_chapter_to_bot
from discord.ext.commands import Bot

from typing import Optional


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        await self.tree.sync()


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

@client.tree.command()
async def download(interaction: discord.Interaction):
    """Downloads new chapters"""
    await interaction.response.send_message(f'Checking for new chapters...')
    downloaded = download_new_chapters()
    if len(downloaded) > 0:
        await interaction.followup.send(f'Downloaded {len(downloaded)} new chapters: {downloaded}')
    else:
        await interaction.followup.send(f'No new chapters found')

@client.tree.command()
async def find(interaction: discord.Interaction):
    """Lists all chapters"""
    await interaction.response.send_message(f'Searching for chapters...')
    chapters = list_files("scripts")
    await interaction.followup.send(f'Found {len(chapters)} chapters')

@client.tree.command()
@app_commands.describe(
    book_name='Name of book. Eg. endless_summer',
    book_number='Number of book. In case of standalones, write 1. Eg. 1',
    chapter_number='Number of chapter. Eg. 01, 12, etc.'
)
async def send_chapter(interaction: discord.Interaction, book_name: str, book_number: int, chapter_number: str):
    """Sends a chapter"""
    await interaction.response.send_message(f'Sending {book_name} {book_number} chapter {chapter_number}...')
    chapter = send_chapter_to_bot(book_name, str(book_number), chapter_number)
    if chapter == "No chapter found":
        await interaction.followup.send(f'No chapter found')
    else:
        #send chapter as attachment
        await interaction.followup.send(file=discord.File(chapter, f'{book_name}_{book_number}_chapter_{chapter_number}.txt'))


# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@client.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='Text to send in the current channel')
async def send(interaction: discord.Interaction, text_to_send: str):
    """Sends the text into the current channel."""
    await interaction.response.send_message(text_to_send)


# To make an argument optional, you can either give it a supported default argument
# or you can mark it as Optional from the typing standard library. This example does both.
@client.tree.command()
@app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    """Says when a member joined."""
    # If no member is explicitly provided then we use the command user here
    member = member or interaction.user

    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')


# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.

# This context menu command only works on members
@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')


# This context menu command only works on messages
@client.tree.context_menu(name='Report to Moderators')
async def report_message(interaction: discord.Interaction, message: discord.Message):
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(
        f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
    )

    # Handle report by sending it into a log channel
    log_channel = interaction.guild.get_channel(0)  # replace with your channel id

    embed = discord.Embed(title='Reported Message')
    if message.content:
        embed.description = message.content

    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at

    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

    await log_channel.send(embed=embed, view=url_view)


client.run('Nzk1Njc2NjIyNjk4OTcxMTc3.Gkw6IS.X8VMxSvAuwDFBji4jJ7ilwPgN5bs3OT1KFgC2k')