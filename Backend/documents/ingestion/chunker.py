from dataclasses import dataclass
 
from transformers import AutoTokenizer

# Local tokenizer used only for token counting/chunking.
_ENCODING = AutoTokenizer.from_pretrained("bert-base-uncased")
 
CHUNK_SIZE_TOKENS = 350
CHUNK_OVERLAP_TOKENS = 60
 
 
@dataclass
class Chunk:
    page_number: int
    content: str
    token_count: int
 
 
def count_tokens(text: str) -> int:
    return len(_ENCODING.encode(text, add_special_tokens=False))
 
 
def chunk_pages(
    pages: list[tuple[int, str]],
    chunk_size: int = CHUNK_SIZE_TOKENS,
    overlap: int = CHUNK_OVERLAP_TOKENS,
) -> list[Chunk]:
    
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
 
    chunks: list[Chunk] = []
 
    for page_number, text in pages:
        tokens = _ENCODING.encode(text, add_special_tokens=False)
        start = 0
        while start < len(tokens):
            end = min(start + chunk_size, len(tokens))
            token_slice = tokens[start:end]
            chunk_text = _ENCODING.decode(token_slice, skip_special_tokens=True).strip()
            if chunk_text:
                chunks.append(
                    Chunk(
                        page_number=page_number,
                        content=chunk_text,
                        token_count=len(token_slice),
                    )
                )
 
            if end == len(tokens):
                break
            start = end - overlap
 
    return chunks
 
