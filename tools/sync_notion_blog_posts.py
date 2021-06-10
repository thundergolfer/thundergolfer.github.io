import logging
import os
import requests  # third party dep


logging.basicConfig(level=logging.DEBUG)

NOTION_API_BASE = "https://api.notion.com/v1/"
NOTION_BLOCKS_API_BASE = f"{NOTION_API_BASE}blocks/"


def retrieve_full_page(page_id: str):
    """
    The 'pages' endpoint actually just returns the properties of a page.
    To get the content of a page you need to use the 'blocks' endpoint and retrieve all of a
    page's children.

    See: https://developers.notion.com/reference/get-block-children
    """
    children = []
    blog_listing_block_children_url = f"{NOTION_BLOCKS_API_BASE}{page_id}/children?page_size100"
    token = os.environ['NOTION_API_TOKEN']
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-05-13",
    }
    has_more = True
    next_cursor = None
    while has_more:
        if next_cursor:
            res = requests.get(
                f"{blog_listing_block_children_url}&start_cursor={next_cursor}",
                headers=headers,
            )
        else:
            res = requests.get(
                blog_listing_block_children_url,
                headers=headers
            )

        data = res.json()
        has_more = data["has_more"]
        if has_more:
            next_cursor = data["next_cursor"]
        children.extend(
            data["results"]
        )

    return children


blog_listing_page_id = "532ddb26-001e-4f2f-a7ec-38fef6081dda"
children = retrieve_full_page(page_id=blog_listing_page_id)
import pdb; pdb.set_trace()
# TODO(Jonathon): Implement 'Notion children' -> Jekyll Markdown Post logic
