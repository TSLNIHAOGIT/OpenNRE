
import json
# df=pd.read_csv('../data/train_people_relation.txt',delimiter='\t')
# print(df['rel'].value_counts())


# for each in df['sentence'].head():
#     print(each)
word_vec_new=[]
with open('../data/sgns.baidubaike.bigram-char',encoding='utf8') as f:

    for index ,each0 in enumerate(f):
        word_dict = {}
        if index==0:
            print('index=0,each',each0)
            continue

        # if index>30:
        #     break
        #     print(each0)
        each=each0.strip().split(' ')

        # print('each:',len(each),each[0],len(each[1:]))
        # print(len(each),each[0],each[1:])
        if len(each[1:])!=300:
            print(index,len(each[1:]))
            print(each0)
            continue
        else:
            word_dict['word']=each[0]
            word_dict['vec']=each[1:]
            word_vec_new.append(word_dict)
print('开始保存文件')
with open('../data/word_vec_new.json','w',encoding='utf8') as f:
    #两种效果一样
    ## f.write(json.dumps(all_rel_data,indent=4))
    json.dump(word_vec_new,f,ensure_ascii=False)

