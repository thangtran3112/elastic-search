# FastAPI backend

## Data Scraper

* Scraped from [Nasa website](https://apod.nasa.gov/apod/archivepix.html) using BeautifulSoup

## Preparing the index

```zsh
  python3 index_data.py
```

## Serve the backend and frontend

```zsh
  cd backend
  pip install "fastapi[standard]"
  fastapi dev main.py
```

```zsh
  cd frontend
  npm run serve
```
