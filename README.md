# reddit-discord-mod-bot (Everything is broken right now. Don't download.)

Huge update! Hurray!

Ever thought, "Geez, I'm active on Discord yet I need to scavenge the subreddit I mod every hour to at least fulfill my mod duties"?

Well, this bot might suit your needs! Do your mod job for virtual Internet attention, all from the comfort from your Discord server!

## Table of Contents

- [reddit-discord-mod-bot (Everything is broken right now. Don't download.)](#reddit-discord-mod-bot-everything-is-broken-right-now-dont-download)
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
3. Locate `resources\\settings.json`. Fill in just the part about discord owner and discord token. Make sure that the owner field is filled with owner id and is not surrounded in quotes. Also make sure that the token is in quotes. Like so:

```json
{
    "discord": {
        "owner": {owner_id},
        "token": "{secret_token}"
    },
    ...
}
```
Optionally, you can choose to fill in the rest of the fields *if you know what you're doing*. Just note the formatting about what is `int` and what is `str`. I've already labelled what should be in quotes, **except the owner ID field**. That needs to be an int. If you fail, no worries! Just download a copy from here and just replace it.

4. In the Command Prompt/Powershell/Terminal, type `python main.py` and hit Enter. You might have a problem with your machine automatically choosing Python 2, so if an error pops up you should use `python3 main.py`.
1. Bot should be live after you see it loading the cogs and logged in.
2. If you didn't choose to fill in the settings, try using `+setup`. Don't do this on a public server though, there are sensitive data to fill in. Don't say I didn't warn you. Just follow the steps and you'll be fine!

If you need any help, I'm @JZ#4616 on Discord. Good luck!

## Tips

This bot works well together with [Redditcord](https://discordapp.com/oauth2/authorize?client_id=372767838231986177&scope=bot&permissions=27648).