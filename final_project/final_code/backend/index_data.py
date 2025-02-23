# Insert all document from ../data/apod.json to elastic search

import json
from pprint import pprint
from typing import List

from elasticsearch import Elasticsearch
from tqdm import tqdm
from config import INDEX_NAME_DEFAULT, INDEX_NAME_N_GRAM
from utils import get_es_client


def index_data(documents: List[dict]) -> None:
    es = get_es_client(max_retries=5, sleep_time=5)
    _ = _create_index(es=es)
    _ = _insert_documents(es=es, documents=documents)
    pprint(
        f'Indexed {len(documents)} documents to Elasticsearch for index "{INDEX_NAME_DEFAULT}"'
    )


def _create_index(es: Elasticsearch) -> dict:
    es.indices.delete(index=INDEX_NAME_DEFAULT, ignore_unavailable=True)
    return es.indices.create(index=INDEX_NAME_DEFAULT)


def _insert_documents(es: Elasticsearch, documents: List[dict]) -> dict:
    operations = []
    index_name = INDEX_NAME_DEFAULT
    for document in tqdm(documents, total=len(documents), desc="Indexing documents"):
        operations.append({"index": {"_index": index_name}})
        operations.append(document)
    return es.bulk(operations=operations)


if __name__ == "__main__":
    with open("../../../data/apod.json") as f:
        documents = json.load(f)

    index_data(documents=documents)
