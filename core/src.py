from interface import user, bank, shop
from lib import common

user_dic = {
    'user_name': None
}


def index():
    """
    主界面菜单
    :return:
    """
    while True:
        if user_dic['user_name']:
            print('---------------\n'
                  '3.查看余额\n'
                  '4.转账\n'
                  '5.还款\n'
                  '6.取款\n'
                  '7.查看流水\n'
                  '8.购物\n'
                  '9.查看购买商品\n'
                  '10.注销\n'
                  '---------------\n')
        else:
            print('---------------\n'
                  '1.登录\n'
                  '2.注册\n'
                  '3.查看余额\n'
                  '4.转账\n'
                  '5.还款\n'
                  '6.取款\n'
                  '7.查看流水\n'
                  '8.购物\n'
                  '9.查看购买商品\n'
                  '10.注销\n'
                  '---------------\n')
        choice = input('请输入功能编号：').strip()
        choice_dic = {
            '1': login,
            '2': register,
            '3': check_balance,
            '4': transfer_accounts,
            '5': repayment,
            '6': withdrawal,
            '7': check_water_bills,
            '8': shopping,
            '9': check_shopping_car,
            '10': cancel,
        }

        if choice not in choice_dic:
            continue
        choice_dic.get(choice)()


def login():
    """
    登录功能
    """
    print('---------\n欢迎登录\n---------\n')
    while True:
        user_name = input('请输入用户名：').strip()
        user_pwd = input('请输入密码：').strip()
        flag, msg = user.login_interface(user_name, user_pwd)
        if flag:
            user_dic['user_name'] = user_name
            print(msg)
            break
        else:
            print(msg)
            continue


def register():
    """
    注册功能
    """
    print('---------\n欢迎注册\n---------\n')
    while True:
        user_name = input('请输入用户名：').strip()
        user_pwd = input('请输入密码：').strip()
        conf_pwd = input('请确认密码：').strip()
        if user_pwd == conf_pwd:
            flag, msg = user.register_interface(user_name, user_pwd)
            if flag:
                print(msg)
                break
            else:
                print(msg)
                continue
        else:
            print("两次输入不一致")


@common.auth
def check_balance():
    """
    查看余额
    """
    print('---------\n查看余额\n---------\n')
    balance = bank.check_balance_interface(user_dic['user_name'])
    print(f'尊敬的用户您好，您的余额为：{balance}')


@common.auth
def transfer_accounts():
    """
    转账功能
    """
    print('---------\n转账\n---------\n')
    while True:
        to_user = input('目标用户：').strip()
        money = input('转账金额：').strip()
        if money.isdigit():
            money = int(money)
            flag, msg = bank.transfer_accounts_interface(user_dic['user_name'], to_user, money)
            if flag:
                print(msg)
                break
            else:
                print(msg)
                break
        else:
            print('您的输入有误')


@common.auth
def repayment():
    """
    还款
    """
    print('---------\n还款\n---------\n')
    while True:
        flag, msg, repayment_money = bank.repayment_interface(user_dic['user_name'])
        if flag:
            print(msg)
            while True:
                money = input('请输入还款金额：').strip()
                if money.isdigit():
                    money = int(money)
                    if money <= repayment_money:
                        msg = bank.confirm_repayment_interface(user_dic['user_name'], money)
                    else:
                        print('还款金额出错')
                        continue
                    print(msg)
                    break
                else:
                    print('您的输入有误')
            break
        else:
            print(msg)
            break


@common.auth
def withdrawal():
    """
    取款
    """
    print('---------\n取款\n---------\n')
    while True:
        money = input('请输入取款金额：').strip()
        if money.isdigit():
            money = int(money)
            flag, msg = bank.withdrawal_interface(user_dic['user_name'], money)
            if flag:
                print(msg)
                break
            else:
                print(msg)
                break
        else:
            print('您的输入有误')


@common.auth
def check_water_bills():
    """
    查看流水
    """
    print('---------\n查看流水\n---------\n')
    while True:
        flag, msg = bank.check_water_bills_interface(user_dic['user_name'])
        if flag:
            print(msg)
            break
        else:
            print(msg)
            break


@common.auth
def shopping():
    """
    购物
    """
    print('---------\n购物\n---------\n')
    print('商品名称：价格\n')
    flag_goods, msg_goods = shop.check_goods_interface()
    while True:
        if flag_goods:
            print(msg_goods)
            goods_choice = input('请输入要购买的商品编号（输入q结算）:').strip()
            if goods_choice == 'q':
                flag_pay, msg_pay = shop.pay_shopping_car_interface(user_dic['user_name'])
                if flag_pay:
                    print(msg_pay)
                    break
                else:
                    print(msg_pay)
                    break
            else:
                goods_number_choice = int(input('请输入要购买的数量:').strip())
                flag, msg = shop.shopping_interface(user_dic['user_name'], goods_choice, goods_number_choice)
                print(msg)
                continue
        else:
            print(msg_goods)
            break


@common.auth
def check_shopping_car():
    """
    查看购物车
    """
    print('---------\n查看购物车\n---------\n')
    while True:
        flag, msg = shop.check_shopping_car_interface(user_dic['user_name'])
        if flag:
            print('商品名称：数量\n')
            print(msg)
            break
        else:
            print(msg)
            break


def cancel():
    """
    注销账户
    """
    user_dic['user_name'] = None
