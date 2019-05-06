from sklearn.externals import joblib
import json
import pickle
import pandas as pd
import thulac
import numpy as np
import json
# # 生成词向量
# thu1 = thulac.thulac(seg_only=True)  #默认模式
# text = thu1.cut("工商注册地、税务征管关系及统计关系在广州市南沙区范围内", text=True)  #进行一句话分词
# print(text)

def get_pretrained_vec():
    vocabu2id=joblib.load('../open_data/vocabulary2id.pkl')
    # df=pd.read_csv('../data/train_people_relation.txt',delimiter='\t')
    # print(df['rel'].value_counts())




    # for each in df['sentence'].head():
    #     print(each)

    # with open('../data/sgns.baidubaike.bigram-char',encoding='utf8') as f:
    #     all_lines=f.read()
    #     all_lines_split=all_lines.split('\n')
    #     print(len(all_lines_split))





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
                if each[0] in vocabu2id:
                    word_dict['word']=each[0]
                    word_dict['vec']=each[1:]
                    word_vec_new.append(word_dict)
                if index%50000==0:
                    print('index={},word_dict={}'.format(index,word_dict))
    print('len word_vec_new',len(word_vec_new))
    print('word_vec_new\n',word_vec_new[0:10])
    print('开始保存文件')


    with open('../data/word_vec_people.json','w',encoding='utf8') as f:
        #两种效果一样
        ## f.write(json.dumps(all_rel_data,indent=4))
        json.dump(word_vec_new,f,ensure_ascii=False)



    # with open('../data/word_vec_people.pkl','wb') as f:
    #     #两种效果一样
    #     ## f.write(json.dumps(all_rel_data,indent=4))
    #     # json.dump(word_vec_new,f,ensure_ascii=False)
    #     pickle.dump(word_vec_new,f)

    # with open('../data/word_vec_people.pkl', 'rb') as f:
    #      data = pickle.load(f)
    #      print(data)

def convert_people_train():
    path = '../open_data/sent_dev.txt'
    df=pd.read_csv(path,delimiter='\t',header=-1,names=['id','e1','e2','sentence'])
    print(df.head())

    df_rel=pd.read_csv('../open_data/sent_relation_dev.txt',delimiter='\t',header=-1,names=['rel_id','class'])
    print('df_rel.head',df_rel.head())
    with open('../data/rel2id_people.json',encoding='utf8') as f:
      rel2id=json.load(f)
      id2rel={}
      for k,v in rel2id.items():
          # print(type(k),type(v))
          id2rel[v]=k
    print('id2rel',id2rel)
    # df_rel['class'].apply(lambda row: print(type(row),row))
    def id2rel_process(class_input):
        # print('type',type(class_input),class_input)
        return  id2rel[int(class_input)]

    df_rel['rel']=df_rel['class'].apply(lambda row:id2rel_process(row))
    print('df_rel.tail\n',df_rel.tail())
    rel_class_id={}
    for index ,row in df_rel.iterrows():
        rel_class_id[row['rel_id']]=row['rel']

    # with open('../data/rel_class_id.json', 'w', encoding='utf8') as f:
    # # #两种效果一样
    #     ## f.write(json.dumps(all_rel_data,indent=4))
    #     json.dump(rel_class_id,f,ensure_ascii=False,indent=4)

    print('rel_class_id\n',rel_class_id)
    all_train=[]
    for index,row in df.iterrows():
        print('row',row['id'],rel_class_id[row['id']])
        each_train={}
        each_train['head']={'id':row['id'],'word':row['e1']}
        each_train['relation']=rel_class_id[row['id']]
        each_train['sentence']=row['sentence']
        each_train['tail']={'id':row['id'],'word':row['e2']}
        # print('each_train',each_train)
        all_train.append(each_train)

    with open('../data/dev_people.json','w',encoding='utf8') as f:
        #两种效果一样
        ## f.write(json.dumps(all_rel_data,indent=4))
        json.dump(all_train,f,ensure_ascii=False,indent=4)
        #显示比较少时前面的关系确实都为NA，转换程序并没有错




    pass
def convert_people_rel2id():
    rel2id_people={}
    path = '../open_data/relation2id.txt'
    df = pd.read_csv(path, delimiter='\t',header=-1,names=['relation','class'])
    print('df',df)
    for index,each in df.iterrows():
        rel2id_people[each['relation']]=each['class']
    with open('../data/rel2id_people.json','w',encoding='utf8') as f:
        #两种效果一样
        ## f.write(json.dumps(all_rel_data,indent=4))
        json.dump(rel2id_people,f,ensure_ascii=False)

    pass
if __name__=='__main__':
    # convert_people_rel2id()
    convert_people_train()

    # with open('../data/train_people.json',encoding='utf8') as f:
    #     # 两种效果一样
    #     ## f.write(json.dumps(all_rel_data,indent=4))
    #     list_data=json.load(f)
    #     print(list_data[-10:-1])
    pass

