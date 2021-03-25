# reddit-discord-mod-bot

(Updated 25th March 2021) Pretty significant update, using Asyncpraw and added a couple more functions.

Ever thought, "Geez, I'm active on Discord yet I need to scavenge the subreddit I mod every hour to at least fulfill my mod duties"?

Well, this bot might suit your needs! Do your mod job for virtual Internet attention, all from the comfort of your Discord server!

## Table of Contents

- [reddit-discord-mod-bot](#reddit-discord-mod-bot)
  - [Table of Contents](#table-of-contents)
  - [What's this?](#whats-this)
  - [How to install](#how-to-install)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Tips](#tips)

## What's this?

A Python script to help you mod your subreddit within Discord.

## How to install

### Prerequisites

- You'll need to have Python 3.7. 3.6 might work as well, but it hasn't been tested fully. Make sure you have `pip` and `python` in your environment variables.
- You'll also need to have a bot registered in the [Discord Developer Portal](https://discordapp.com/developers/applications). Register an application, make a Bot on the sidebar, and take note of the token.
- You'll also need a Reddit account, obviously. While logged in, go to `preferences` > `apps` > `create another app...`. Fill up the form. You'll need the client ID and client secret.

### Installation

1. Obtain this repo. If you're using the download function, you might want to unzip it first.
2. Install the requirements. Open up a Command Prompt/Powershell/Terminal in the folder of this repo, and go `pip install -r requirements.txt`. Wait for it to finish its job.
3. Locate `resources\\settings.json`. Fill in the details that it needs to know to function.

```json
{
    "discord": {
        "owner": , // no quotes
        "token": "",
        "prefix": "--"
    },
    "reddit": {
        "client_id": "",
        "client_secret": "",
        "username": "",
        "password": "",
        "user_agent": "Developed by /u/JingzOoi"
    },
    "subreddit": {
        "name": "",
        "mods": [
            mod_id_1, //no quotes
            mod_id_2,
            ...
        ]
    }
}
```

1. Before you start, the bot wants to have a place to communicate with you. You should invite it into your server that you're going to converse with it through a url like this: `https://discordapp.com/oauth2/authorize?client_id={discord_client_id_here}&scope=bot&permissions=76880`
2. In the Command Prompt/Powershell/Terminal, type `python main.py` and hit Enter. You might have a problem with your machine automatically choosing Python 2, so if an error pops up you should use `python3 main.py`.
3. Bot should be live after you see it loading the cogs and logged in.

If you need any help, I'm @JZ#4616 on Discord. Good luck!

## Tips

This bot works well together with [Redditcord](https://discordapp.com/oauth2/authorize?client_id=372767838231986177&scope=bot&permissions=27648). (Update: This bot is now made private after the new Discord API update about bots. Might spin one up later.)

Use `--help` for a list of available commands.

Currently is able to remove and approve posts, check if post media is a repost, and check modmail. I'll add more in the future. Also all of the functions are tailored to fit my own needs, if you need more you'll have to tell me and I'll see what I can do.

Also you can change the prefix in `settings.json` if you don't like `--`.
