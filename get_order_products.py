import efficient_apriori
import pandas as pd
import numpy as np
import time

from collections import OrderedDict

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
    df_new = df_orders_product.groupby('orders_code')['product_code'].apply(list)

    for index, row in df_new.items():  # 获取每行的index、row
        orders_product_info[index] = row

    print('get_orders_product_info cost time: ', time.time()-start_t)
    return orders_product_info


def split_suit_product(orders_product_info, suits_product_info):
    return orders_product_info


def map_product_code_2_common_titles(orders_product_info, )





# ddd = get_suits_product_info()

# print('ddd[796319] is ', ddd[796319])
# print('ddd[799223] is ', ddd[799223])

eee = get_orders_product_info()
print('eee is ', len(eee))