from documents.rag.retrieval import RetrievedChunk
 
NO_ANSWER_PHRASE = "The documents don't contain information to answer this question."
 
SYSTEM_PROMPT = f"""You are a document question-answering assistant. You answer \
questions using ONLY the numbered context passages provided by the user -- never \
from outside knowledge, training data, or assumptions.
 
Rules you must follow exactly:
1. Every factual claim in your answer must be immediately followed by a citation \
in the form [Source: <document name>, page <page number>], referencing the exact \
passage number(s) it came from.
2. If the passages do not contain enough information to answer the question, \
respond with exactly this sentence and nothing else: "{NO_ANSWER_PHRASE}"
3. Never blend information from outside the passages, even if you believe you \
know the answer from general knowledge.
4. Keep answers concise and directly responsive to the question.
5. If multiple passages disagree, mention the discrepancy and cite both sources \
rather than silently picking one."""
 
 
def build_user_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    
    passages = []
    for i, chunk in enumerate(chunks, start=1):
        passages.append(f"--- Passage {i} (Source: {chunk.document_name}, page {chunk.page_number}) ---\n" f"{chunk.content}" ) 
    context_block = "\n\n".join(passages)
 
    return (f"Context passages:\n\n{context_block}\n\n" f"Question: {question}\n\n" f"Answer the question using only the passages above, citing " f"[Source: document name, page X] for every claim." )
 
  