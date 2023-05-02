def create_h1(text):
    block = {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [
                {"type": "text", "text": {"content": text, "link": None}}
            ]
        },
    }
    return block


def create_h2(text):
    block = {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [
                {"type": "text", "text": {"content": text, "link": None}}
            ]
        },
    }
    return block


def create_h3(text):
    block = {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [
                {"type": "text", "text": {"content": text, "link": None}}
            ]
        },
    }
    return block


def create_text(text):
    block = {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {"type": "text", "text": {"content": text, "link": None}}
            ]
        },
    }
    return block


def create_quote(text):
    block = {
        "object": "block",
        "type": "quote",
        "quote": {
            "rich_text": [
                {"type": "text", "text": {"content": text, "link": None}}
            ]
        },
    }
    return block


def create_image(url):
    block = {
        "object": "block",
        "type": "image",
        "image": {"type": "external", "external": {"url": url}},
    }
    return block


def create_bookmark(url):
    block = {"object": "block", "type": "bookmark", "bookmark": {"url": url}}
    return block


def create_divider():
    block = {"object": "block", "type": "divider", "divider": {}}
    return block


def create_gray_text(text):
    block = {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": text, "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "gray",
                    },
                    "plain_text": text,
                    "href": None,
                }
            ],
            "children": [],
        },
    }
    return block


def create_video(url):
    block = {
        "object": "block",
        "type": "video",
        "video": {"type": "external", "external": {"url": url}},
    }
    return block


def create_bullet_point(text):
    if text:
        text = text[:1996] + "..." if len(text) > 1995 else text
    else:
        text = "No comment"
    block = {
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {"type": "text", "text": {"content": text, "link": None}}
            ]
        },
    }
    return block


def create_toggle(toggle_items):
    block = {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": [{"type": "text", "text": {"content": "Comments"}}],
            "children": [
                create_bullet_point(toggle_item) for toggle_item in toggle_items
            ],
        },
    }
    return block


def create_block(number_at, post):
    blocks_list = []
    blocks_list.append(
        create_h3(str(number_at) + ". " + post["content"]["title"])
    )  # block 1
    blocks_list.append(
        create_gray_text(str(post["content"]["votes"]) + " votes")
    )  # block 2

    if post["type"] == "image":
        blocks_list.append(create_image(post["content"]["url"]))  # block 3
    elif (
        post["type"] == "text"
        and post["content"]["text"] != ""
        and post["content"]["text"] is not None
    ):
        blocks_list.append(create_quote(post["content"]["text"]))  # block 3
    elif post["type"] == "video":
        blocks_list.append(
            create_video(post["content"]["video_url"])
        )  # block 3
    elif post["type"] == "link":
        blocks_list.append(create_bookmark(post["content"]["url"]))  # block 3
    else:
        blocks_list.append(create_text(post["content"]["url"]))  # block 3

    blocks_list.append(create_toggle(post["content"]["comments"]))
    blocks_list.append(
        create_bookmark("https://reddit.com" + post["content"]["permalink"])
    )  # block 4

    blocks_list.append(create_divider())  # block 5
    return blocks_list
