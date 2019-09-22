from db import db_handler


def check_goods_interface():
    goods_info = db_handler.check_goods()
    data = ''
    if goods_info:
        for key in goods_info:
            data = data + key + '：' + goods_info[key] + '\n'
        return True, data
    else:
        return False, '数据库文件损坏'


def shopping_interface(user_name, goods_choice, goods_number_choice):
    user_info = db_handler.select(user_name)
    goods_info = db_handler.check_goods()
    for key in goods_info:
        if int(goods_choice) > len(goods_info):
            return False, '没有该商品'
        else:
            if goods_choice == key.split('.')[0]:
                user_info['shopping_car'][key.split('.')[1]] = goods_number_choice
                user_info['shopping_car']['total'] = user_info['shopping_car']['total'] + int(
                    goods_info[key]) * goods_number_choice
                db_handler.save(user_info)
                return True, '加入购物车成功'


def check_shopping_car_interface(user_name):
    user_info = db_handler.select(user_name)
    data = ''
    if user_info['shopping_car']['total'] > 0:
        for key in user_info['shopping_car']:
            data = data + key + '：' + user_info['shopping_car'][key] + '\n'
        return True, data
    else:
        return False, f'{user_name}，您的购物车为空'


def pay_shopping_car_interface(user_name):
    user_info = db_handler.select(user_name)
    if user_info['balance'] + user_info['limit'] >= user_info['shopping_car']['total']:
        if user_info['limit'] > user_info['shopping_car']['total']:
            user_info['limit'] -= user_info['shopping_car']['total']
            user_info['shopping_car'] = {"total": 0}
            db_handler.save(user_info)
            return True, "支付成功，已用信用额度支付"
        else:
            user_info['shopping_car']['total'] = user_info['shopping_car']['total'] + user_info['limit'] - \
                                                 user_info['shopping_car']['total']
            user_info['shopping_car'] = {"total": 0}
            db_handler.save(user_info)
            return True, "支付成功，已用信用额度和余额支付"
    else:
        return False, "信用额度和余额不足，无法支付"
