<h1>reddit-discord-mod-bot</h1>

<p>A self-hosted bot to moderate your subreddit from Discord.</p>

<hr>

<h2>(External) Requirements:</h2>
<ol>
    <li><a href='https://www.python.org/downloads/release/python-365/'>Python 3.6</a></li>
    <li><a href='https://github.com/praw-dev/praw'>Python Reddit API Wrapper (PRAW)</a></li>
    <li><a href='https://github.com/Rapptz/discord.py'>discord.py</a></li>
    <a href='https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token'>Register your bot with Discord</a>
    <a href='https://www.youtube.com/watch?v=krTUf7BpTc0'>Register your script with Reddit (Up till getting the client id and secret for the bot)</a>
</ol>

Best paired with <a href='https://discordapp.com/oauth2/authorize?client_id=372767838231986177&scope=bot&permissions=27648'>Redditcord by @appu#4444</a>.

<hr>

<h2>Installation</h2>
<ol>
    <li>Install all the requirements above.</li>
    <li>Clone/Download this repo.</li>
    <li>Run setup.py and follow the steps.</li>
    <li>Run main.py to start the bot.</li>
</ol>

<hr>

<h2>What the bot can do</h2>
Default prefix: -
<ul>
    <li>Remove posts</li>
    <pre>
        -remove (url) (rule number)
    </pre>
    <li>Approve posts</li>
    <pre>
        -approve (url)
    </pre>
    <li>Display rules</li>
    <pre>
        -rules 
        -rules (rule number)
    </pre>
</ul>