import logging
import time

from django.conf import settings
from openai import OpenAI

logger = logging.getLogger(__name__)

LLM_MODEL = "gpt-4.1-mini"

MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client

    if _client is None:
        _client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    return _client


def generate_answer(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 512,
) -> str:

    client = get_client()
    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                max_tokens=max_tokens,
                temperature=0.2,
            )

            answer = response.choices[0].message.content

            if answer:
                return answer.strip()

            raise RuntimeError("Model returned an empty response.")

        except Exception as exc:
            last_error = exc

            logger.warning(
                "LLM call failed (attempt %s/%s): %s",
                attempt,
                MAX_RETRIES,
                exc,
            )

            time.sleep(RETRY_BACKOFF_SECONDS * attempt)

    raise RuntimeError(
        f"OpenAI model {LLM_MODEL} failed after {MAX_RETRIES} attempts."
    ) from last_error