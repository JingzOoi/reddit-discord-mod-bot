from discord.ext import commands
import discord
import praw
import json
import asyncio
from utils.checks import owner_check
from utils.construct import construct_path
from functools import partial


class RedditSetup(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.settings_path = construct_path("resources, settings.json")

    def save_config(self):
        with open(self.settings_path, "w") as f:
            f.write(json.dumps(self.client.config, indent=4))

    async def reddit_user_setup(self, ctx):
        await ctx.send("```Would you like to perform user setup for the bot? (y/N)\nNote: This action will override your current settings and cannot be undone.```")
        msg = await self.client.wait_for("message", check=lambda m: (m.content.lower() in ("y", "n")) and m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
        if not msg or msg.content.lower() == "n":
            return await ctx.send("```Setup not completed. Exiting.```")
        elif msg.content.lower() == "y":
            await ctx.send("```Starting setup session. Use the keyword 'exit' to exit the setup.```")
            await ctx.send("```Nice to meet you. Please tell me the Reddit username that I can use to moderate a subreddit.```")
            reddit_username = await self.client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
            if not reddit_username or reddit_username.content.lower() == "exit":
                return await ctx.send("```Setup not completed. Exiting.```")
            else:
                reddit_username.content.strip("u/")
                await ctx.send(f"```Great. I'm /u/{reddit_username.content} on Reddit. (By the way, logic dictates that my Reddit account should be set as a moderator on the subreddit I'm supposed to moderate, okay?) What's my password?```")
                reddit_password = await self.client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
                if not reddit_password or reddit_password.content.lower() == "exit":
                    return await ctx.send("```Setup not completed. Exiting.```")
                if reddit_password:
                    await ctx.send(f"```Right. If you did create an application with that account, you should have a client ID and client secret on hand. Mind telling me what the ID is first?```")
                    reddit_client_id = await self.client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
                    if not reddit_client_id or reddit_client_id.content.lower() == "exit":
                        return await ctx.send("```Setup not completed. Exiting.```")
                    else:
                        await ctx.send(f"```And the client secret?```")
                        reddit_client_secret = await self.client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
                        if not reddit_client_secret or reddit_client_secret.content.lower() == "exit":
                            return await ctx.send("```Setup not completed. Exiting.```")
                        else:
                            await ctx.send("```Gotcha. We have completed the Reddit account setup. Let me save the settings.```")
                            self.client.config["reddit"] = {
                                "client_id": reddit_client_id.content,
                                "client_secret": reddit_client_secret.content,
                                "username": reddit_username.content,
                                "password": reddit_password.content,
                                "user_agent": "Developed by /u/JingzOoi"
                            }
                            self.save_config()
                            return await ctx.send("```Saved user settings.```")

    async def subreddit_setup(self, ctx):
        await ctx.send("```Would you like to perform subreddit setup for the bot? (y/N)\nNote: This action will override your current settings and cannot be undone.```")
        msg = await self.client.wait_for("message", check=lambda m: (m.content.lower() in ("y", "n")) and m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
        if not msg or msg.content.lower() == "n":
            return await ctx.send("```Setup not completed. Exiting.```")
        elif msg.content.lower() == "y":
            await ctx.send("```Starting setup session. Use the keyword 'exit' to exit the setup.```")
            await ctx.send("```Welcome back. Please tell me the subreddit that I am assigned to.```")
            subreddit_name = await self.client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
            if not subreddit_name or subreddit_name.content.lower() == "exit":
                return await ctx.send("```Setup not completed. Exiting.```")
            else:
                await ctx.send("```I see. Please hold on while I verify that I was given the permissions to mod the subreddit.```")
                loop = asyncio.get_event_loop()
                reddit = await loop.run_in_executor(None, partial(praw.Reddit, **self.client.config["reddit"]))
                try:
                    subreddit = await loop.run_in_executor(None, reddit.subreddit, subreddit_name.content.lower())
                    if subreddit.user_is_moderator is True:
                        self.client.config["subreddit"]["name"] = subreddit_name.content
                        self.save_config()
                        await ctx.send(f"```It would seem like the Reddit account I can access is indeed a moderator of /r/{subreddit_name.content}.```")
                        subreddit_mods = []
                        await ctx.send(f"```Somebody should be able to give me commands to remove or approve posts. Would you like to list yourself as one of the controllers? (y/N)```")
                        msg = await self.client.wait_for("message", check=lambda m: (m.content.lower() in ("y", "n")) and m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=30)
                        if msg.content.lower() == "y":
                            subreddit_mods.append(ctx.author.id)
                        elif not msg or msg.content.lower() == "n":
                            await ctx.send("```So I'll ignore you when you try to use Reddit mod commands. Got it.```")
                        await ctx.send("```You should also tell me who else can use my Reddit mod commands. Just tell me their Discord user IDs in one message, separated with a comma (,) each. You have about 90 seconds. If you don't want more, then reply with 'None'.```")
                        sub_mods = await self.client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=90)
                        if sub_mods.content.lower() in ("none"):
                            await ctx.send("```So I listen to no one else.```")
                        else:
                            await ctx.send("```Let's see...```")
                            s_mods = [int(sub_mod.strip()) for sub_mod in sub_mods.content.split(",")]
                            subreddit_mods = subreddit_mods + s_mods
                        self.client.config["subreddit"]["mods"] = subreddit_mods
                        self.save_config()
                        return await ctx.send("```We've reached the end of the setup. Before trying to mod, you should try populating my database using the '--updaterules' command.```")
                    else:
                        return await ctx.send(f'```It doesn\'t seem like this account (/u/{self.client.config["reddit"]["username"]}) is allowed to mod the subreddit (/r/{subreddit_name.content}). Please do something about it and try again.```')
                except praw.exceptions.APIException:
                    return await ctx.send("```Uh oh. Seems like something is not right. Check if everything is in place and try again.```")

    @commands.check(owner_check)
    @commands.command()
    async def setup(self, ctx, option: str = None):
        """Set up Reddit settings and/or subreddit settings. Usage: `--setup {option (Optional)}`"""
        if option is None:
            user_setup = await self.reddit_user_setup(ctx)
            if user_setup:
                if not (self.client.config["reddit"]["username"] == "" or self.client.config["reddit"]["password"] == "" or self.client.config["reddit"]["client_id"] == "" or self.client.config["reddit"]["client_secret"] == ""):
                    await self.subreddit_setup(ctx)
        elif option.lower() in ("-r", "--reddit"):
            await self.reddit_user_setup(ctx)
        elif option.lower() in ("-s", "--subreddit"):
            if self.client.config["reddit"]["username"] == "" or self.client.config["reddit"]["password"] == "" or self.client.config["reddit"]["client_id"] == "" or self.client.config["reddit"]["client_secret"] == "":
                return await ctx.send("```It doesn't seem like you have set up the Reddit user settings. Might I recommend you to try out the '--setup' command?```")
            else:
                await self.subreddit_setup(ctx)


def setup(client):
    client.add_cog(RedditSetup(client))
