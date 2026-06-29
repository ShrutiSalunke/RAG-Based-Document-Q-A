// File location: frontend/src/hooks/useDocuments.js
//
// Owns the document list and keeps it fresh by polling while any
// document is still pending/processing. This is the simplest reliable
// way to reflect the Phase 2 django-q2 background ingestion status in
// the UI without adding a WebSocket layer the proposal doesn't ask for.
 
import { useCallback, useEffect, useRef, useState } from "react";
import * as api from "../lib/api.js";
 
const POLL_INTERVAL_MS = 3000;
const ACTIVE_STATUSES = new Set(["pending", "processing"]);
 
export function useDocuments(isLoggedIn) {
  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const pollRef = useRef(null);
 
  const refresh = useCallback(async () => {
    try {
      const data = await api.listDocuments();
      setDocuments(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, []);
 
  // Only fetch once the user is actually authenticated -- calling this
  // before login would hit the API with no token and surface a
  // pointless 401 error right as the dashboard first mounts.
  useEffect(() => {
    if (isLoggedIn) {
      refresh();
    }
  }, [isLoggedIn, refresh]);
 
  // Poll only while logged in AND something is actively ingesting.
  // hasActiveDocument (not the full documents array) is the dependency,
  // so the interval is only created/torn down on a true state
  // transition, not re-created on every single poll tick.
  const hasActiveDocument = documents.some((doc) => ACTIVE_STATUSES.has(doc.status));
 
  useEffect(() => {
    if (isLoggedIn && hasActiveDocument) {
      pollRef.current = setInterval(refresh, POLL_INTERVAL_MS);
    }
    return () => {
      if (pollRef.current) {
        clearInterval(pollRef.current);
        pollRef.current = null;
      }
    };
  }, [isLoggedIn, hasActiveDocument, refresh]);
 
  // Clear stale document state on logout so a subsequent login (by
  // possibly a different user) never briefly shows the previous
  // session's documents before the fresh fetch completes.
  useEffect(() => {
    if (!isLoggedIn) {
      setDocuments([]);
      setIsLoading(true);
    }
  }, [isLoggedIn]);
 
  const upload = useCallback(
    async (file, onProgress) => {
      const newDoc = await api.uploadDocument(file, onProgress);
      setDocuments((prev) => [newDoc, ...prev]);
      return newDoc;
    },
    []
  );
 
  const remove = useCallback(async (id) => {
    await api.deleteDocument(id);
    setDocuments((prev) => prev.filter((doc) => doc.id !== id));
  }, []);
 
  const retry = useCallback(async (id) => {
    const updated = await api.retryDocument(id);
    setDocuments((prev) => prev.map((doc) => (doc.id === id ? updated : doc)));
  }, []);
 
  return { documents, isLoading, error, refresh, upload, remove, retry };
}
 
