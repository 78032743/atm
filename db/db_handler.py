from conf import settings
import os
import json


def save(user_info):
    path = os.path.join(settings.BASE_DB, f'{user_info["user_name"]}.json')
    with open(path, 'w', encoding='utf-8')as f:
        json.dump(user_info, f)
        f.flush()


def select(name):
    path = os.path.join(settings.BASE_DB, f'{name}.json')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8')as f:
            data = json.load(f)
            return data
    else:
        return False


def check_goods():
    path = os.path.join(settings.BASE_DB, 'goods.json')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8')as f:
            data = json.load(f)
            return data
    else:
        return False
