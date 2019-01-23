import efficient_apriori
import pandas as pd
import numpy as np

df_new = pd.read_csv('./data/df_new_data.csv')
print('df.shape is ', df_new.shape)
print('df_new.head(10) is ', df_new.head(10))