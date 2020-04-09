from discord.ext import commands
import discord
import praw
import json
import asyncio
from utils.checks import reddit_mod_check
from functools import partial
from datetime import datetime
import os


class RedditMod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.subreddit = self.client.config["subreddit"]

    async def get_rules_from_subreddit(self):
        """Retrieves the rules of the subreddit."""
        pass

    async def remove_submission(self, submission: praw.Reddit.submission, message):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, submission.mod.remove)
        reply = f'Your post has been removed.\n\n>{message}\n\n*If you think this is a mistake, you can [message the moderators](https://www.reddit.com/message/compose?to=%2Fr%2F{self.subreddit["name"]}).*'
        comment = await loop.run_in_executor(None, submission.reply, reply)
        comment.mod.distinguish(how="yes", sticky=True)
        time_created = datetime.utcfromtimestamp(submission.created_utc)
        return f"```Post removed.\nTime since post creation: {datetime.utcnow()-time_created}```"

    async def approve_submission(self, url):
        loop = asyncio.get_event_loop()
        reddit = await loop.run_in_executor(None, partial(praw.Reddit, **self.client.config["reddit"]))
        submission = await loop.run_in_executor(None, partial(reddit.submission, url=url))
        await loop.run_in_executor(None, submission.mod.approve)
        async for c in submission.comments:
            if c.author == self.client.config["reddit"]["username"]:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, c.mod.remove)
        return "```Post approved.```"

    @commands.command()
    @commands.check(reddit_mod_check)
    async def remove(self, ctx, url, reason):
        """Remove a post on Reddit from the subreddit. Usage: `+remove {url} {reason}`"""
        loop = asyncio.get_event_loop()
        reddit = await loop.run_in_executor(None, partial(praw.Reddit, **self.client.config["reddit"]))
        submission = await loop.run_in_executor(None, partial(reddit.submission, url=url))
        if submission.subreddit.display_name.lower() != self.subreddit["name"].lower():
            return f'```Invalid subreddit.\nThe post must be from {self.client.config["subreddit"]["name"]} to be removed, but it seems like the provided url pointed me to {submission.subreddit.display_name}.```'
        else:
            pass

    @commands.command()
    @commands.check(reddit_mod_check)
    async def approve(self, ctx, url):
        """Approve a post on Reddit from the subreddit. Usage: `+approve {url}`"""
        await ctx.trigger_typing()
        reply = await self.approve_submission(url)
        await ctx.send(reply)


def setup(client):
    client.add_cog(RedditMod(client))
