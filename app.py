from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import httpx

app = FastAPI()

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/classify")
async def classify(name: str = Query(None)):

    # 400 — missing or empty
    if name is None or name.strip() == "":
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Missing or empty name parameter"}
        )

    # 422 — not a valid string (e.g. a number passed as name)
    try:
        float(name)
        return JSONResponse(
            status_code=422,
            content={"status": "error", "message": "name must be a string"}
        )
    except ValueError:
        pass

    # Call Genderize
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.genderize.io",
                params={"name": name},
                timeout=5.0
            )
            response.raise_for_status()
            data = response.json()

    except httpx.TimeoutException:
        return JSONResponse(status_code=502, content={"status": "error", "message": "Upstream API timed out"})
    except httpx.HTTPStatusError:
        return JSONResponse(status_code=502, content={"status": "error", "message": "Upstream API returned an error"})
    except Exception:
        return JSONResponse(status_code=500, content={"status": "error", "message": "Server error"})

    # Edge case — Genderize couldn't predict
    if data.get("gender") is None or data.get("count") == 0:
        return JSONResponse(
            status_code=422,
            content={"status": "error", "message": "No prediction available for the provided name"}
        )

    # Process
    probability = data["probability"]
    sample_size = data["count"]
    is_confident = probability >= 0.7 and sample_size >= 100

    return {
        "status": "success",
        "data": {
            "name": data["name"],
            "gender": data["gender"],
            "probability": probability,
            "sample_size": sample_size,
            "is_confident": is_confident,
            "processed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    }