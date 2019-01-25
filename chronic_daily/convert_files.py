# import efficient_apriori
# from efficient_apriori import apriori

import pandas as pd
import numpy as np
import time
import json

from apriori_in_actions import *
from collections import OrderedDict


useless_common_titles = {'售后服务卡', '健客大药房旗舰店宣传单', '健客家庭药箱',
                         'nan', '无'}


def strip_useless_titles(titles_list):
    titles_list_new = []

    for title in titles_list:
        flag = True
        for useless_title in useless_common_titles:
            if title==useless_title:
                flag = False
                break
        if flag:
            titles_list_new.append(title)
        else:
            print('title: ', title)

    return titles_list_new

def convert_transactions_files():
    transactions = []
    with open('orders_common_titles_info_split.json', 'r', encoding='utf8') as file:
        orders_common_titles = json.load(file)

    skip_num = 0
    # with open('./samples_ttt.txt', 'w', encoding='utf8') as file:
    with open('./chronic_samples_full.txt', 'w', encoding='utf8') as file:
        cnt = 0
        for code in orders_common_titles:
            cnt += 1
            products = [str(ele).strip() for ele in orders_common_titles[code]]
            products = set(products)
            products = list(products)
            products = strip_useless_titles(products)
            if len(products)==0:
                print('skip one transaction')
                skip_num += 1
                continue
            content = '###'.join(products)
            file.write(content+'\n')
            if cnt>=10000:
                continue

    print('skip_num is ', skip_num)
    print('convert_transactions_files file write ok')


def check_transactions_files():
    with open('./chronic_samples_full.txt', 'r', encoding='utf8') as file:
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



