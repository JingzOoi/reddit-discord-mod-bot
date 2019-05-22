import json
import os
import praw

# make resources folder
os.makedirs('resources', exist_ok=True)

# setup discord bot credentials
print('\nWe are now setting up your bot. \nMake sure you already have the Discord side client and Reddit side client registered and ready to go.\n')
bot_cred = {
    "reddit": {
        "client_id": input("Reddit client id: "),
        "client_secret": input("Reddit client secret: "),
        "username": input("Reddit username: "),
        "password": input("Reddit password: ")
    },
    "discord": {
        "token": input("Discord client token: ")
    }
}

with open('resources\\token.json', 'w') as f:
    f.write(json.dumps(bot_cred, indent=4))

# setup subreddits to moderate
print('We are now setting up the subreddit(s) that the bot will mod.\nMake sure that the bot account is a moderator of the subreddit(s).')
subreddit_list = []
while True:
    subreddit_to_mod = input("Subreddit to mod (Leave blank to end): ")
    if subreddit_to_mod == '':
        break
    else:
        subreddit_list.append(subreddit_to_mod)

with open('resources\\subreddit.json', 'w') as f:
    f.write(json.dumps({"subreddit": subreddit_list}, indent=4))

# import rules
print('Importing rules from your subreddit.\nReminder: rules are not the ones you list on your sidebar, but the ones you setup in the rules page of your subreddit.')

with open('resources\\token.json', 'r') as f:
    r_cred = json.load(f)["reddit"]
reddit = praw.Reddit(
    client_id=r_cred["client_id"],
    client_secret=r_cred["client_secret"],
    username=r_cred["username"],
    password=r_cred["password"],
    user_agent=f'/u/{r_cred["username"]}'
)
subreddit = reddit.subreddit(subreddit_list[0])

rules = {}
for num, rule in enumerate(subreddit.rules()["rules"], start=1):
    rules[f'{num}'] = {
        "name": rule["short_name"],
        "desc": rule["description"]
    }

with open('resources\\rules.json', 'w') as f:
    f.write(json.dumps(rules, indent=4))


# setup discord users that can use mod commands
print('We are now setting up the users that can use the moderator commands on Discord. \nGet the IDs of the authorized users.')
authorized_users = []
while True:
    authorized_user = input("ID of authorized user (Leave blank to end): ")
    if authorized_user == '':
        break
    else:
        authorized_users.append(authorized_user)

with open('resources\\authorized_users.json', 'w') as f:
    f.write(json.dumps({"authorized_users": authorized_users}, indent=4))

print('We are done! Now you should be able to run the bot through main.py. Happy modding!')
