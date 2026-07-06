from fastapi import FastAPI
import redis
import os

app = FastAPI()

redis_host = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.get("/healthz")
def health():
    try:
        r.ping()
        return {"status": "ok", "redis": "up"}
    except Exception:
        return {"status": "error", "redis": "down"}

@app.post("/hit/{key}")
def hit(key: str):
    count = r.incr(key)
    return {"key": key, "count": count}

@app.get("/count/{key}")
def count(key: str):
    value = r.get(key)
    return {"key": key, "count": int(value) if value else 0}