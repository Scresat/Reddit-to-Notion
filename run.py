import requests
import config
import reddit_fetch
import block_creator
import notion_delete_data
import notion_get_data
import praw
import notion_create_page
from datetime import datetime
import pytz

r = praw.Reddit(
    username=config.username,
    password=config.password,
    client_id=config.client_id,
    client_secret=config.client_secret,
    user_agent="The Reddit Commenter v1.0",
)

notion_delete_data.delete_all_blocks(
    notion_get_data.get_all_ids(notion_get_data.get_data())
)

end_point = f"https://api.notion.com/v1/blocks/{config.page_block_id}/children"
new_page_endpoing = "https://api.notion.com/v1/pages"


IndiaTz = pytz.timezone(config.timezone)

timeInIndia = datetime.now(IndiaTz)
currentTimeInIndia = timeInIndia.strftime("%I:%M%p, %d %B %Y, ")
data = {
    "children": [
        block_creator.create_gray_text(text="Updated at: " + currentTimeInIndia)
    ]
}
requests.patch(end_point, headers=config.headers, json=data)

for current_category_index in range(len(config.subreddit_to_scrape)):
    data = {"children": []}
    data["children"].append(
        block_creator.create_h2(
            (config.subreddit_to_scrape[current_category_index]["category"])
        )
    )
    # add block to page
    response = requests.patch(end_point, headers=config.headers, json=data)

    for current_subreddit_index in range(
        len(config.subreddit_to_scrape[current_category_index]["subreddits"])
    ):
        data = {"children": []}
        top_posts = reddit_fetch.fetch_posts(
            config.subreddit_to_scrape[current_category_index]["subreddits"][
                current_subreddit_index
            ],
            r,
        )

        for i in range(len(top_posts)):
            data["children"].extend(
                block_creator.create_block(i + 1, top_posts[i])
            )

        notion_create_page.create_page(
            data["children"],
            reddit_fetch.get_subreddit_details(
                config.subreddit_to_scrape[current_category_index][
                    "subreddits"
                ][current_subreddit_index],
                r,
            ),
        )
