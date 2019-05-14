# sentence='As a teenager , he studied in Florence with Pietro Annigoni , a painter -LRB- known for his portrait of the young Elizabeth II -RRB- who initiated Cammell into his milieu of sex and drugs .'
# head_entity='Pietro Annigoni'
# # relation:: /people/deceased_person/place_of_death
# tail_entity='Florence'
# # sentence=sentence.replace(head_entity,'***_head')
# # sentence=sentence.replace(tail_entity,'***_tail')
# def entity_label(entity):
#     length=entity.split(' ')
#     if length==1:
#         return '{} S'.format(entity)
#     elif length==2:
#         return
#
# head_entity_len = len(head_entity.split(' '))
# tail_entity_len = len(tail_entity.split(' '))
# print('head_entity_len',head_entity_len)
# print('tail_entity_len',tail_entity_len)
#
# sentence_entity_split = sentence.split(' ')
# for each_word in sentence_entity_split:
#     # print(each_word)
#     if each_word not in head_entity and each_word not in tail_entity:
#         print(each_word,'O')
#     else:
#         # if head_entity_len==1 :
#
#         print(each_word,"***")

# sentence=list('张 韶 hj涵')
#
# print(sentence)
# print(len(sentence))

import pandas as pd
df=pd.read_csv('entity_pair_relations.csv')
print(df.head())

def process_rel(line):
    line_split=line.split('/')
    print(line_split)
    return line_split[-1]
df[':TYPE']=df[':TYPE'].apply(lambda x:process_rel(x))

df.to_csv('entity_pair_relations_new.csv',index=False)
print(df.head())