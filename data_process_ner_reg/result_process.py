import json
import pandas as pd
''':START_ID	role	:END_ID
'''
with open('../data/label_test_relation.json') as f:
    test_label_new={}
    test_label=json.load(f)
    # print(' test_label', test_label)
    for each in test_label:
        id=each['head']['id']+'#'+each['tail']['id']
        pair_etity=(each['head']['word'],each['tail']['word'])
        test_label_new[id]=pair_etity
        # print('test_label_new',test_label_new)
        # break
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
