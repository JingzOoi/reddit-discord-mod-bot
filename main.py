from discord.ext import commands
import json
import os
from utils.checks import owner_check
import asyncio
import praw
from functools import partial

client = commands.Bot(command_prefix=commands.when_mentioned_or("-"))


with open("resources\\settings.json", "r") as f:
    client.config = json.load(f)


@client.event
async def on_ready():
    print(f"Logged in as: {client.user.name}")


@client.event
async def on_command(ctx):
    print(f"\n@{ctx.author.name}#{ctx.author.discriminator} in #{ctx.channel.name} ({ctx.guild.name}):\n{ctx.message.content}")


@client.event
async def on_command_error(ctx, error):
    await ctx.send(f"```An error has occured: {error}```")


@commands.check(owner_check)
@client.command()
async def setup(ctx):
    await ctx.send("```Would you like to perform setup for the bot? (y/N)\nNote: This action will override your current settings and cannot be undone.```")
    msg = await client.wait_for("message", check=lambda m: (m.content.lower() in ("y", "n")) and m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
    if not msg or msg.content.lower() == "n":
        return await ctx.send("```Setup not completed. Exiting.```")
    elif msg.content.lower() == "y":
        await ctx.send("```Starting setup session. Use the keyword 'exit' to exit the setup.```")
        await ctx.send("```Nice to meet you. Please tell me the Reddit username that I can use to moderate a subreddit.```")
        reddit_username = await client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
        if not reddit_username or reddit_username.content.lower() == "exit":
            return await ctx.send("```Setup not completed. Exiting.```")
        else:
            reddit_username.content.strip("u/")
            await ctx.send(f"```Great. I'm /u/{reddit_username.content} on Reddit. \nBy the way, logic dictates that my Reddit account should be set as a moderator on the subreddit I'm supposed to moderate, okay?\nWhat's my password?```")
            reddit_password = await client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
            if not reddit_password or reddit_password.content.lower() == "exit":
                return await ctx.send("```Setup not completed. Exiting.```")
            if reddit_password:
                await ctx.send(f"```Right. If you did create an application with that account, you should have a client ID and client secret on hand. Mind telling me what the ID is first?```")
                reddit_client_id = await client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
                if not reddit_client_id or reddit_client_id.content.lower() == "exit":
                    return await ctx.send("```Setup not completed. Exiting.```")
                else:
                    await ctx.send(f"```And the client secret?```")
                    reddit_client_secret = await client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
                    if not reddit_client_secret or reddit_client_secret.content.lower() == "exit":
                        return await ctx.send("```Setup not completed. Exiting.```")
                    else:
                        await ctx.send("```Gotcha. We have completed the Reddit account setup. Please hold on while I test out the credentials.```")
                        client.config["reddit"] = {
                            "client_id": reddit_client_id,
                            "client_secret": reddit_client_secret,
                            "username": reddit_username,
                            "password": reddit_password,
                            "user_agent": "Developed by /u/JingzOoi"
                        }
                        loop = asyncio.get_event_loop()
                        reddit = await loop.run_in_executor(None, partial(praw.Reddit, **client.config["reddit"]))
                        if reddit:
                            await ctx.send("```It would seem like you did not make a mistake. That's great!```")
                        else:
                            return await ctx.send("```It would seem like you have made a mistake. You should do this again when you are more prepared.```")


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
