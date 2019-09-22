from db import db_handler
from conf import settings


def register_interface(user_name, user_pwd, balance=settings.BALANCE):
    user_info = db_handler.select(user_name)
    if not user_info:
        user_info = {'user_name': user_name,
                     'user_pwd': user_pwd,
                     'balance': balance,
                     'bank_flow': [],
                     'lock': False,
                     'shopping_car': {'total': 0},
                     'limit': settings.LIMIT
                     }
        db_handler.save(user_info)
        return True, '注册成功'
    else:
        return False, '当前用户已存在'


def login_interface(user_name, user_pwd):
    user_info = db_handler.select(user_name)
    if user_info:
        if user_info['user_pwd'] == user_pwd and not user_info['lock']:
            return True, '登录成功'
        else:
            return False, '密码验证失败'
    else:
        return False, '当前用户不存在'
