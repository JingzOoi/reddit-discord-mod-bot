import praw
import json
from datetime import datetime

with open('resources\\token.json', 'r') as f:
    r_cred = json.load(f)["reddit"]

reddit = praw.Reddit(
    client_id=r_cred["client_id"],
    client_secret=r_cred["client_secret"],
    username=r_cred["username"],
    password=r_cred["password"],
    user_agent=f'/u/{r_cred["username"]} by /u/JingzOoi'
)

subreddit_list = [
    'Kaguya_sama_css'
]


def read_rules(num="0"):
    with open("resources\\rules.json", "r") as f:
        rules = json.load(f)
    ruleList = [str(i) for i in range(10)]
    if num not in ruleList:
        return "Invalid rule number."
    elif num == "0":
        r = 'Rules: '
        for rule, desc in zip(rules.keys(), rules.values()):
            r += f'\n{rule}: {desc}'
        return f'```{r}```'
    else:
        return rules[num]


def remove_submission(url, num):
    submission = reddit.submission(url=url)
    ruleList = [str(i) for i in range(10)]
    if num not in ruleList:
        return "Invalid rule number."
    elif num == "0":
        submission.mod.remove()
        time_created = datetime.utcfromtimestamp(submission.created_utc)
        return f"Post removed.\nTime since post creation: {datetime.utcnow()-time_created}"
    else:
        message = f'Your post seems to have violated Rule {num}. As a result, it has been removed. \n\n>Rule {num}: {read_rules(num=num)}\n\nYou can read the full rules in the sidebar.\n\nIf you think this is a mistake, you can [message the moderators](https://www.reddit.com/message/compose?to=%2Fr%2FKaguya_sama_css).'
        comment = submission.reply(message)
        comment.mod.distinguish(how="yes", sticky=True)
        submission.mod.remove()
        time_created = datetime.utcfromtimestamp(submission.created_utc)
        return f"Post removed.\nTime since post creation: {datetime.utcnow()-time_created}"


def approve_submission(url):
    submission = reddit.submission(url=url)
    submission.mod.approve()
    for c in submission.comments:
        if c.author == 'botsugi':
            c.mod.remove()
    return "Post approved."


def post_info(url):
    submission = reddit.submission(url=url)
    return submission
