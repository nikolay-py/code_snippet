from logging import getLogger
from typing import Any, Dict, List, Type, Union

from elastic.elastic_settings import elastic_settings

from elasticsearch import Elasticsearch

from app_backend.exceptions.invalid_api_usage import InvalidAPIUsage
from app_backend.entity.exception_enum import ExceptionEnum

LOGGER = getLogger(__name__)
JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]


def connect_elasticsearch() -> Elasticsearch:
    """Connect."""
    _es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
    if _es.ping():
        LOGGER.info('Elasticsearch connection is set up')
    else:
        _es = None
        LOGGER.debug('No connection to Elasticsearch!')
    return _es


def create_index(es_object: Elasticsearch, index_name: str) -> bool:
    """Create index."""
    created = False
    settings = elastic_settings

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            outcome = es_object.indices.create(index=index_name, body=settings)
            LOGGER.info(f'Elastic.Created new Index {outcome}')

        created = True
        LOGGER.info(f'Elastic.Index exists: {str(created)}')

    except Exception:
        LOGGER.exception(f'Elastic.Exception occurred while creating index {index_name}')

    return created


def create_index_alias(es_object: Elasticsearch, index_name: str, alias_name: str) -> bool:
    """Create or update an alias."""
    created = False
    alias_name = alias_name + '_alias'
    try:
        if es_object.indices.exists(index_name):
            outcome = es_object.indices.put_alias(index=index_name, name=alias_name)
            LOGGER.info(f'Elastic.Created new alias {outcome}')

        created = True
        LOGGER.info(f'Elastic.Alias exists: {str(created)}')

    except Exception:
        LOGGER.exception(f'Elastic.Exception occurred while creating alias {index_name}')

    return created


def delete_index(elastic_object: Elasticsearch, index_name: str) -> None:
    """Delete index."""
    outcome = elastic_object.indices.delete(index=index_name)
    LOGGER.info(f'Elastic.Index {index_name} deleted {outcome}')


def store_record(elastic_object: Elasticsearch,
                 index_name: str, record: JSON, id_doc: str) -> bool:
    """Save record."""
    is_stored = True
    try:
        outcome = elastic_object.index(index=index_name, id=id_doc, body=record)
        LOGGER.info(f'Elastic.data has been saved in the index {outcome}')
    except Exception as ex:
        LOGGER.exception(f'Elastic.Exception when saving record {str(ex)}')
        is_stored = False

    LOGGER.info(f'Elastic.Record saved in the index: {str(is_stored)}')
    return is_stored


def search_record(es_object: Elasticsearch, index_name: str, search: JSON) -> Dict:
    """Find records."""
    try:
        res = es_object.search(index=index_name, body=search)
        LOGGER.info('search results returned')
    except Exception:
        raise InvalidAPIUsage(ExceptionEnum.READ_ELASIC_PROBLEM)
    return res
