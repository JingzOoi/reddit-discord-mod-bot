from discord.ext import commands
import json
import os

client = commands.Bot(command_prefix=commands.when_mentioned_or("--"))


with open("resources\\settings.json", "r") as f:
    client.config = json.load(f)


@client.event
async def on_ready():
    print(f"Logged in as: {client.user.name}")


@client.event
async def on_command(ctx):
    print(f"\n@{ctx.author.name}#{ctx.author.discriminator} in #{ctx.channel.name} ({ctx.guild.name}):\n{ctx.message.content}")


# @client.event
# async def on_command_error(ctx, error):
#     await ctx.send(f"```An error has occured: {error}```")


@client.command()
async def alive(ctx):
    return await ctx.send("```I'm here.```")


if __name__ == "__main__":
    for file in os.listdir('cogs'):
        if file.endswith('.py'):
            try:
                client.load_extension("cogs." + os.path.splitext(file)[0])
                print(f'Extension {file} loaded.')
            except Exception as e:
                print(f'Failed to load extension {file}: {e}')

    client.run(client.config["discord"]["token"])
