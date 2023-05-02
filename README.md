# Reddit To Notion

Tired of endless scrolling on Reddit? You probably are. The reason behind the endless scroll of doom is because you want to stay connected, to not feel any FOMO, to not miss anything.
Maybe the next post will be something important. Maybe I can find a life hack that will change my life forever.
It keeps going on and on and on.

I found a way to reduce this behaviour. Every day, at 8am in the morning and 8pm in the night, my scheduled CRON job runs `run.py` on my server.

It connects to reddit for every subreddit I have configured in `config.py`, fetches the top posts there, including any text, image, video in the post, alongwith top comments per post.
Then using Notion API, it creates a separate page for each subreddit, and adds the posts there.

So everyday while having my breakfast, I open the notion page on my phone (for which I have put in a shortcut on my homescreen), and keep me up to date with whatever is happening on Reddit

# Installation

### Pre-requisite

-   Python >= 3.10
-   Docker, Docker-compose (optional)
-   Reddit API token
    > Follow the steps [here](https://praw.readthedocs.io/en/latest/tutorials/reply_bot.html), your created bots and details can be found [here](https://www.reddit.com/prefs/apps)
-   Notion integration key
    > Create a notion page, and create an integration using [this guide](https://developers.notion.com/docs/create-a-notion-integration).

### Running

-   Copy the .env.example to .env
-   Update the variables
-   Run

```sh
docker compose up -d
```
