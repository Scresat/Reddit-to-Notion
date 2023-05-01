import os


notion_integration_key = os.environ.get("NOTION_KEY")
page_block_id = os.environ.get("NOTION_PAGE_ID")
username = os.environ.get("REDDIT_USERNAME")
password = os.environ.get("REDDIT_PASSWORD")
client_id = os.environ.get("REDDIT_CLIENT_ID")
client_secret = os.environ.get("REDDIT_SECRET")
timezone = os.environ.get("TIMEZONE", "Asia/Kolkata")


headers = {
    "authorization": "Bearer " + notion_integration_key,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

number_of_posts_to_fetch = 10
subreddit_to_scrape = [
    {
        "category": "Sitewide",
        "subreddits": [
            "all",
            "popular",
        ],
    },
    {"category": "News", "subreddits": ["worldnews", "news", "technology"]},
    {"category": "Memes", "subreddits": ["dankmemes", "programmerhumor"]},
    {
        "category": "India",
        "subreddits": ["pune", "indiangaming", "developersindia"],
    },
    {"category": "Entertainment", "subreddits": ["movies", "television"]},
    {"category": "Sports", "subreddits": ["formula1", "cricket"]},
    {"category": "Miscellaneous", "subreddits": ["askreddit"]},
]
