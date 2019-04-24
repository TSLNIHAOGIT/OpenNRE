import pandas as pd
df = pd.DataFrame({'id': ['001', '002', '001','003','001'],
                   'label': ['a', 'b', 'c','d','f'],
                   'entity': ['aa', 'bb', 'aa','dd','aa']},
                  columns=['id', 'label','entity'])
print(df)
# df_merge = df.groupby('id')['counts'].sum()
# # df_merge = df['counts'].groupby(df['id']).sum()
# print(df_merge)

# def max(input):
#     return '11'
# df_merge2 = df.groupby('id').agg({'counts':['sum',max],'counts2':['sum','max']}).reset_index()
# print('df_merge2',df_merge2)

# df.groupby('id').agg(lambda col:print('col:\n',col))
#
# df.groupby('id').apply(lambda df:print('df:\n',df))

def id_merge(col):
    new=[]
    col_length=len(col)
    if col_length==1:
        return col
    elif col_length>1:
        for each in col:
            new.append(each)
        return ';'.join(new)
# #[id_merge]会增加层级
# df_merge2 = df.groupby('id').agg({'label':id_merge}).reset_index()
# print('df_merge2\n\n',df_merge2)
#
# df2=df[['id','entity']].drop_duplicates()
# print(df2)
#
# df_final=pd.merge(df_merge2,df2,how='inner',on='id')
# print(df_final)

def merge_dup_id(df,col=['id', 'entity','label']):
    df_merge2 = df.groupby(col[0]).agg({col[2]: id_merge}).reset_index()
    df2 = df[col[0:2]].drop_duplicates()
    df_final = pd.merge(df_merge2, df2, how='inner', on=col[0])
    return df_final

if __name__=='__main__':
    print(merge_dup_id(df,['id', 'entity','label']))



