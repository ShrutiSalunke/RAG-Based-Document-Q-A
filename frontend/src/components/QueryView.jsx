// File location: frontend/src/components/QueryView.jsx
import { useMemo, useRef, useState } from "react";
import { Send, Search, Clock, Zap, FileQuestion, Inbox } from "lucide-react";
import AnswerText from "./AnswerText.jsx";
import SourcesList from "./SourcesList.jsx";
 
export default function QueryView({ documents, onQuery }) {
  const [question, setQuestion] = useState("");
  const [selectedDocIds, setSelectedDocIds] = useState([]);
  const [isAsking, setIsAsking] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const chipRefs = useRef({});
 
  const readyDocuments = useMemo(
    () => documents.filter((d) => d.status === "ready"),
    [documents]
  );
 
  function toggleDoc(id) {
    setSelectedDocIds((prev) =>
      prev.includes(id) ? prev.filter((d) => d !== id) : [...prev, id]
    );
  }
 
  async function handleAsk(e) {
    e.preventDefault();
    if (!question.trim() || isAsking) return;
 
    setIsAsking(true);
    setError(null);
    try {
      const data = await onQuery({
        question: question.trim(),
        documentIds: selectedDocIds.length > 0 ? selectedDocIds : undefined,
      });
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong while running your query.");
    } finally {
      setIsAsking(false);
    }
  }
 
  function handleCitationClick(documentName, pageNumber) {
    const key = `${documentName}-${pageNumber}`;
    const el = chipRefs.current[key];
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "center" });
      el.classList.add("ring-2", "ring-amber");
      setTimeout(() => el.classList.remove("ring-2", "ring-amber"), 1200);
    }
  }
 
  if (readyDocuments.length === 0) {
    return (
      <div className="max-w-2xl mx-auto py-12 px-8">
        <h1 className="font-display text-2xl text-ink mb-1.5">Ask a question</h1>
        <p className="text-sm text-slate mb-10">
          Query your document collection in plain language.
        </p>
        <div className="flex flex-col items-center text-center py-16 border border-dashed border-line rounded-xl">
          <Inbox className="w-9 h-9 text-slate-light mb-3" strokeWidth={1.5} />
          <p className="text-sm font-medium text-ink mb-1">No documents ready yet</p>
          <p className="text-xs text-slate-light">
            Upload a PDF and wait for it to finish processing before asking questions.
          </p>
        </div>
      </div>
    );
  }
 
  return (
    <div className="max-w-2xl mx-auto py-12 px-8">
      <h1 className="font-display text-2xl text-ink mb-1.5">Ask a question</h1>
      <p className="text-sm text-slate mb-8">
        Answers are generated only from your documents, with sources cited inline.
      </p>
 
      <form onSubmit={handleAsk}>
        <div className="relative">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleAsk(e);
              }
            }}
            placeholder="What does the contract say about termination notice periods?"
            rows={3}
            className="w-full resize-none rounded-xl border border-line bg-paper-raised px-4 py-3 pr-12 text-sm text-ink placeholder:text-slate-light focus:outline-none focus:border-amber focus:ring-2 focus:ring-amber/20 transition"
          />
          <button
            type="submit"
            disabled={!question.trim() || isAsking}
            className="absolute right-3 bottom-3 w-8 h-8 flex items-center justify-center rounded-md bg-ink text-paper disabled:opacity-30 disabled:cursor-not-allowed hover:bg-ink-soft transition"
          >
            <Send className="w-3.5 h-3.5" strokeWidth={2} />
          </button>
        </div>
 
        <div className="flex items-center gap-1.5 flex-wrap mt-3">
          <span className="text-xs text-slate-light mr-1">Search in:</span>
          <button
            type="button"
            onClick={() => setSelectedDocIds([])}
            className={`text-xs font-medium px-2.5 py-1 rounded-full border transition ${
              selectedDocIds.length === 0
                ? "bg-ink text-paper border-ink"
                : "text-slate border-line hover:border-slate-light"
            }`}
          >
            All documents
          </button>
          {readyDocuments.map((doc) => (
            <button
              type="button"
              key={doc.id}
              onClick={() => toggleDoc(doc.id)}
              className={`text-xs font-medium px-2.5 py-1 rounded-full border transition truncate max-w-[160px] ${
                selectedDocIds.includes(doc.id)
                  ? "bg-amber-soft text-amber-deep border-amber/40"
                  : "text-slate border-line hover:border-slate-light"
              }`}
              title={doc.original_filename}
            >
              {doc.original_filename}
            </button>
          ))}
        </div>
      </form>
 
      <div className="mt-8">
        {isAsking && (
          <div className="flex items-center gap-2.5 text-sm text-slate py-8 justify-center">
            <Search className="w-4 h-4 animate-pulse" strokeWidth={1.75} />
            Searching your documents…
          </div>
        )}
 
        {!isAsking && error && (
          <div className="bg-error-soft border border-error/20 rounded-xl px-4 py-3 text-sm text-error">
            {error}
          </div>
        )}
 
        {!isAsking && result && (
          <div className="bg-paper-raised border border-line rounded-xl px-5 py-5">
            {!result.answerable && (
              <div className="flex items-center gap-2 text-xs font-medium text-slate-light uppercase tracking-wide mb-3">
                <FileQuestion className="w-3.5 h-3.5" strokeWidth={1.85} />
                Not answerable from your documents
              </div>
            )}
 
            <AnswerText text={result.answer} onCitationClick={handleCitationClick} />
 
            <SourcesList
              sources={result.sources}
              highlightRef={(name, page, el) => {
                chipRefs.current[`${name}-${page}`] = el;
              }}
            />
 
            <div className="flex items-center gap-4 mt-5 pt-4 border-t border-line text-xs font-mono text-slate-light">
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" strokeWidth={1.85} />
                retrieval {result.retrieval_latency_ms}ms
              </span>
              <span className="flex items-center gap-1">
                <Zap className="w-3 h-3" strokeWidth={1.85} />
                generation {result.generation_latency_ms}ms
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
 
