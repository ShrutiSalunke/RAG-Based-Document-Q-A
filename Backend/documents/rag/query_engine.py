import logging
import time
from dataclasses import dataclass, field 
from django.contrib.auth.models import AbstractBaseUser 
from documents.llm_client import generate_answer
from documents.models import QueryLog
from documents.rag.prompts import SYSTEM_PROMPT, NO_ANSWER_PHRASE, build_user_prompt
from documents.rag.retrieval import (RetrievedChunk, has_relevant_match, retrieve_relevant_chunks,) 
logger = logging.getLogger(__name__)
 
 
@dataclass
class QuerySource:
    document_id: str
    document_name: str
    page_number: int
 
 
@dataclass
class QueryResult:
    answer: str
    answerable: bool
    sources: list[QuerySource] = field(default_factory=list)
    retrieval_latency_ms: int = 0
    generation_latency_ms: int = 0
    query_log_id: str | None = None
 
 
def run_query(question: str, user: AbstractBaseUser,  document_ids: list[str] | None = None,  top_k: int = 5,) -> QueryResult:
    
    retrieval_start = time.monotonic()
    chunks: list[RetrievedChunk] = retrieve_relevant_chunks(question=question, owner=user, document_ids=document_ids,top_k=top_k, )
    retrieval_latency_ms = int((time.monotonic() - retrieval_start) * 1000)

    if not has_relevant_match(chunks):
        log = QueryLog.objects.create(user=user, question=question, answer=NO_ANSWER_PHRASE, retrieved_chunk_ids=[c.chunk_id for c in chunks], retrieval_latency_ms=retrieval_latency_ms, generation_latency_ms=0, )
        return QueryResult( answer=NO_ANSWER_PHRASE, answerable=False, sources=[], retrieval_latency_ms=retrieval_latency_ms, generation_latency_ms=0,query_log_id=str(log.id), )
 
    user_prompt = build_user_prompt(question, chunks)
 
    generation_start = time.monotonic()
    try:
        answer = generate_answer(SYSTEM_PROMPT, user_prompt)
    except Exception:
        logger.exception("LLM generation failed for question: %s", question)
        answer = ("Sorry, the answer-generation service is temporarily unavailable. "  "Please try again in a moment." )
    generation_latency_ms = int((time.monotonic() - generation_start) * 1000)

    answerable = NO_ANSWER_PHRASE.strip().lower() not in answer.strip().lower()
 
    sources = (
        [
            QuerySource(
                document_id=c.document_id,
                document_name=c.document_name,
                page_number=c.page_number,
            )
            for c in chunks
        ]
        if answerable
        else []
    )
 
    log = QueryLog.objects.create(user=user, question=question, answer=answer, retrieved_chunk_ids=[c.chunk_id for c in chunks],  retrieval_latency_ms=retrieval_latency_ms,  generation_latency_ms=generation_latency_ms, )
 
    return QueryResult(answer=answer, answerable=answerable, sources=sources,  retrieval_latency_ms=retrieval_latency_ms, generation_latency_ms=generation_latency_ms,   query_log_id=str(log.id), )
 
