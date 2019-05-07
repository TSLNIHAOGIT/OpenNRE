import pandas as pd
df=pd.read_csv('all_labels.csv')
df['myid:ID']=df['myent']
df.to_csv('all_labels_new.csv',index=False)

# print(df.head())
# print(df.shape)
# name='entity:ID'
# print(df[name].head())
# print(df[name].shape)
# print(df[name].nunique())