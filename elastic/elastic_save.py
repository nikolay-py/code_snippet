"""Create a save request and send it."""
import json
from logging import getLogger
from typing import Any, Dict, Tuple, TypedDict

from elastic.elastic_client import (connect_elasticsearch,
                                    create_index,
                                    store_record)

from elasticsearch import Elasticsearch


LOGGER = getLogger(__name__)

Tags_dict = TypedDict('Tags_dict', {
    'tag': str,
    'confidence': float,
})


def create_elastic_index(client_id: int) -> bool:
    """Create index as client id."""
    es: Elasticsearch = connect_elasticsearch()
    index_name = str(client_id)
    if es is not None:
        created = create_index(es, index_name)
        return created
    else:
        LOGGER.debug('Elastic.Clients id index elastic not created: No connection to Elasticsearch')
    return False


def convert_dict_to_text(tags: Tags_dict) -> str:
    """Convert tags dictionary to text."""
    tags_text = ''
    if tags:
        for tag in tags:
            tags_text = tags_text + ' ' + str(tag['tag'])
        return tags_text
    return


def create_record_object(incom_param: Dict[str, Any]) -> Tuple:
    """Create record and save it."""
    index_name = incom_param['index_name']
    tags_text = convert_dict_to_text(incom_param['tags'])
    id_doc = str(incom_param['image_uuid'])
    record_dict = {
        'description': str(incom_param['description']),
        'tags': tags_text,
        'image_uuid': id_doc,
        'path': str(incom_param['path']),
        'lang': str(incom_param['lang']),
        'project_name': str(incom_param['project_name']),
    }
    record_json = json.dumps(record_dict)
    return index_name, record_json, id_doc


def save_in_elastic(incom_param: Dict[str, Any]) -> bool:
    """Convert request to json and write to index."""
    index_name, record, id_doc = create_record_object(incom_param)
    es: Elasticsearch = connect_elasticsearch()
    if es is not None:
        if create_index(es, index_name):
            is_stored = store_record(es, index_name, record, id_doc=id_doc)
            return is_stored
    return False
