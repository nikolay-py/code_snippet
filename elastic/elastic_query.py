"""Form a request object and send it."""
import json
from logging import getLogger
from typing import Dict, Union

from elastic.elastic_client import connect_elasticsearch, search_record

from elasticsearch import Elasticsearch

LOGGER = getLogger(__name__)


def create_connect_and_search_record(index_name: str,
                                     search_object: json) -> Union[Dict, bool]:
    """Create connect and search records in elastic database."""
    es: Elasticsearch = connect_elasticsearch()
    if es is not None:
        query_result = search_record(es, index_name, search_object)
        return query_result
    return False


def get_search_result(index_name: str, query_text: Dict) -> Dict:
    """Get search results."""
    search_object = create_search_object(query_text)
    search_result = create_connect_and_search_record(index_name, search_object)
    if search_result:
        return search_result['hits']['hits']
    return {'Note': 'No connection to the search service'}


def create_search_object(query_text: Dict) -> json:
    """Create search object."""
    search_object_dict = {
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
    search_object_json = json.dumps(search_object_dict)
    return search_object_json
