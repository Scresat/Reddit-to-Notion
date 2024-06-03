import requests
import config
import copy

new_page_endpoint = "https://api.notion.com/v1/pages"


def create_page(children, subreddit_details):
    data = {
        "parent": {"type": "page_id", "page_id": config.page_block_id},
        "properties": {
            "title": [{"text": {"content": "r/" + subreddit_details["name"]}}]
        },
        "children": children,
    }
    
    if (
        subreddit_details["icon"] != ""
        and subreddit_details["icon"] is not None
    ):
        data["icon"] = {
            "type": "external",
            "external": {"url": subreddit_details["icon"]},
        }
    elif (
        subreddit_details["icon2"] != ""
        and subreddit_details["icon2"] is not None
    ):
        data["icon"] = {
            "type": "external",
            "external": {"url": subreddit_details["icon2"]},
        }
    else:
        data["icon"] = {
            "type": "external",
            "external": {
                "url": "https://www.redditstatic.com/desktop2x/img/favicon/favicon-96x96.png"
            },
        }

    if (
        subreddit_details["cover"] != ""
        and subreddit_details["cover"] is not None
    ):
        data["cover"] = {
            "type": "external",
            "external": {"url": subreddit_details["cover"]},
        }

    # create new notion page
    total_posts_added = 0
    if len(data["children"]) > 99:
        patch_data = copy.deepcopy(data)
        patch_data["children"] = data["children"][:100]
        total_posts_added += len(data["children"]) / 5

        new_page_response = requests.post(
            new_page_endpoint, headers=config.headers, json=patch_data
        )
        # pprint.pprint(new_page_response.json())

        if new_page_response.status_code == 200:
            created_page_id = new_page_response.json()["id"]
            for i in range(100, len(data["children"]), 100):
                patch_data = {"children": data["children"][i : i + 100]}
                for current_children in patch_data["children"]:
                    current_children["parent"] = {
                        "type": "page_id",
                        "page_id": created_page_id,
                    }

                new_page_response = requests.patch(
                    f"https://api.notion.com/v1/blocks/{created_page_id}/children",
                    headers=config.headers,
                    json=patch_data,
                )
                if new_page_response.status_code != 200:
                    print("Page updation failed")
                    print(new_page_response.text)
                    print(subreddit_details)
        else:
            print("Page creation failed")
            print(new_page_response.text)
            print(subreddit_details)

    else:
        new_page_response = requests.post(
            new_page_endpoint, headers=config.headers, json=data
        )
        if new_page_response.status_code != 200:
            print("Page creation failed")
            print(new_page_response.text)
            print(subreddit_details)
