def auth(func):
    from core import src
    def wrapper(*args, **kwargs):
        if src.user_dic['user_name']:
            ret = func(*args, **kwargs)
            return ret
        else:
            print('请先登录')
            src.login()

    return wrapper
