import json
path='test.json'
# with open(path) as f:
#     list_data=json.load(f)
#     print(len(list_data))
#     for index, each in enumerate(list_data):
#         if index<5:
#             print(each)

path='../label_test_relation.json'
'''
test 172448
'''
with open(path) as f:
    list_data=json.load(f)
    print(len(list_data))
    # print('list_data 0',list_data[0],'\n','list_data -1',list_data[-1])
    # for index, each in enumerate(list_data):
    #     if index<5:
    #         print(each)