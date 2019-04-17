import pandas as pd
import json

def data_process(rel=None):
    rel_data=list(relat_process())
    with open('../data/train.json') as f:
        json_data=json.load(f)
        times=0
        for each in json_data:
            #'/people/place_of_interment/interred_here','/time/event/locations',
            if each['relation'] in ['/business/shopping_center_owner/shopping_centers_owned']:#rel_data:
                # rel_data.remove(each['relation'])
                print('times:',times)
                print('sentence::',each['sentence'])
                print('head entity::',each['head']['word'])
                print('relation::',each['relation'])
                print('tail entity::',each['tail']['word'])
                print('\n')
                times=times+1

        # print(json_data)
        # df=pd.DataFrame(data=json_data)
        # print(df.head())

# with open('../../test_result/nyt_pcnn_att_pred.json') as f:
#     json_data=json.load(f)
#     for each in json_data:
#         print(each)
#         break
import re
def multiple_replace(text, adict):
     rx = re.compile('|'.join(map(re.escape, adict)))
     def one_xlat(match):
           return adict[match.group(0)]
     return rx.sub(one_xlat, text)

#BIOES
def entity_single_label(entity_single,entity_type):
         each_list=entity_single.split()
         entity_length=len(each_list)
         if entity_length==1:
             entity_new='{}___S-{}'.format(entity_single,entity_type)
         elif entity_length==2:
             entity_new='{}___B-{} {}___E-{}'.format(each_list[0],entity_type,each_list[1],entity_type)
         else:
             each_list_new=[]
             for index, each in enumerate(each_list):
                 if index==0:
                     each_list_new.append('{}___B-{}'.format(each_list[index],entity_type))
                 elif index<entity_length-1:
                     each_list_new.append('{}___I-{}'.format(each_list[index],entity_type))
                 else:
                     each_list_new.append('{}___E-{}'.format(each_list[index],entity_type))
             entity_new=' '.join(each_list_new)
         return entity_new

def entpair_type(head_Entity,head_Entity_type,tail_Entity,tail_Entity_type):
    head_Entity_new = entity_single_label(head_Entity, head_Entity_type)
    tail_Entity_new = entity_single_label(tail_Entity, tail_Entity_type)
    return {head_Entity: head_Entity_new, tail_Entity: tail_Entity_new}


rela_headtype_tailtype={
    '/location/location/contains':('LOC','LOC'),
    '/people/person/nationality':('PER','LOC'),
    '/people/person/place_of_birth':('PER','LOC'),
    '/people/deceased_person/place_of_death':('PER','LOC'),
    '/people/person/place_lived':('PER','LOC'),
    '/business/company/founders':('ORG','PER'),
    '/people/person/ethnicity':('PER','LOC'),
    '/location/neighborhood/neighborhood_of':('LOC','LOC'),
    '/business/person/company':('PER','ORG'),
    '/location/administrative_division/country':('LOC','LOC'),
    '/business/company/place_founded':('ORG','LOC'),
    '/location/country/administrative_divisions':('LOC','LOC'),
    '/location/country/capital':('LOC','LOC'),
    '/people/person/children':('PER','PER'),
    '/people/person/religion':('PER','ORG'),
    '/business/company/major_shareholders':('ORG','PER'),
    '/people/ethnicity/geographic_distribution':('PER','LOC'),
    '/sports/sports_team/location':('ORG','LOC'),
    '/people/person/profession':('PER','ORG'),
    '/business/company/advisors':('ORG','PER'),
    '/location/us_county/county_seat':('LOC','LOC'),
    '/film/film/featured_film_locations':('MISC','LOC'),
    '/people/ethnicity/included_in_group':('PER','PER'),
    '/people/place_of_interment/interred_here':('LOC','PER'),
    '/time/event/locations':('MISC','LOC'),
    '/location/de_state/capital':('LOC','LOC'),
    '/location/us_state/capital':('LOC','LOC'),
    '/business/company_advisor/companies_advised':('PER','ORG'),
    '/people/deceased_person/place_of_burial':('PER','LOC'),
    '/broadcast/content/location':('ORG','LOC'),
    '/film/film_festival/location':('MISC','LOC'),
    '/location/it_region/capital':('LOC','LOC'),
    '/business/shopping_center_owner/shopping_centers_owned':('ORG','ORG'),
    '/location/in_state/legislative_capital':('LOC','LOC'),
    '/location/in_state/administrative_capital':('LOC','LOC'),
    '/business/business_location/parent_company':('LOC','ORG'),
    '/people/family/members':('PER','PER'),
    '/location/jp_prefecture/capital':('LOC','LOC'),
    '/film/film_location/featured_in_films':('LOC','PER'),
    '/people/family/country':('PER','LOC'),
    '/business/company/locations':('ORG','LOC'),
    '/people/profession/people_with_this_profession':('PER','PER'),
    '/location/br_state/capital':('LOC','LOC'),
    '/location/cn_province/capital':('LOC','LOC'),
    '/broadcast/producer/location':('ORG','LOC'),
    '/location/fr_region/capital':('LOC','LOC'),
    '/location/province/capital':('LOC','LOC'),
    '/location/in_state/judicial_capital':('LOC','LOC'),
    '/business/shopping_center/owner':('ORG','ORG'),
    '/location/mx_state/capital':('LOC','LOC'),
    '/location/country/languages_spoken':('LOC','MISC'),
    '/base/locations/countries/states_provinces_within':('LOC','LOC'),
    'NA':('MISC','MISC')
}

def entpair_label(head_Entity,tail_Entity,relation):
    entity_head_tail_type=rela_headtype_tailtype[relation]
    return entpair_type(head_Entity, entity_head_tail_type[0], tail_Entity, entity_head_tail_type[1])





def relat_process():
    with open('../data/rel2id.json') as f:
        json_data=json.load(f)
        # for each in json_data:
        #     print('rel:',each)
        print(json_data.keys())
        return json_data.keys()
def construct_Entity_label_Bioes():
    with open('../data/test.json') as f:
        json_data = json.load(f)
        for each in json_data:
            relation = each['relation']
            sentence=each['sentence']
            head_Entity=each['head']['word']
            tail_Entity=each['tail']['word']
            # if relation == 'NA':
            #     print('sentence::', each['sentence'])
            #     print('head entity::', each['head']['word'])
            #     print('relation::', each['relation'])
            #     print('tail entity::', each['tail']['word'])
            #     continue
            # print(entpair_label(head_Entity, tail_Entity, relation))
            entity_dict=entpair_label(head_Entity, tail_Entity, relation)
            new_sentence=multiple_replace(sentence, entity_dict)
            print('sentence',new_sentence)
            for each in new_sentence.split(' '):
                if '___' not in each :
                    print('{} o'.format(each))
                else:
                    print(each.replace('___',' '))
            break
            # print('\n\n\n')











if __name__=='__main__':
    # relat_process()
    # data_process()
    # entity_single='amy like dogs very much'
    # print(entity_single_label(entity_single,'LOC'))

    construct_Entity_label_Bioes()