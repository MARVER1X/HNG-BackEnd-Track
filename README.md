# HNG Stage 0 — Name Gender Classification API

A lightweight REST API built with FastAPI that integrates with the Genderize.io API to classify names by gender. Submitted as part of the HNG Internship i14 Backend track Stage 0 task.

---

## 🔗 Live API

web-production-575cc.up.railway.app


## 📌 Endpoint

### `GET /api/classify`

Classifies a name by gender using the Genderize.io API and returns a processed result.

**Query Parameter:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | The name to classify |

---

## ✅ Success Response `200 OK`

```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-13T14:32:35Z"
  }
}
```

**Field descriptions:**

- `name` — the name that was queried
- `gender` — `"male"` or `"female"`
- `probability` — Genderize confidence score (0–1)
- `sample_size` — number of samples the prediction is based on
- `is_confident` — `true` only when `probability >= 0.7` AND `sample_size >= 100`
- `processed_at` — UTC timestamp of when the request was processed (ISO 8601, never hardcoded)

---

## ❌ Error Responses

All errors follow this structure:

```json
{ "status": "error", "message": "<error message>" }
```

| Status Code | Condition | Message |
|---|---|---|
| `400` | Missing or empty `name` parameter | `"Missing or empty name parameter"` |
| `422` | `name` is a numeric value | `"name must be a string"` |
| `422` | Genderize has no prediction for the name | `"No prediction available for the provided name"` |
| `502` | Genderize API timed out or returned an error | `"Upstream API timed out"` |
| `500` | Unexpected server error | `"Server error"` |

---

## 🧪 Example Requests

```bash
# Valid name
curl https://yourapp.up.railway.app/api/classify?name=john

# Valid name (accented)
curl https://yourapp.up.railway.app/api/classify?name=josé

# Missing name — 400
curl https://yourapp.up.railway.app/api/classify

# Empty name — 400
curl https://yourapp.up.railway.app/api/classify?name=

# Numeric input — 422
curl https://yourapp.up.railway.app/api/classify?name=12345

# Unknown name — 422
curl https://yourapp.up.railway.app/api/classify?name=xyzqqqq
```

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **FastAPI** — web framework
- **Uvicorn** — ASGI server
- **httpx** — async HTTP client for external API calls

---

## 🚀 Running Locally

```bash
# Clone the repo
git clone https://github.com/MARVER1X/hng-stage-0-backend.git
cd hng-stage-0-backend

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

Then visit: `http://127.0.0.1:8000/api/classify?name=john`

---

## 📁 Project Structure

```
├── main.py            # FastAPI app and endpoint logic
├── requirements.txt   # Python dependencies
├── Procfile           # Railway deployment config
└── README.md
```

---

## 👤 Author

**Marvellous**
- GitHub: [@MARVER1X](https://github.com/MARVER1X)

---

*Submitted for HNG Internship i14 — Backend Stage 0*
