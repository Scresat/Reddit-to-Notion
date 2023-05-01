import requests
import config
import time


def delete_all_blocks(id_list):
    end_point = "https://api.notion.com/v1/blocks/"
    for id in id_list:
        requests.delete(end_point + id, headers=config.headers)
        time.sleep(1)
