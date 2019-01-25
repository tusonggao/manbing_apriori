# import efficient_apriori
# from efficient_apriori import apriori

import pandas as pd
import numpy as np
import time
import json

from apriori_in_actions import *
from collections import OrderedDict

useless_common_titles = {'售后服务卡', '健客大药房旗舰店宣传单', '健客家庭药箱'}


def convert_transactions_files():
    transactions = []
    with open('orders_common_titles_info_split.json', 'r', encoding='utf8') as file:
        orders_common_titles = json.load(file)

    # with open('./samples_ttt.txt', 'w', encoding='utf8') as file:
    with open('./samples_full.txt', 'w', encoding='utf8') as file:
        cnt = 0
        for code in orders_common_titles:
            products = [str(ele).strip() for ele in orders_common_titles[code]]
            products = set(products)
            products = list(products)
            content = '###'.join(products)
            file.write(content+'\n')
            cnt += 1
            if cnt%50000==0:
                print('cnt is ', cnt)

    print('convert_transactions_files file write ok')


def check_transactions_files():
    with open('./samples_full.txt', 'r', encoding='utf8') as file:
        cnt = 0
        for line in file:
            cnt += 1
            sss = line.strip().split('###')
            if len(set(sss))!=len(sss):
                print('cnt is ', cnt, 'sss is ', sss)

    print('check_transactions_files file write ok')


if __name__=='__main__':
    convert_transactions_files()
    check_transactions_files()



