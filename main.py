import random, discord
from discord import app_commands
from facts import facts, noises

MY_GUILD = discord.Object(id=1148819928158310471)

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
    game = discord.Game("with GOD")
    await client.change_presence(status=discord.Status.online, activity=game)
    print('------')


@client.tree.command()
async def fact(interaction: discord.Interaction):
    """Says a random rat fact"""
    await interaction.response.send_message(random.choice(facts), ephemeral=True)

client.run('MTE0ODgyMDI0MDQ5MTM0ODA0OA.GLsFe_.RXmQHe_t7PFMwnY32ZVww1G-paqgGJ7WxM4Ylc')