from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

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
async def search(
    search_query: str,
    skip: int = 0,
    limit: int = 10,
    year: str | None = None,
) -> dict:
    try:
        es = get_es_client(max_retries=1, sleep_time=0)
        query = {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": search_query,
                            "fields": [
                                "title",
                                "explanation",
                            ],  # search_query text within title and explanation fields
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
    except Exception as e:
        return handle_error(e)


@app.get("/api/v1/get_docs_per_year_count/")
async def get_docs_per_year_count(search_query: str) -> dict:
    try:
        es = get_es_client(max_retries=1, sleep_time=0)
        query = {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": search_query,
                            "fields": [
                                "title",
                                "explanation",
                            ],  # search_query text within title and explanation fields
                        }
                    }
                ]
            }
        }
        index_name = INDEX_NAME_DEFAULT
        response = es.search(
            index=index_name,
            body={
                "query": query,
                "aggs": {
                    "docs_per_year": {
                        "date_histogram": {  # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html
                            "field": "date",
                            "calendar_interval": "year",  # Group by year
                            "format": "yyyy",  # Format the year in the response
                        }
                    }
                },
            },
            filter_path=["aggregations.docs_per_year"],
        )
        return {"docs_per_year": extract_docs_per_year(response)}
    except Exception as e:
        return handle_error(e)


def extract_docs_per_year(response: dict) -> dict:
    aggregations = response.get("aggregations", {})
    docs_per_year = aggregations.get("docs_per_year", {})
    buckets = docs_per_year.get("buckets", [])
    return {bucket["key_as_string"]: bucket["doc_count"] for bucket in buckets}


def handle_error(e: Exception) -> HTMLResponse:
    error_message = f"An error occurred: {str(e)}"
    return HTMLResponse(content=error_message, status_code=500)
