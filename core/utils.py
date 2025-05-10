import re
import json


def serialize_mongo_document(doc):
    return {**doc, "_id": str(doc["_id"])}


def clean_json_output(raw: str):
    # remove leading/trailing triple backticks or markdown formatting
    cleaned = re.sub(r"^```json|^```|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned)