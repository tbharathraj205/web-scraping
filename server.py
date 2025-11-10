
from fastapi import FastAPI, Header, HTTPException
from main import run_scrape

API_KEY = "mysecret123"

app = FastAPI()

def check_key(key):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/search")
def api_search(query: str, max_results: int = 5, x-api-key: str = Header(None)):
    check_key(x-api-key)
    return run_scrape(query, max_results)
