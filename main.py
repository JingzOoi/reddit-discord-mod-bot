from discord.ext import commands
import reddit_commands
import json

client = commands.Bot(command_prefix=commands.when_mentioned_or("-"))

with open('resources\\token.json', 'r') as f:
    d_cred = json.load(f)["discord"]
    token = d_cred["token"]

authorized_users = [
    '287949832814067722',
    '341319020974178316',
    '245249323049156609'
]


@client.event
async def on_ready():
    print(f"Logged in as: {client.user.name}")


@client.event
async def on_command_error(ctx, error):
    await ctx.send(error)


@client.command()
async def alive(ctx):
    await ctx.send('`:KaguyaSmug:`')


@client.command()
async def rules(ctx, num="0"):
    await ctx.send(reddit_commands.read_rules(num))


@client.command()
async def remove(ctx, url, num="0"):
    if str(ctx.author.id) not in authorized_users:
        await ctx.send("You are FORBIDDEN from doing that. **FORBIDDEN**")
    else:
        reply = reddit_commands.remove_submission(url, num=num)
        await ctx.send(reply)


@client.command()
async def approve(ctx, url):
    if str(ctx.author.id) not in authorized_users:
        await ctx.send("You are FORBIDDEN from doing that. **FORBIDDEN**")
    else:
        reply = reddit_commands.approve_submission(url)
        await ctx.send(reply)


client.run(token)
