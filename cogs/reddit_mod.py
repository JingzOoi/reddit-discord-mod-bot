import discord
from discord.ext import commands
from utils.construct import construct_path, blockify
import asyncpraw
from datetime import datetime
from utils.checks import owner_check, reddit_mod_check
from utils.SimplePaginator import SimplePaginator
import aiohttp


class RedditMod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit_instance = asyncpraw.Reddit(**self.client.config["reddit"])
        self.subreddit_config = self.client.config["subreddit"]
        # self.rules_path = construct_path("settings", "rules.json") # deprecate if can read directly from rules page

    async def _get_subreddit(self, subreddit_name):
        return await self.reddit_instance.subreddit(subreddit_name)

    async def _init_subreddit(self):
        self.subreddit_instance = await self.reddit_instance.subreddit(self.subreddit_config["subreddit"])
        return self.subreddit_instance

    async def _get_submission(self, submission_link):
        return await self.reddit_instance.submission(url=submission_link)

    # read rules from sub

    @commands.command()
    @commands.check(reddit_mod_check)
    async def rules(self, ctx, num: int = 0):
        """Read rules from the subreddit. Specify a number to read a more detailed version."""
        await ctx.trigger_typing()
        reply_str = ""
        actual_num = num - 1
        subreddit = await self._get_subreddit(self.subreddit_config["name"])
        if actual_num < 0:
            async for rule in subreddit.rules:
                reply_str += f"{rule.priority+1}: {rule.short_name}\n"
        else:
            rule = await subreddit.rules.get_rule(actual_num)
            if rule:
                reply_str += f"Rule {num}: {rule.short_name}\n{rule.description}"
        return await ctx.reply(blockify(reply_str))

    # update rules (on subreddit) # cancel if able to read directly from rules page

    # update rules (locally) # cancel if able to read directly from rules page

    # preview post details
    @commands.command(aliases=["submission"])
    @commands.check(reddit_mod_check)
    async def preview(self, ctx, url):
        """Peek into a Reddit submission."""
        await ctx.trigger_typing()
        submission = await self._get_submission(url)
        await submission.subreddit.load()
        em = discord.Embed(
            url=url,
            color=0xff6600
        )
        em.add_field(name="Title", value=submission.title)
        em.add_field(name="Subreddit", value=submission.subreddit.display_name)
        em.add_field(name="Author", value=f"{submission.author.name}")
        em.add_field(name="Posted", value=f"{datetime.utcfromtimestamp(submission.created_utc).strftime('%d-%m-%Y %X')}")
        em.add_field(name="Score", value=submission.score)
        em.add_field(name="Comments", value=submission.num_comments)
        em.add_field(name="Flair", value=submission.link_flair_text)
        em.add_field(name="Text Post?", value=submission.is_self)
        em.add_field(name="Locked?", value=submission.locked)
        if not submission.is_self:
            em.set_thumbnail(url=submission.url)
        em.add_field(name="Distinguished?", value=submission.distinguished)
        em.add_field(name="Shortlink", value=submission.shortlink)

        return await ctx.reply(embed=em)

    # remove post

    @commands.command(aliases=["removepost"])
    @commands.check(reddit_mod_check)
    async def remove(self, ctx, url, reason: str = None, *args):
        """Remove a submission."""
        await ctx.trigger_typing()
        submission = await self._get_submission(url)
        await submission.subreddit.load()
        assert submission.subreddit.display_name == self.subreddit_config[
            "name"], f'Submission is in /r/{submission.subreddit.display_name}, not /r/{self.subreddit_config["name"]}'
        if reason is None:
            message = None
        elif reason.lower() in ("faq"):
            message = f'You seem to be asking for a certain information that is available on the [**FAQ page**](https://www.reddit.com/r/{self.subreddit_config["name"]}/wiki/faq) or an information that is easily available by looking around the subreddit. You are recommended to check the sidebar, the announcements and the pinned posts before making an enquiry post.'
        elif reason.lower() in ("answered", "a"):
            message = "Your post seems to contain a question that has been answered."
        elif reason.lower() in ("repost"):
            if args:
                message = f"This is a repost: {args[0]}"
            else:
                message = "This is a repost."
        elif reason in ("reason", "message"):
            if args:
                message = " ".join(args)
            else:
                return await ctx.reply(blockify("Reason not recognized. Post removal cancelled."))
        else:
            try:
                rule_num = int(reason)
                actual_rule_num = rule_num - 1
                actual_rule = await submission.subreddit.rules.get_rule(actual_rule_num)
                message = f"**Rule {rule_num}: {actual_rule.short_name}**\n{actual_rule.description}"
            except TypeError:
                return await ctx.reply(blockify("Reason not recognized. Post removal cancelled."))
            except IndexError:
                return await ctx.reply(blockify("Rule does not exist. Might want to check with the 'rules' command or the subreddit rules configuration."))

        await submission.mod.remove()

        if message:
            await submission.mod.send_removal_message(f'This post has been removed for:\n\n>{message}\n\n*If you think this is a mistake, you can [message the moderators](https://www.reddit.com/message/compose/?to=/r/{self.subreddit_config["name"]}).*')

        return await ctx.reply(blockify(f"Post removed. \nTime since post creation: {datetime.utcnow()-datetime.utcfromtimestamp(submission.created_utc)}"))

    # approve post

    @commands.command(aliases=["approvepost"])
    @commands.check(reddit_mod_check)
    async def approve(self, ctx, url):
        """Approve a submission."""
        await ctx.trigger_typing()
        submission = await self._get_submission(url)
        await submission.subreddit.load()
        assert submission.subreddit.display_name == self.subreddit_config[
            "name"], f'Submission is in /r/{submission.subreddit.display_name}, not /r/{self.subreddit_config["name"]}'

        comments = await submission.comments()
        await comments.replace_more(limit=0)
        for top_level_comment in comments:
            if top_level_comment.author.name == self.client.config["reddit"]["username"]:
                await top_level_comment.mod.remove()
        await submission.mod.approve()
        return await ctx.reply(blockify(f"Post approved."))

    # submit post

    # make announcement

    # remove announcement

    # leave reply

    # check reposts
    @commands.command()
    @commands.check(owner_check)
    async def repost(self, ctx, url):
        """Check for reposts of a piece of media in the same subreddit. Powered by RepostSleuth."""
        await ctx.trigger_typing()
        submission = await self._get_submission(url)
        parameters = {
            "filter": "true",
            "url": f"https://redd.it/{submission.id}",
            "postId": submission.id,
            "same_sub": "true",
            "filter_author": "false",
            "only_older": "false",
            "include_crossposts": "false",
            "meme_filter": "false",
            "target_match_percent": 90,
            "filter_dead_matches": "false",
            "target_days_old": "0"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.repostsleuth.com/image", params=parameters) as page:
                assert page.status == 200, f"Request made about submission returned status code {page.status}."
                resp = await page.json()

                if resp:
                    try:
                        match_details = resp["closest_match"]["post"]

                        em = discord.Embed(
                            title=f'{match_details["title"]}',
                            url=match_details["url"],
                            description=f'[Comments](https://redd.it/{match_details["post_id"]})',
                            color=0xff6600
                        )
                        em.set_image(url=match_details["url"])
                        em.set_author(name=f'Showing closest match out of {len(resp["matches"])} match results.')
                        em.set_footer(text=f'Post by: /u/{match_details["author"]}')
                        return await ctx.send(embed=em)
                    except KeyError:
                        return await ctx.send(blockify("No close matches found."))

    # check recent posts

    # check modmail
    @commands.command(aliases=["mm"])
    @commands.check(reddit_mod_check)
    async def modmail(self, ctx, mode: str = "unread", *args):
        """Provides a preview of modmail. Currently no plans to have reply function, only preview."""
        MODE_OPTIONS = ("unread", "new", "readall")
        await ctx.trigger_typing()
        subreddit = await self._get_subreddit(self.subreddit_config["name"])
        if mode.lower() not in MODE_OPTIONS:
            return await ctx.reply(blockify(f"Mode not recognized. Currently supported modes: {MODE_OPTIONS}"))
        else:
            if mode.lower() in ("unread", "new"):
                embed_list = []
                inbox = [message async for message in subreddit.mod.unread(limit=10)]
                for index, message in enumerate(inbox, start=1):
                    date_created = datetime.utcfromtimestamp(message.created_utc)
                    if (datetime.utcnow() - date_created).days > 31:
                        break
                    em = discord.Embed(
                        title=f"Showing unread modmail {index}/{len(inbox)} from /r/{subreddit.display_name}",
                        description=f"[Check inbox](https://mod.reddit.com/mail/inbox)",
                        color=0xff6600,

                    )
                    em.add_field(name="Sent by", value=message.author.name)
                    em.add_field(name="Datetime (UTC)", value=date_created.strftime('%d-%m-%Y %X'))
                    em.add_field(name="Subject", value=f"{message.subject[:50]}{'...' if len(message.subject)>=50 else ''}", inline=False)
                    em.add_field(name="Content", value=f"{message.body[:300]}{'...' if len(message.body)>=300 else ''}", inline=False)
                    # em.set_thumbnail(url=message.author.icon_img)
                    embed_list.append(em)
                if len(embed_list) > 1:
                    return await SimplePaginator(extras=embed_list).paginate(ctx)
                elif len(embed_list) == 1:
                    return await ctx.reply(embed=embed_list[0])
                else:
                    return await ctx.reply(embed=discord.Embed(
                        title=f"No unread modmail!",
                        description=f"[Check inbox](https://mod.reddit.com/mail/inbox)",
                        color=0xff6600,
                    ))
            elif mode.lower() in ("readall"):
                inbox = [message async for message in subreddit.mod.unread(limit=20)]
                for message in inbox:
                    await message.mark_read()
                return await ctx.send(blockify("Marked all inbox items as read."))

    # check modqueue

    # @commands.command(aliases=["mq"])
    # @commands.check(reddit_mod_check)
    # async def modqueue(self, ctx):
    #     await ctx.trigger_typing()
    #     subreddit = await self._get_subreddit(self.subreddit_config["name"])
    #     # queue = await subreddit.mod.modqueue()
    #     queue_str = ""
    #     async for item in subreddit.mod.modqueue():
    #         queue_str += str(type(item))
    #     return await ctx.reply(blockify(queue_str))

    # lock submission

    # lock subreddit


def setup(client):
    client.add_cog(RedditMod(client))
