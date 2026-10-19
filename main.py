import datetime
import urllib.parse
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Neotech AI Core Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

def execute_action(intent: str, text: str) -> Dict[str, Any]:
    t = text.lower()
    
    if "time" in t:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return {"reply": f"The current time is {now}.", "action": "none"}
    
    if "date" in t or "day" in t:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return {"reply": f"Today is {today}.", "action": "none"}
    
    if "play" in t or "youtube" in t:
        search_term = t.replace("play", "").replace("youtube", "").strip()
        encoded = urllib.parse.quote(search_term)
        return {
            "reply": f"Playing {search_term} on YouTube.",
            "action": "open_url",
            "url": f"https://www.youtube.com/results?search_query={encoded}"
        }
    
    if "search" in t or "google" in t:
        search_term = t.replace("search for", "").replace("search", "").replace("google", "").strip()
        encoded = urllib.parse.quote(search_term)
        return {
            "reply": f"Searching for {search_term}.",
            "action": "open_url",
            "url": f"https://www.google.com/search?q={encoded}"
        }

    if any(char in t for char in ["+", "-", "*", "/"]) and any(c.isdigit() for c in t):
        clean_expr = "".join([c for c in t if c in "0123456789+-*/.() "])
        try:
            result = eval(clean_expr)
            return {"reply": f"The answer is {result}.", "action": "none"}
        except Exception:
            pass

    return {
        "reply": f"Neotech AI processed: '{text}'. All systems operational.",
        "action": "none"
    }

@app.post("/api/chat")
async def process_chat(req: QueryRequest) -> Dict[str, Any]:
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Empty query")
    return execute_action("general", req.query)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)