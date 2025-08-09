from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json, os

app = FastAPI(
    title="Slide Finder Mock API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


DATA_PATH = os.getenv("MOCK_DATA", os.path.join(os.path.dirname(__file__), "mock_data.json"))
with open(DATA_PATH, "r", encoding="utf-8") as f:
    MOCK = json.load(f)

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    filters: Optional[Dict[str, Any]] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/search")
def search(req: SearchRequest):
    q = (req.query or "").lower().strip()
    results = []
    for item in MOCK:
        title = item.get("title", "").lower()
        score = item.get("score", 0.5)
        # very naive relevance boost: contains query => +0.1
        if q and q in title:
            score = min(0.99, score + 0.1)
        out = dict(item)
        out["score"] = round(score, 2)
        results.append(out)
    # sort by score desc and cut
    results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)[: req.top_k]
    return results

@app.post("/index")
def index(payload: dict = Body(...)):
    # Mock: just echo back
    return {"received": True, "slides_count": len(payload.get("slides", []))}
