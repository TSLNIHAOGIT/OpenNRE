import json

all_name_set=set()
def get_name_dict(read_path):
    with open(read_path,encoding='utf8') as f:
        data=json.load(f)
        for each in data:
            head_name=each['head']['word']
            tail_name=each['tail']['word']
            all_name_set.add(head_name)
            all_name_set.add(tail_name)
    return all_name_set

if __name__=='__main__':
    p1='../data/train_people.json'
    p2='../data/dev_people.json'
    set_dict1=get_name_dict(p1)
    set_dict2 = get_name_dict(p2)
    all_set=set_dict1|set_dict2

    with open('../data/self_dict.txt',mode='w+',encoding='utf8') as f:
       f.write('\n'.join(list(all_set)))
        # json.dump(list(all_set),f,ensure_ascii=False)

