// File location: frontend/src/components/HistoryView.jsx
import { useEffect, useState } from "react";
import { Clock, Zap, MessageSquareOff } from "lucide-react";
import * as api from "../lib/api.js";
import AnswerText from "./AnswerText.jsx";
 
function formatDate(isoString) {
  return new Date(isoString).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
 
export default function HistoryView() {
  const [queries, setQueries] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
 
  useEffect(() => {
    api
      .listQueryHistory()
      .then(setQueries)
      .catch((err) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, []);
 
  return (
    <div className="max-w-2xl mx-auto py-12 px-8">
      <h1 className="font-display text-2xl text-ink mb-1.5">Query history</h1>
      <p className="text-sm text-slate mb-8">Every question you've asked, most recent first.</p>
 
      {isLoading && (
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-20 bg-paper-raised border border-line rounded-xl animate-pulse" />
          ))}
        </div>
      )}
 
      {!isLoading && error && (
        <div className="bg-error-soft border border-error/20 rounded-xl px-4 py-3 text-sm text-error">
          {error}
        </div>
      )}
 
      {!isLoading && !error && queries.length === 0 && (
        <div className="flex flex-col items-center text-center py-16 border border-dashed border-line rounded-xl">
          <MessageSquareOff className="w-9 h-9 text-slate-light mb-3" strokeWidth={1.5} />
          <p className="text-sm font-medium text-ink mb-1">No queries yet</p>
          <p className="text-xs text-slate-light">Questions you ask will show up here.</p>
        </div>
      )}
 
      <div className="space-y-3">
        {queries.map((q) => (
          <details key={q.id} className="group bg-paper-raised border border-line rounded-xl px-4 py-3.5">
            <summary className="cursor-pointer list-none flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="text-sm font-medium text-ink line-clamp-2">{q.question}</p>
                <p className="text-xs text-slate-light font-mono mt-1">{formatDate(q.created_at)}</p>
              </div>
              <div className="flex items-center gap-3 flex-shrink-0 text-xs font-mono text-slate-light">
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3" strokeWidth={1.85} />
                  {q.retrieval_latency_ms}ms
                </span>
                <span className="flex items-center gap-1">
                  <Zap className="w-3 h-3" strokeWidth={1.85} />
                  {q.generation_latency_ms}ms
                </span>
              </div>
            </summary>
            <div className="mt-3 pt-3 border-t border-line">
              <AnswerText text={q.answer} />
            </div>
          </details>
        ))}
      </div>
    </div>
  );
}
