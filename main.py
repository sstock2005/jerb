import random, discord, configparser, aiohttp, io, datetime, requests
from discord import app_commands
from data import facts, noises

config = configparser.ConfigParser()
config.readfp(open(r'config.txt'))

MY_GUILD = discord.Object(id=config.get("DEFAULT", "guild.id"))

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.all()
client = MyClient(intents=intents)

@client.event
async def on_message(message):
    if message.author == client:
        return
    if client.user.mentioned_in(message):
        await message.channel.send(random.choice(noises))

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    game = discord.Game("with the cat")
    await client.change_presence(status=discord.Status.online, activity=game)
    print('------')


@client.tree.command()
async def fact(interaction: discord.Interaction):
    """Says a random rat fact"""
    await interaction.response.send_message(random.choice(facts), ephemeral=True)

@client.tree.command()
async def cat(interaction: discord.Interaction):
    """Shows you a random cat image from https://sillycats.me"""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://sillycats.me/api/cat") as resp:
            img = await resp.read()
            with io.BytesIO(img) as file:
                file=discord.File(file, "cat.png")
                e = discord.Embed(title=requests.get("https://sillycats.me/api/noise").text, url="https://sillycats.me", color=0x07a9f3)
                e.set_image(url="attachment://cat.png")
                e.set_footer(text="Made by Sam Stockstrom", icon_url="https://avatars.githubusercontent.com/u/144393153")
                e.timestamp = datetime.datetime.utcnow()
                await interaction.response.send_message(file=file, embed=e)

@client.tree.command()
async def help(interaction: discord.Integration):
    """Shows you a list the commands"""
    e = discord.Embed(title="Commands", description="Fun fact, you can mention me for a response!", color=0x07a9f3)
    e.add_field(name="**/fact**", value="Says a random rat fact", inline=False)
    e.add_field(name="**/cat**", value="Shows you a random cat image from https://sillycats.me", inline=False)
    e.set_footer(text="Made by Sam Stockstrom", icon_url="https://avatars.githubusercontent.com/u/144393153")
    e.timestamp = datetime.datetime.now()
    await interaction.response.send_message(embed=e)

client.run(config.get("DEFAULT", "token"))