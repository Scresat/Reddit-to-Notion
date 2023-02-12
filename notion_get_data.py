import requests
import config
import pprint
import json
import notion_delete_data

def get_data():
    end_point = f'https://api.notion.com/v1/blocks/{config.page_block_id}/children'

    response = requests.get(end_point, headers=config.headers)
    
    return response.json()

def get_all_ids(result):
    return [i['id'] for i in result['results']]
