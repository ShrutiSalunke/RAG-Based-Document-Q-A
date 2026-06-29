// File location: frontend/src/components/UploadView.jsx
import { useCallback, useRef, useState } from "react";
import { UploadCloud, FileText, AlertCircle, ArrowRight } from "lucide-react";
 
export default function UploadView({ onUpload, onNavigateToDocuments }) {
  const [isDragging, setIsDragging] = useState(false);
  const [uploads, setUploads] = useState([]); // [{ id, name, progress, error }]
  const inputRef = useRef(null);
 
  const handleFiles = useCallback(
    (fileList) => {
      const files = Array.from(fileList).filter((f) => f.type === "application/pdf");
      files.forEach((file) => {
        const tempId = `${file.name}-${Date.now()}`;
        setUploads((prev) => [...prev, { id: tempId, name: file.name, progress: 0, error: null }]);
 
        onUpload(file, (progress) => {
          setUploads((prev) => prev.map((u) => (u.id === tempId ? { ...u, progress } : u)));
        })
          .then(() => {
            setUploads((prev) => prev.filter((u) => u.id !== tempId));
          })
          .catch((err) => {
            setUploads((prev) =>
              prev.map((u) => (u.id === tempId ? { ...u, error: err.message } : u))
            );
          });
      });
    },
    [onUpload]
  );
 
  function handleDrop(e) {
    e.preventDefault();
    setIsDragging(false);
    handleFiles(e.dataTransfer.files);
  }
 
  return (
    <div className="max-w-2xl mx-auto py-12 px-8">
      <h1 className="font-display text-2xl text-ink mb-1.5">Upload documents</h1>
      <p className="text-sm text-slate mb-8">
        Add PDFs to your collection. Each one is parsed, chunked, and embedded in the
        background — you can keep working while it processes.
      </p>
 
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`rounded-xl border-2 border-dashed transition cursor-pointer px-8 py-14 flex flex-col items-center text-center ${
          isDragging
            ? "border-amber bg-amber-soft/40"
            : "border-line bg-paper-raised hover:border-slate-light"
        }`}
      >
        <div className="w-12 h-12 rounded-full bg-line-soft flex items-center justify-center mb-4">
          <UploadCloud className="w-6 h-6 text-slate" strokeWidth={1.75} />
        </div>
        <p className="text-sm font-medium text-ink mb-1">
          Drop PDF files here, or click to browse
        </p>
        <p className="text-xs text-slate-light">PDF only · no size limit enforced by the UI</p>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          multiple
          className="hidden"
          onChange={(e) => {
            handleFiles(e.target.files);
            e.target.value = "";
          }}
        />
      </div>
 
      {uploads.length > 0 && (
        <div className="mt-6 space-y-2">
          {uploads.map((u) => (
            <div
              key={u.id}
              className="flex items-center gap-3 bg-paper-raised border border-line rounded-xl px-4 py-3"
            >
              <FileText className="w-4 h-4 text-slate flex-shrink-0" strokeWidth={1.75} />
              <div className="flex-1 min-w-0">
                <p className="text-sm text-ink truncate">{u.name}</p>
                {u.error ? (
                  <p className="text-xs text-error flex items-center gap-1 mt-0.5">
                    <AlertCircle className="w-3 h-3" strokeWidth={2} />
                    {u.error}
                  </p>
                ) : (
                  <div className="w-full h-1 bg-line-soft rounded-full mt-1.5 overflow-hidden">
                    <div
                      className="h-full bg-amber transition-all duration-200"
                      style={{ width: `${u.progress}%` }}
                    />
                  </div>
                )}
              </div>
              {!u.error && (
                <span className="text-xs font-mono text-slate-light flex-shrink-0">
                  {u.progress}%
                </span>
              )}
            </div>
          ))}
        </div>
      )}
 
      <button
        onClick={onNavigateToDocuments}
        className="mt-8 inline-flex items-center gap-1.5 text-sm font-medium text-ink-soft hover:text-ink transition"
      >
        View document library
        <ArrowRight className="w-3.5 h-3.5" strokeWidth={2} />
      </button>
    </div>
  );
}
 
