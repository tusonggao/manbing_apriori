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



df = read_and_store_df_from_impala('./sql_scripts/hive_sql_orders_products.txt')



print('program ends')




