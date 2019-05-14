import json
import pandas as pd
import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname('__file__'),'..')))
from data_process_ner_reg.df_eg import merge_dup_id
''':START_ID	role	:END_ID
'''
# train_people.json
# label_test_relation_split.json
with open('../data/train_people.json',encoding='utf8') as f:
    test_label_new={}
    word_ll={}
    all_wrod_ll=[]
    test_label=json.load(f)
    # print(' test_label', test_label)
    for each in test_label:
        # id=each['head']['id']+'#'+each['tail']['id']
        # pair_etity=(each['head']['id'],each['tail']['id'])

        id = each['head']['id'] + '#' + each['tail']['id']
        pair_etity = (each['head']['word'], each['tail']['word'])

        test_label_new[id]=pair_etity
        # print('test_label_new',test_label_new)
        # break

        word_ll['entityid:ID'] = each['head']['word']
        word_ll['myentity']=each['head']['word']#,each['tail']['word']

        # word_ll[':LABEL']=each['head']['label']
        word_ll[':LABEL'] = 'PER'

        all_wrod_ll.append(word_ll)
        word_ll = {}
        word_ll['entityid:ID'] = each['tail']['word']
        word_ll['myentity'] = each['tail']['word']  # ,each['tail']['word']
        # word_ll[':LABEL'] = each['tail']['label']
        word_ll[':LABEL'] = 'PER'

        all_wrod_ll.append(word_ll)
        word_ll = {}
all_wrod_ll_df=pd.DataFrame(data=all_wrod_ll).drop_duplicates()
print('all_wrod_ll_df',all_wrod_ll_df.head(10))

# print('all_wrod_ll_df shape',all_wrod_ll_df.shape)
# print('all_wrod_ll_df[entity:ID].nunique()',all_wrod_ll_df['entity:ID'].nunique())


all_wrod_ll_df=merge_dup_id(all_wrod_ll_df,col=['entityid:ID', 'myentity',':LABEL'])
print('df_final\n',all_wrod_ll_df.head(10))

##可以只用一个包含所有label的大表或者多用几个小表
all_wrod_ll_df.to_csv('all_labels.csv',columns=['entityid:ID','myentity',':LABEL'],index=False)



# ##neo4j导入识别，看log是标注的问题，同一个实体，在不同的位置，
# # 有点有的label是org有的label是Loc
# #此种情况是同一个实体有多个label,要用逗号分隔
#
# per_df=all_wrod_ll_df[all_wrod_ll_df[':LABEL']=='PER']
# loc_df=all_wrod_ll_df[all_wrod_ll_df[':LABEL']=='LOC']
# org_df=all_wrod_ll_df[all_wrod_ll_df[':LABEL']=='ORG']
# other_df=all_wrod_ll_df[ (all_wrod_ll_df[':LABEL']!='PER')&(all_wrod_ll_df[':LABEL']!='LOC')&(all_wrod_ll_df[':LABEL']!='ORG')]
#
# per_df.to_csv('per.csv',columns=['entity:ID','entity',':LABEL'],index=False)
# loc_df.to_csv('loc.csv',columns=['entity:ID','entity',':LABEL'],index=False)
# org_df.to_csv('org.csv',columns=['entity:ID','entity',':LABEL'],index=False)
# other_df.to_csv('other.csv',columns=['entity:ID','entity',':LABEL'],index=False)
#
#

# def create_nodes_by_label(test_label):
#     {''}
#     pass


with open('../data/rel2id_people.json',encoding='utf8') as f:
    rel_dict=json.load(f)
    rel_new={value:key for key,value in rel_dict.items()}
    print('rel_new',rel_new)


''':START_ID	role	:END_ID
'''

with open('../test_result/nyt_pcnn_att_pred_train.json',encoding='utf8') as f:
    list_pred=json.load(f)
    print(len(list_pred))
    all_data=[]

    for index,each in enumerate(list_pred):
        each_entitiy_pair = {}

        #当预测全为0时，就不走下面流程了
        if each['relation']!=0:
            print('each',each)
            print('test_label_new',test_label_new[each['entpair']],rel_new[each['relation']])
            print('\n')
            each_entitiy_pair[':START_ID']=test_label_new[each['entpair']][0]
            each_entitiy_pair[':END_ID'] = test_label_new[each['entpair']][1]
            each_entitiy_pair[':TYPE'] = rel_new[each['relation']]
            all_data.append(each_entitiy_pair)

df=pd.DataFrame(data=all_data).drop_duplicates()


#简化人物关系显示
def process_rel(line):
    line_split=line.split('/')
    print(line_split)
    return line_split[-1]
df[':TYPE']=df[':TYPE'].apply(lambda x:process_rel(x))

print('df',df.head())
df.to_csv('entity_pair_relations.csv',columns=[':START_ID',':END_ID',':TYPE'],index=False)
print(df.drop_duplicates())




