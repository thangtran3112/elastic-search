from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import INDEX_NAME_DEFAULT
from utils import get_es_client

app = FastAPI()

# Make sure any server (including the frontend) can make requests to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/regular_search/")
async def search(search_query: str, skip: int = 0, limit: int = 10) -> dict:
    es = get_es_client(max_retries=1, sleep_time=0)
    query = {
        "bool": {
            "must": [
                {
                    "multi_match": {
                        "query": search_query,
                        "fields": ["title", "explanation"],
                    }
                }
            ]
        }
    }
    response = es.search(
        index=INDEX_NAME_DEFAULT,
        body={
            "query": query,
            "from": skip,
            "size": limit,
        },
        filter_path=[
            "hits.hits._source",
            "hits.hits._score",
            "hits.total",
        ],
    )
    return {
        "hits": response["hits"]["hits"],
    }
