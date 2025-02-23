import json
import torch

from tqdm import tqdm
from typing import List
from pprint import pprint
from utils import get_es_client
from elasticsearch import Elasticsearch
from config import INDEX_NAME_EMBEDDING

from sentence_transformers import SentenceTransformer


def index_data(documents: List[dict], model: SentenceTransformer) -> None:
    es = get_es_client(max_retries=1, sleep_time=0)
    _ = _create_index(es=es)
    _ = _insert_documents(es=es, documents=documents, model=model)

    pprint(
        f'Indexed {len(documents)} documents into Elasticsearch index "{INDEX_NAME_EMBEDDING}"'
    )


# ElasticSearch will not be able to infer the embedding mappings like JSON, so we need to specify the mapping explicitly.
def _create_index(es: Elasticsearch) -> dict:
    _ = es.indices.delete(index=INDEX_NAME_EMBEDDING, ignore_unavailable=True)
    return es.indices.create(
        index=INDEX_NAME_EMBEDDING,
        mappings={
            "properties": {
                "embedding": {
                    "type": "dense_vector",
                }
            }
        },
    )


def _insert_documents(
    es: Elasticsearch, documents: List[dict], model: SentenceTransformer
) -> dict:
    operations = []
    for document in tqdm(documents, total=len(documents), desc="Indexing documents"):
        operations.append({"index": {"_index": INDEX_NAME_EMBEDDING}})
        operations.append(
            {**document, "embedding": model.encode(document["explanation"])}
        )
    return es.bulk(operations=operations)


if __name__ == "__main__":
    with open("../../../data/apod.json") as f:
        documents = json.load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SentenceTransformer("all-MiniLM-L6-v2").to(device)
    index_data(documents=documents, model=model)
