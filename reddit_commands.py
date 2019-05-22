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
    user_agent=f'/u/{r_cred["username"]} by /u/JingzOoi'
)

subreddit_list = [
    'Kaguya_sama_css',
    'Kaguya_sama'
]


def read_rules(num="0"):
    with open("resources\\rules.json", "r") as f:
        rules = json.load(f)
    ruleList = [str(i) for i in range(10)]
    if num not in ruleList:
        return "Invalid rule number."
    elif num == "0":
        r = 'Subreddit Rules: '
        for rule, desc in zip(rules.keys(), rules.values()):
            r += f'\n\n{rule}: {desc}'
        return f'```{r}```'
    else:
        return rules[num]


def remove_submission(url, num):
    submission = reddit.submission(url=url)
    if submission.subreddit.display_name not in subreddit_list:
        return f"Invalid subreddit. Subreddit must be from one of the following: {subreddit_list}"
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


def newJBchapter(chapterNum, url):
    r = re.compile(
        r'https://jaiminisbox\.com/reader/read/kaguya-wants-to-be-confessed-to/en/0/[0-9]+/page/1')
    if re.match(r, url):
        subreddit = reddit.subreddit('Kaguya_sama_css')
        subreddit.submit(
            title=f"Kaguya Wants to be Confessed to :: Chapter {chapterNum} :: Jaimini's Box", url=url, flair_text="Chapter Discussion")

        return f"Kaguya-sama chapter {chapterNum} by JB posted to /r/Kaguya_sama_css: {subreddit.new(limit=1)}"
    else:
        return "URL doesn't look quite right."
