# import efficient_apriori
# from efficient_apriori import apriori

import pandas as pd
import numpy as np
import time
import json

from apriori_in_actions import *
from collections import OrderedDict

def get_all_transactions():
    transactions = []
    with open('orders_common_titles_info_split.json', 'r', encoding='utf8') as file:
        ddd = json.load(file)

    cnt = 0
    for code in ddd:
        # transactions.append(list(ddd[code]))
        transactions.append([str(ele) for ele in ddd[code]])
        cnt += 1
        if cnt > 1000:
            continue
    print('len of transactions is ', len(transactions))

    return transactions


if __name__=='__main__':
    # transactions = [('eggs', 'bacon', 'soup'),
    #                 ('eggs', 'bacon', 'apple'),
    #                 ('soup', 'bacon', 'banana')]

    dataSet = get_all_transactions()
    # dataSet=loadDataSet()
    # print('dataSet is', dataSet)

    print('start apriori')
    L, suppData = apriori(dataSet, minSupport=0.0005)
    print('L is', L)
    print('suppData is', suppData)

    print('start generateRules')
    rules = generateRules(L, suppData, minConf=0.03)
    print('rules is', rules)
