import json
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



with open('nyt_pcnn_att_pred_new.json') as f:
    list_pred=json.load(f)
    print(len(list_pred))
    for index,each in enumerate(list_pred):
        if each['relation']!=0:
            print(each)
            print(test_label_new[each['entpair']])
            print('\n')

        # if index>5:
        #     break
