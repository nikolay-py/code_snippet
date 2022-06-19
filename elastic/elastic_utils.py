from elasticsearch import Elasticsearch
from pprint import pprint
import json


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
system_index = ['.apm-agent-configuration', '.kibana_1', '.kibana_task_manager_1']


def users_log(result_var, text='Значение переменной'):
    delim_char = '='*60

    print(f"""
        {delim_char}
        {text}
        {result_var}
        {delim_char}""")


def list_index_alias():  # curl 'localhost:9200/_cat/indices?v&pretty'
    """Get list indices omit system_index."""
    list_index = []
    outcom = es.indices.get_alias('*')  # Отражает Индекс:Алиас
    # print(outcom)
    for key, val in outcom.items():
        # print(key, ':', val)
        if key not in list_index and key not in system_index:
            list_index.append(key)
    print(list_index)
    return list_index


def search_record(index_name, search_object):
    query_el = json.dumps(search_object)
    res = es.search(index=index_name, body=query_el)
                    # filter_path=['hits.hits._source'])  # Поиск в индексе, параметры запроса - в теле
    a = res['hits']['hits']
    # {'hits': {'hits': [{'_source':
    pprint(a)



def delete_index(index_name: str) -> None:
    """Delete index."""
    es.indices.delete(index=index_name)  # Удалить конкреный индекс
    users_log(index_name, 'Индекс удален')


def delet_all_indexs():
    """Delete all indices."""
    indices = list_index_alias()
    if indices:
        for index in indices:
            delete_index(index)


def list_idex_full():
    """Get full information about index."""
    outcom = es.indices.get('*')  # Отражает полную информацию об индексе
    # print(outcom)
    for key, val in outcom.items():
        # if key not in system_index:
        print(key)
            # pprint(val)


def query_to_elasticsearch_demo(query_text):
    """Create query for demo."""
    search_object = {
        'size': 5,
        'query': {
            'multi_match': {
                'query': str(query_text),
                'fields': [
                    'tags',
                    'description',
                    'custom_description',
                    'custom_tags',
                ],
            },
        },
    }
    return search_object

def query_to_elasticsearch_demo2(query_text):
    """Create query for demo."""
    search_object = {
        'size': 5,
        'query': {
            'bool': {
                'should': [
                    {'multi_match': {
                        'query': str(query_text),
                        'fields': [
                            'tags',
                            'description',
                            'custom_description',
                            'custom_tags',
                        ],
                    }},
                    {'regexp': {
                            'tags': {
                                # 'value': "j",
                                # 'value': "([a-z]+)",  # Черезе регулярку ищем все аглийские слова
                                'value': "([а-я]+)",  # Черезе регулярку ищем все русские слова
                                'flags': 'ALL',
                            },
                    }},
                ],
            },
        },
    }

    return search_object



def search_demo(index_name, query_text):

    search_object = query_to_elasticsearch_demo2(query_text)
    search_record(index_name, search_object)


if __name__ == '__main__':

    # index_name = '172.22.0.1python-requests2.26.0'
    # index_name = 'demo'
    # query_text = 'питомец'
    index_name = '7'
    query_text = 'pet'

    search_demo(index_name, query_text)

    # delete_index(index_name)
    list_index_alias()
    list_idex_full()

    # delet_all_indexs()
