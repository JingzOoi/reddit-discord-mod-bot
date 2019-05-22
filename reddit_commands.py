import praw
import json
import re
from datetime import datetime

with open('resources\\token.json', 'r') as f:
    r_cred = json.load(f)["reddit"]

reddit = praw.Reddit(
    client_id=r_cred["client_id"],
    client_secret=r_cred["client_secret"],
    username=r_cred["username"],
    password=r_cred["password"],
    user_agent=f'/u/{r_cred["username"]}'
)

with open("resources\\subreddit.json", 'r') as f:
    subreddit_list = json.load(f)["subreddit"]


def read_rules(num="0"):
    with open('resources\\rules.json', 'r') as f:
        rules = json.load(f)

    if num == "0":
        ruleReply = "Subreddit Rules:\n"
        for rule in rules.keys():
            ruleReply += f'\n{rule}: {rules[rule]["name"]}'
        return f'```{ruleReply}```'
    elif num in rules.keys():
        return f'`{num}: {rules[num]["desc"]}`'
    else:
        return '`Invalid Rule Number.`'


def import_rules():
    subreddit = reddit.subreddit(subreddit_list[0])
    rules = {}
    for num, rule in enumerate(subreddit.rules()["rules"], start=1):
        rules[f'{num}'] = {
            "name": rule["short_name"],
            "desc": rule["description"]
        }

    with open('resources\\rules.json', 'w') as f:
        f.write(json.dumps(rules, indent=4))


def remove_submission(url, num):
    submission = reddit.submission(url=url)
    if submission.subreddit.display_name not in subreddit_list:
        return f"Invalid subreddit. Subreddit must be from one of the following: {subreddit_list}"
    with open("resources\\rules.json", "r") as f:
        rules = json.load(f)
    if num not in rules.keys():
        return "Invalid rule number."
    elif num == "0":
        submission.mod.remove()
        time_created = datetime.utcfromtimestamp(submission.created_utc)
        return f"Post removed.\nTime since post creation: {datetime.utcnow()-time_created}"
    else:
        message = f'Your post seems to have violated Rule {num}. As a result, it has been removed. \n\n>{read_rules(num=num)}\n\nYou can read the full rules in the sidebar.\n\nIf you think this is a mistake, you can [message the moderators](https://www.reddit.com/message/compose?to=%2Fr%2FKaguya_sama_css).'
        comment = submission.reply(message)
        comment.mod.distinguish(how="yes", sticky=True)
        submission.mod.remove()
        time_created = datetime.utcfromtimestamp(submission.created_utc)
        return f"Post removed.\nTime since post creation: {datetime.utcnow()-time_created}"


def approve_submission(url):
    submission = reddit.submission(url=url)
    submission.mod.approve()
    for c in submission.comments:
        if c.author == r_cred["username"]:
            c.mod.remove()
    return "Post approved."
