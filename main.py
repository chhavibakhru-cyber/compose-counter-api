from fastapi import FastAPI
import redis
import os

app = FastAPI()


REDIS_URL = os.getenv("REDIS_URL")

r = redis.from_url(
    REDIS_URL,
    decode_responses=True
)
@app.post("/hit/{key}")
def hit(key: str):
    count = r.incr(key)
    return {"key": key, "count": count}

@app.get("/count/{key}")
def count(key: str):
    value = r.get(key)
    return {"key": key, "count": int(value) if value else 0}

    
@app.get("/healthz")
def health():
    try:
        r.ping()
        return {
            "status": "ok",
            "redis": "up"
        }
    except Exception as e:
        return {
            "status": "error",
            "redis": "down",
            "message": str(e)
        }

from fastapi import Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

# allow CORS (required by grader)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ASSIGNED_KEY = "ak_33tsx64lvwg375014ppc45j6"
YOUR_EMAIL = "25f1002355@ds.study.iitm.ac.in"  

@app.post("/analytics")
async def analytics(request: Request, x_api_key: str = Header(None)):
    
    # 🔴 MUST FAIL ON WRONG KEY
    if x_api_key != ASSIGNED_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()
    events = data.get("events", [])

    total_events = len(events)

    users = set()
    revenue = 0
    user_totals = {}

    for e in events:
        user = e.get("user")
        amount = e.get("amount", 0)

        users.add(user)

        if amount > 0:
            revenue += amount
            user_totals[user] = user_totals.get(user, 0) + amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else None

    return {
        "email": "25f1002355@ds.study.iitm.ac.in",
        "total_events": total_events,
        "unique_users": len(users),
        "revenue": revenue,
        "top_user": top_user
    }