// File location: frontend/src/components/SourcesList.jsx
import { useRef } from "react";
import { FileText } from "lucide-react";
 
export default function SourcesList({ sources, highlightRef }) {
  if (!sources || sources.length === 0) return null;
 
  return (
    <div className="mt-5 pt-5 border-t border-line">
      <p className="text-xs font-medium text-slate-light uppercase tracking-wide mb-2.5">
        Sources
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {sources.map((source, idx) => (
          <div
            key={`${source.document_id}-${source.page_number}-${idx}`}
            ref={(el) => highlightRef?.(source.document_name, source.page_number, el)}
            className="flex items-start gap-2.5 bg-paper border border-line rounded-xl px-3 py-2.5 transition-colors"
          >
            <FileText className="w-3.5 h-3.5 text-amber-deep flex-shrink-0 mt-0.5" strokeWidth={1.85} />
            <div className="min-w-0">
              <p className="text-xs font-medium text-ink truncate">{source.document_name}</p>
              <p className="text-xs text-slate-light font-mono mt-0.5">page {source.page_number}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
