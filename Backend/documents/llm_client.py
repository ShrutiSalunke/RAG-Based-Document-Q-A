from django.conf import settings
from openai import OpenAI
 
# Free-tier text-generation model hosted on Hugging Face's Inference
# Providers. If this specific model is rate-limited or deprecated,
# swap it for another free chat model listed at:
# https://huggingface.co/docs/inference-providers/index
HF_MODEL = "meta-llama/Llama-3.1-8B-Instruct"
 
_client: OpenAI | None = None
 
 
def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=settings.HF_TOKEN,
        )
    return _client
 
 
def generate_answer(system_prompt: str, user_prompt: str, max_tokens: int = 512) -> str:
    """
    Sends a chat-completion request to Hugging Face's free Inference
    Providers endpoint and returns the generated text.
    """
    client = get_client()
    response = client.chat.completions.create(
        model=HF_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.2,
    )
    return response.choices[0].message.content
