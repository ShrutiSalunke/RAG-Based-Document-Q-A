import logging
import time

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIMENSION = 384
MAX_RETRIES = 3

API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_NAME}"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.HF_TOKEN}",
        "Content-Type": "application/json",
    }


def _embed_one(text: str) -> list[float]:
    payload = {
        "inputs": text,
        "parameters": {
            "normalize": True
        }
    }

    last_exc = None

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                API_URL,
                headers=_headers(),
                json=payload,
                timeout=60,
            )

            print("=" * 80)
            print("Status Code:", response.status_code)
            print("Headers:", response.headers)
            print("Response Body:")
            print(response.text)
            print("=" * 80)

            response.raise_for_status()

            result = response.json()

            if result and isinstance(result[0], list):
                width = len(result[0])
                pooled = [
                    sum(v[i] for v in result) / len(result)
                    for i in range(width)
                ]
                return pooled

            return result

        except Exception as exc:
            last_exc = exc
            wait = 2 ** attempt
            logger.warning(
                "Embedding request failed (%s/%s). Retrying in %ss...",
                attempt + 1,
                MAX_RETRIES,
                wait,
            )
            time.sleep(wait)

    raise last_exc


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    return [_embed_one(text) for text in texts]


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]