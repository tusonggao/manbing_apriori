import os
import json
import time
import pandas as pd
from sqlalchemy import create_engine

###############################################################

def read_sql_script(sql_file):
    sql_str = ''
    with open(sql_file, encoding='UTF-8') as file:
        for line in file:
            content = line.strip()
            if content.startswith('--'):  # 过滤注释行
                continue
            if content.find('/*')!=-1 and content.find('*/')!=-1:
                start_idx = content.index('/*')
                end_idx = content.index('*/')
                print('start_idx, end_idx ', start_idx, end_idx)
                content = content[:start_idx] + content[end_idx+2:]
            sql_str += ' ' + content
    return sql_str


def basefilename(full_file_name):
    file_name = os.path.split(full_file_name)[-1]
    raw_file_name = os.path.splitext(file_name)[0]
    print('raw_file_name is', raw_file_name)
    return raw_file_name


def read_and_store_df_from_impala(sql_file):
    print('read_and_store_df_from_impala: ', sql_file)

    start_t = time.time()
    conn_impala = create_engine('impala://172.21.57.127:21050')
    sql = read_sql_script(sql_file)
    print('sql is ', sql)
    df = pd.read_sql(sql, conn_impala)
    end_t = time.time()

    print('read data from impala cost time ', end_t-start_t)
    print('df.shape is', df.shape)
    print('df.head() is', df.head())

    output_file = basefilename(sql_file) + '_data.csv'
    df.to_csv('./data/'+output_file, index=0)

    return df



# df = read_and_store_df_from_impala('./sql_scripts/hive_sql_orders_products.txt')
# df = read_and_store_df_from_impala('./sql_scripts/hive_sql_products_info.txt')


df_order_products = pd.read_csv('./data/hive_sql_orders_products_data.csv')
# df1 = df.groupby('orders_code')['product_code'].apply(list)
print('df_order_products.shape is ', df_order_products.shape)
print('df_order_products.head(10) is ', df_order_products.head(10))


df_product_name_map = pd.read_csv('./data/hive_sql_products_info_data.csv')
df_product_name_map = df_product_name_map[['product_code', 'common_title']]
# df1 = df.groupby('orders_code')['product_code'].apply(list)
print('df_product_name_map.shape is ', df_product_name_map.shape)
print('df_product_name_map.head(10) is ', df_product_name_map.head(10))


df_merged = pd.merge(df_order_products, df_product_name_map, how='left', on=['product_code'])
print('df_merged.shape is ', df_merged.shape)
print('df_merged.head(10) is ', df_merged.head(10))


print('start group by')
start_t = time.time()
df_new = df_merged.groupby('orders_code')['common_title'].apply(list)
print(df_new.shape)
print('group by cost time', time.time()-start_t)

df_new.to_csv('./data/df_new_data.csv')

print('program ends')




