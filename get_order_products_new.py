import efficient_apriori
# from efficient_apriori import apriori

import pandas as pd
import numpy as np
import time
import json

# from apriori_in_actions import *
from collections import OrderedDict

useless_common_titles = {'售后服务卡', '健客大药房旗舰店宣传单', '健客家庭药箱'}

def get_suits_product_info():
    start_t = time.time()
    suits_product_info = {}
    df = pd.read_csv('./data/hive_sql_suits_info_data.csv')
    print('df.dtypes is ', df.dtypes)
    df_new = df.groupby('suit_product_code')['single_product_code'].apply(list)
    for index, row in df_new.items():  # 获取每行的index、row
        suits_product_info[index] = row
    print('get_suits_product_info cost time: ', time.time()-start_t)
    return suits_product_info


def get_orders_product_info():
    start_t = time.time()

    print('in get_orders_product_info start ')
    orders_product_info = {}
    df_orders_product = pd.read_csv('./data/hive_sql_orders_products_data.csv')
    df_orders_product = df_orders_product[['orders_code', 'product_code']]

    df_orders_product.sort_values(by=['orders_code'], ascending=False, inplace=True)
    # df_orders_product = df_orders_product[:3000]

    df_new = df_orders_product.groupby('orders_code')['product_code'].apply(list)

    for index, row in df_new.items():  # 获取每行的index、row
        orders_product_info[index] = row

    print('get_orders_product_info cost time: ', time.time()-start_t)
    return orders_product_info


def split_suit_product(orders_product_info, suits_product_info):
    print('in split_suit_product')
    orders_product_info_new = {}
    for orders_code in orders_product_info:
        orders_product_info_new[orders_code] = []
        for product_code in orders_product_info[orders_code]:
            if product_code in suits_product_info:
                orders_product_info_new[orders_code] += suits_product_info[product_code]
            else:
                orders_product_info_new[orders_code].append(product_code)

    return orders_product_info_new


def map_product_code_2_common_titles(orders_product_info):
    print('in map_product_code_2_common_titles')
    df_product_name_map = pd.read_csv('./data/hive_sql_products_info_data.csv')
    # df_product_name_map = df_product_name_map.sample(15)
    df_product_name_map = df_product_name_map[['product_code', 'common_title']]
    df_product_name_map = df_product_name_map.set_index('product_code')
    df_product_name_map = df_product_name_map.to_dict()['common_title']
    # print('df_product_name_map is ', df_product_name_map)

    correct_cnt = 0
    err_cnt = 0

    orders_product_info_new = {}
    for order_code in orders_product_info:
        common_title_set = set()
        for product_code in orders_product_info[order_code]:
            try:
                common_title = df_product_name_map[product_code]
                # print('product_code is {0} common_title is {1}'.format(product_code, common_title))
                if common_title not in useless_common_titles:
                    common_title_set.add(common_title)
                correct_cnt += 1
            except KeyError:
                err_cnt += 1
                # print('Oops! product_code: {0} not in df_product_name_map'.format(product_code))
        orders_product_info_new[order_code] = list(common_title_set)

    print('err_cnt is ', err_cnt, 'correct_cnt is ', correct_cnt)
    return orders_product_info_new


# orders_product_info = get_orders_product_info()
# print('orders_product_info is ', len(orders_product_info))
# orders_common_titles_info_unsplit = map_product_code_2_common_titles(orders_product_info)
#
# suits_product_info = get_suits_product_info()
# orders_product_info_split = split_suit_product(orders_product_info, suits_product_info)
# orders_common_titles_info_split = map_product_code_2_common_titles(orders_product_info_split)
#
# with open('orders_common_titles_info_unsplit.json', 'w', encoding='utf8') as fp:
#     json.dump(orders_common_titles_info_unsplit, fp)
#
# with open('orders_common_titles_info_split.json', 'w', encoding='utf8') as fp:
#     json.dump(orders_common_titles_info_split, fp)

# with open('orders_common_titles_info_unsplit.json', 'r', encoding='utf8') as file:
#     ddd = json.load(file)
#     print(ddd)


def get_all_transactions():
    transactions = []
    with open('orders_common_titles_info_split.json', 'r', encoding='utf8') as file:
        ddd = json.load(file)

    cnt = 0
    for code in ddd:
        # transactions.append(list(ddd[code]))
        # transactions.append([str(ele) for ele in ddd[code]])
        transactions.append(tuple([str(ele) for ele in ddd[code]]))
        cnt += 1
        if cnt > 1000:
            continue
    # print('transactions is ', transactions)
    print('len of transactions is ', len(transactions))
    return transactions




if __name__=='__main__':
    # transactions = [('eggs', 'bacon', 'soup'),
    #                 ('eggs', 'bacon', 'apple'),
    #                 ('soup', 'bacon', 'banana')]

    transactions = get_all_transactions()
    # dataSet=loadDataSet()
    # print('dataSet is', dataSet)

    print('start apriori')

    itemsets, rules = efficient_apriori.apriori(transactions, min_support=0.0003, min_confidence=0.02)
    print(rules)  # [{eggs} -> {bacon}, {soup} -> {bacon}]
