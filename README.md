# reddit-discord-mod-bot

Huge update! Hurray!

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
  - [Available commands](#available-commands)
    - [If you're the owner](#if-youre-the-owner)
    - [If you're the mod](#if-youre-the-mod)

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

4. Before you start, the bot wants to have a place to communicate with you. You should invite it into your server that you're going to converse with it through a url like this: `https://discordapp.com/oauth2/authorize?client_id={discord_client_id_here}&scope=bot&permissions=76880`
5. In the Command Prompt/Powershell/Terminal, type `python main.py` and hit Enter. You might have a problem with your machine automatically choosing Python 2, so if an error pops up you should use `python3 main.py`.
6. Bot should be live after you see it loading the cogs and logged in.
7. If you didn't choose to fill in the settings, try using `+setup`. Don't do this on a public server though, there are sensitive data to fill in. Don't say I didn't warn you. Just follow the steps and you'll be fine! (I think)

If you need any help, I'm @JZ#4616 on Discord. Good luck!

## Tips

This bot works well together with [Redditcord](https://discordapp.com/oauth2/authorize?client_id=372767838231986177&scope=bot&permissions=27648).

## Available commands

### If you're the owner

`--now` - Sends a copy of the settings it has. Sensitive data are redacted.

`--updaterules` - Gets the rules of the subreddit you've set and replaces the internal rules file with it. Note that this uses the Rules built-in function of your subreddit, and not whatever you put on your sidebar.

### If you're the mod

`--remove` - Remove post. URL of the post is mandatory, and the reason is optional.

Usage: 

```
--remove {url} (pinned|faq|answered|num)

```

Pre-built reasons: `pinned`/`faq` (for question posts that ask about a information already in the announcements/faq), `answered` (for question posts that can be removed because an answer is already available)

If `--updaterules` has already been used at least once, you can include a rule number. If you just want to remove the post silently, just don't include the reason.

***

`--approve` - Approve a post. URL is mandatory.

Usage: `--approve {url}`

***

`--rules` - Look at the sub rules. Provide a number for details. Only available if `--updaterules` was used at least once.