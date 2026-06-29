// File location: frontend/src/components/DocumentsView.jsx
import { FileText, Trash2, RotateCcw, AlertCircle, Inbox } from "lucide-react";
import StatusBadge from "./StatusBadge.jsx";
 
function formatDate(isoString) {
  return new Date(isoString).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
 
export default function DocumentsView({ documents, isLoading, onDelete, onRetry, onNavigateToUpload }) {
  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-8">
        <div className="h-8 w-48 bg-line-soft rounded animate-pulse mb-8" />
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 bg-paper-raised border border-line rounded-xl animate-pulse" />
          ))}
        </div>
      </div>
    );
  }
 
  if (documents.length === 0) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-8">
        <h1 className="font-display text-2xl text-ink mb-1.5">Document library</h1>
        <p className="text-sm text-slate mb-10">Every document you've uploaded lives here.</p>
 
        <div className="flex flex-col items-center text-center py-16 border border-dashed border-line rounded-xl">
          <Inbox className="w-9 h-9 text-slate-light mb-3" strokeWidth={1.5} />
          <p className="text-sm font-medium text-ink mb-1">No documents yet</p>
          <p className="text-xs text-slate-light mb-5">Upload a PDF to start building your collection.</p>
          <button
            onClick={onNavigateToUpload}
            className="text-sm font-medium text-paper bg-ink px-4 py-2 rounded-lg hover:bg-ink-soft transition"
          >
            Upload a document
          </button>
        </div>
      </div>
    );
  }
 
  return (
    <div className="max-w-4xl mx-auto py-12 px-8">
      <div className="flex items-baseline justify-between mb-8">
        <div>
          <h1 className="font-display text-2xl text-ink mb-1.5">Document library</h1>
          <p className="text-sm text-slate">
            {documents.length} document{documents.length !== 1 ? "s" : ""} ·{" "}
            {documents.filter((d) => d.status === "ready").length} ready to query
          </p>
        </div>
      </div>
 
      <div className="space-y-2">
        {documents.map((doc) => (
          <div
            key={doc.id}
            className="group flex items-center gap-4 bg-paper-raised border border-line rounded-xl px-4 py-3.5 hover:border-slate-light transition"
          >
            <FileText className="w-4.5 h-4.5 text-slate flex-shrink-0" strokeWidth={1.75} />
 
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-ink truncate">{doc.original_filename}</p>
              <p className="text-xs text-slate-light font-mono mt-0.5">
                {doc.page_count > 0 ? `${doc.page_count} pages · ` : ""}
                uploaded {formatDate(doc.created_at)}
              </p>
              {doc.status === "failed" && doc.error_message && (
                <p className="text-xs text-error flex items-start gap-1 mt-1.5">
                  <AlertCircle className="w-3 h-3 mt-0.5 flex-shrink-0" strokeWidth={2} />
                  <span className="line-clamp-2">{doc.error_message}</span>
                </p>
              )}
            </div>
 
            <StatusBadge status={doc.status} />
 
            <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition">
              {doc.status === "failed" && (
                <button
                  onClick={() => onRetry(doc.id)}
                  title="Retry ingestion"
                  className="p-1.5 rounded-md text-slate hover:text-amber-deep hover:bg-amber-soft transition"
                >
                  <RotateCcw className="w-3.5 h-3.5" strokeWidth={1.85} />
                </button>
              )}
              <button
                onClick={() => onDelete(doc.id)}
                title="Delete document"
                className="p-1.5 rounded-md text-slate hover:text-error hover:bg-error-soft transition"
              >
                <Trash2 className="w-3.5 h-3.5" strokeWidth={1.85} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
