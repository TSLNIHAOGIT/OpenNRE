import json
import pandas as pd
''':START_ID	role	:END_ID
'''
with open('../data/label_test_relation_new.json') as f:
    test_label_new={}
    word_ll={}
    all_wrod_ll=[]
    test_label=json.load(f)
    # print(' test_label', test_label)
    for each in test_label:
        id=each['head']['id']+'#'+each['tail']['id']
        pair_etity=(each['head']['id'],each['tail']['id'])
        test_label_new[id]=pair_etity
        # print('test_label_new',test_label_new)
        # break

        word_ll['entity:ID'] = each['head']['id']
        word_ll['entity']=each['head']['word']#,each['tail']['word']
        word_ll[':LABEL']=each['head']['label']

        all_wrod_ll.append(word_ll)
        word_ll = {}
        word_ll['entity:ID'] = each['tail']['id']
        word_ll['entity'] = each['tail']['word']  # ,each['tail']['word']
        word_ll[':LABEL'] = each['tail']['label']
        all_wrod_ll.append(word_ll)
        word_ll = {}
all_wrod_ll_df=pd.DataFrame(data=all_wrod_ll)
print('all_wrod_ll_df',all_wrod_ll_df.head(20))

per_df=all_wrod_ll_df[all_wrod_ll_df[':LABEL']=='PER']
loc_df=all_wrod_ll_df[all_wrod_ll_df[':LABEL']=='LOC']
org_df=all_wrod_ll_df[all_wrod_ll_df[':LABEL']=='ORG']

per_df.to_csv('per.csv',index=False)
loc_df.to_csv('loc.csv',index=False)
org_df.to_csv('org.csv',index=False)




# def create_nodes_by_label(test_label):
#     {''}
#     pass


with open('../data/rel2id.json') as f:
    rel_dict=json.load(f)
    rel_new={value:key for key,value in rel_dict.items()}
    print('rel_new',rel_new)


''':START_ID	role	:END_ID
'''

with open('../test_result/nyt_pcnn_att_pred_new.json') as f:
    list_pred=json.load(f)
    print(len(list_pred))
    all_data=[]

    for index,each in enumerate(list_pred):
        each_entitiy_pair = {}
        if each['relation']!=0:
            print(each)
            print(test_label_new[each['entpair']],rel_new[each['relation']])
            print('\n')
            each_entitiy_pair[':START_ID']=test_label_new[each['entpair']][0]
            each_entitiy_pair[':END_ID'] = test_label_new[each['entpair']][1]
            each_entitiy_pair['entity_relation'] = rel_new[each['relation']]
            all_data.append(each_entitiy_pair)

df=pd.DataFrame(data=all_data).drop_duplicates()
df.to_csv('entity_pair_relations.csv',index=False)
# print(df.drop_duplicates())


        # if index>5:
        #     break
