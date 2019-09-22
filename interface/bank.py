from db import db_handler
from conf import settings


def check_balance_interface(user_name):
    user_info = db_handler.select(user_name)
    if user_info:
        balance = user_info['balance']
        return balance


def transfer_accounts_interface(user, to_user, money):
    to_user_info = db_handler.select(to_user)
    if to_user_info and user != to_user:
        user_info = db_handler.select(user)
        if user_info['balance'] >= money:
            user_info['balance'] -= money
            to_user_info['balance'] += money
            user_info['bank_flow'].append([f'{user}向{to_user}转账{money}'])
            to_user_info['bank_flow'].append([f'{user}向{to_user}转账{money}'])
            db_handler.save(user_info)
            db_handler.save(to_user_info)
            return True, '转账成功'
        else:
            return False, '您的余额不足'
    elif user == to_user:
        return False, '不能给自己转账'
    else:
        return False, '目标用户不存在'


def repayment_interface(user_name):
    user_info = db_handler.select(user_name)
    repayment_money = 0
    if user_info['limit'] < settings.LIMIT:
        repayment_money = settings.LIMIT - user_info['limit']
        return True, f'{user_name}需还款{repayment_money}', repayment_money
    else:
        return False, '不需要还款', repayment_money


def confirm_repayment_interface(user_name, money):
    user_info = db_handler.select(user_name)
    if user_info['balance'] > money:
        user_info['balance'] -= money
        user_info['limit'] += money
    else:
        return '您的账户余额不足无法还款'
    db_handler.save(user_info)
    user_info['bank_flow'].append([f'{user_name}还款{money}'])
    return '还款成功'


def withdrawal_interface(user_name, money):
    user_info = db_handler.select(user_name)
    if user_info['balance'] >= (1 + settings.SERVICE_CHARGE) * money:
        user_info['balance'] = user_info['balance'] - (1 + settings.SERVICE_CHARGE) * money
        db_handler.save(user_info)
        user_info['bank_flow'].append([f'{user_name}取款{money}'])
        return True, '取款成功'
    else:
        return False, '您的余额不足'


def check_water_bills_interface(user_name):
    user_info = db_handler.select(user_name)
    data = ''
    if user_info['bank_flow']:
        for item in user_info['bank_flow']:
            data += str(item)
            data += '\n'
        return True, data
    else:
        return False, '您还没有流水记录'
