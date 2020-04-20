from discord.ext import commands
import discord
import praw
import json
import asyncio
from utils.checks import reddit_mod_check, owner_check
from utils.construct import construct_path, blockify
from functools import partial
from datetime import datetime
import os


class RedditMod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.subreddit = self.client.config["subreddit"]
        self.rules_path = construct_path("resources", "rules.json")

    async def get_reddit(self) -> praw.Reddit:
        loop = asyncio.get_event_loop()
        reddit = await loop.run_in_executor(None, partial(praw.Reddit, **self.client.config["reddit"]))
        return reddit

    async def get_submission(self, url) -> praw.Reddit.submission:
        reddit = await self.get_reddit()
        loop = asyncio.get_event_loop()
        submission = await loop.run_in_executor(None, partial(reddit.submission, url=url))
        return submission

    def is_approved_subreddit(self, submission: praw.reddit.Submission) -> bool:
        return False if submission.subreddit.display_name.lower() != self.subreddit["name"].lower() else True

    def load_rules(self) -> dict:
        with open(self.rules_path, "r") as f:
            rules = json.load(f)
        return rules

    def read_rules(self, num: str = None):
        rules = self.load_rules()
        if num in rules:
            rule = f'Rule {num}: {rules[num]["desc"]}'
        elif num is None:
            rule = f'Subreddit Rules for /r/{self.subreddit["name"]}'
            for r in rules:
                rule += f'\n{r}: {rules[r]["name"]}'
        else:
            rule = "Invalid Rule Number."

        return rule

    async def get_rules_from_subreddit(self):
        """Retrieves the rules of the subreddit."""
        loop = asyncio.get_event_loop()
        reddit = await self.get_reddit()
        subreddit = await loop.run_in_executor(None, reddit.subreddit, self.subreddit["name"])
        rules = subreddit.rules()["rules"]
        rules_simplified = {}

        for num, rule in enumerate(rules, start=1):
            rules_simplified[str(num)] = {
                "name": rule["short_name"],
                "desc": rule["description"]
            }

        with open(self.rules_path, "w") as f:
            f.write(json.dumps(rules_simplified, indent=4))

        return "```Updated rules.json.```"

    @commands.command()
    @commands.check(owner_check)
    async def updaterules(self, ctx):
        """Retrieves the rules from the subreddit and replaces resources\\rules.json."""
        await ctx.trigger_typing()
        reply = await self.get_rules_from_subreddit()
        return await ctx.send(reply)

    @commands.command()
    @commands.check(owner_check)
    async def now(self, ctx):
        """Sends a copy of the bot's settings for debugging purposes."""
        settings = {key: self.client.config[key] for key in self.client.config}
        for key in settings:
            for subkey in settings[key]:
                if subkey in ("password", "token", "client_id", "client_secret"):
                    settings[key][subkey] = "[REDACTED]"
        return await ctx.send(f"```json\n{json.dumps(settings, indent=4)}\n```")

    async def remove_submission(self, submission: praw.Reddit.submission, message: str = None):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, submission.mod.remove)
        if message is not None:
            reply = f'Your post has been removed.\n\n>{message}\n\n*If you think this is a mistake, you can [message the moderators](https://www.reddit.com/message/compose?to=%2Fr%2F{self.subreddit["name"]}).*'
            comment = await loop.run_in_executor(None, submission.reply, reply)
            comment.mod.distinguish(how="yes", sticky=True)
        time_created = datetime.utcfromtimestamp(submission.created_utc)
        return f"```Post removed.\nTime since post creation: {datetime.utcnow()-time_created}```"

    async def approve_submission(self, submission: praw.Reddit.submission):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, submission.mod.approve)
        for c in submission.comments.list():
            if c.author == self.client.config["reddit"]["username"]:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, c.mod.remove)
        return "```Post approved.```"

    @commands.command(aliases=["removepost"])
    @commands.check(reddit_mod_check)
    async def remove(self, ctx, url, reason: str = None):
        """Remove a post on Reddit from the subreddit. Usage: `--remove {url} {reason}`"""
        await ctx.trigger_typing()
        submission = await self.get_submission(url)
        if not self.is_approved_subreddit(submission):
            return await ctx.send(f'```Invalid subreddit.\nThe post must be from /r/{self.subreddit["name"]} to be removed, but it seems like the provided url pointed me to /r/{submission.subreddit.display_name}.```')
        else:
            if reason is None:
                message = None
            elif reason.lower() in ("pinned", "faq"):
                message = "You seem to be asking for a certain information that is available on a pinned post, or an information that is easily available by looking around. You are recommended to check the sidebar, the announcements, or the FAQ before making an enquiry post. The removal is to reduce redundancy on the subreddit."
            elif reason.lower() in ("answered", "a"):
                message = "Your post seems to contain a question that has been answered. The removal is to reduce redundancy on the subreddit."
            elif reason in self.load_rules().keys():
                message = self.read_rules(reason)
            else:
                return await ctx.send("```Reason not recognized. Post removal failed.```")

            reply = await self.remove_submission(submission, message)
            return await ctx.send(reply)

    @commands.command(aliases=["approvepost"])
    @commands.check(reddit_mod_check)
    async def approve(self, ctx, url):
        """Approve a post on Reddit from the subreddit. Usage: `--approve {url}`"""
        await ctx.trigger_typing()
        submission = await self.get_submission(url)
        if not self.is_approved_subreddit(submission):
            return await ctx.send(f'```Invalid subreddit.\nThe post must be from /r/{self.subreddit["name"]} to be approved, but it seems like the provided url pointed me to /r/{submission.subreddit.display_name}.```')
        else:
            reply = await self.approve_submission(submission)
            return await ctx.send(reply)

    @commands.command(aliases=["subrules"])
    @commands.check(reddit_mod_check)
    async def rules(self, ctx, num: str = None):
        """Sends a copy of the subreddit rules."""
        await ctx.trigger_typing()
        reply = self.read_rules(num)
        return await ctx.send(blockify(reply))


def setup(client):
    client.add_cog(RedditMod(client))
