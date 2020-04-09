async def owner_check(ctx):
    return ctx.author.id == ctx.bot.config["discord"]["owner"]


async def reddit_mod_check(ctx):
    return ctx.author.id in ctx.bot.config["subreddit"]["mods"]
