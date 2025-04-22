import json
from pathlib import Path

STORAGE_FILE = Path("reviews.json")

def _load_data():
    if STORAGE_FILE.exists():
        return json.loads(STORAGE_FILE.read_text(encoding="utf-8"))
    return []

def _save_data(data):
    STORAGE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def save_review(text, reply):
    data = _load_data()
    data.append({"text": text, "reply": reply, "status": "pending"})
    _save_data(data)

def get_all_reviews():
    return _load_data()

def update_review_status(index, status):
    data = _load_data()
    if 0 <= index < len(data):
        data[index]["status"] = status
        _save_data(data)
