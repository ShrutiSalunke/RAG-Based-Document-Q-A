// File location: frontend/src/lib/api.js
//
// Single source of truth for every call to the Django backend built in
// Phases 1-3. Centralizing this here means the rest of the app never
// constructs a fetch() call directly, and the JWT access/refresh dance
// only has to be implemented correctly once.
//
// Token storage: kept in memory (a module-level variable) rather than
// localStorage. This avoids the most common React-app security
// footgun (XSS-readable tokens in localStorage) at the small cost of
// needing to log in again on a full page reload, which is an
// acceptable trade-off for this project.
 
const API_BASE = "/api/v1";
 
let accessToken = null;
let refreshToken = null;
 
export function setTokens({ access, refresh }) {
  accessToken = access;
  if (refresh) refreshToken = refresh;
}
 
export function clearTokens() {
  accessToken = null;
  refreshToken = null;
}
 
export function isAuthenticated() {
  return Boolean(accessToken);
}
 
class ApiError extends Error {
  constructor(message, status, payload) {
    super(message);
    this.status = status;
    this.payload = payload;
  }
}
 
/**
 * Core request helper. Attaches the bearer token, retries exactly once
 * after a silent token refresh on a 401, and throws ApiError with the
 * parsed JSON body on any non-2xx response so callers can show the
 * backend's actual error message instead of a generic failure.
 */
async function request(path, { method = "GET", body, isFormData = false, _retried = false } = {}) {
  const headers = {};
  if (accessToken) headers["Authorization"] = `Bearer ${accessToken}`;
  if (!isFormData && body !== undefined) headers["Content-Type"] = "application/json";
 
  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: isFormData ? body : body !== undefined ? JSON.stringify(body) : undefined,
  });
 
  if (response.status === 401 && refreshToken && !_retried) {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
      return request(path, { method, body, isFormData, _retried: true });
    }
  }
 
  if (!response.ok) {
    let payload = null;
    try {
      payload = await response.json();
    } catch {
      /* response had no JSON body */
    }
    const message = payload?.detail || payload?.error || `Request failed (${response.status})`;
    throw new ApiError(message, response.status, payload);
  }
 
  if (response.status === 204) return null;
  return response.json();
}
 
async function tryRefreshToken() {
  try {
    const res = await fetch(`${API_BASE}/auth/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refreshToken }),
    });
    if (!res.ok) {
      clearTokens();
      return false;
    }
    const data = await res.json();
    accessToken = data.access;
    return true;
  } catch {
    clearTokens();
    return false;
  }
}
 
// ---------------------------------------------------------------------
// Auth
// ---------------------------------------------------------------------
export async function login(username, password) {
  const data = await request("/auth/token/", {
    method: "POST",
    body: { username, password },
  });
  setTokens({ access: data.access, refresh: data.refresh });
  return data;
}
 
// ---------------------------------------------------------------------
// Documents (Phase 1 + 2 endpoints)
// ---------------------------------------------------------------------
export function listDocuments() {
  return request("/documents/");
}
 
export function uploadDocument(file, onProgress) {
  // Uses XMLHttpRequest instead of fetch solely to get upload-progress
  // events, which fetch does not expose for request bodies.
  return new Promise((resolve, reject) => {
    const formData = new FormData();
    formData.append("file", file);
 
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `${API_BASE}/documents/`);
    if (accessToken) xhr.setRequestHeader("Authorization", `Bearer ${accessToken}`);
 
    xhr.upload.onprogress = (event) => {
      if (onProgress && event.lengthComputable) {
        onProgress(Math.round((event.loaded / event.total) * 100));
      }
    };
 
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        let payload = null;
        try {
          payload = JSON.parse(xhr.responseText);
        } catch {
          /* ignore */
        }
        reject(new ApiError(payload?.detail || "Upload failed", xhr.status, payload));
      }
    };
    xhr.onerror = () => reject(new ApiError("Network error during upload", 0, null));
    xhr.send(formData);
  });
}
 
export function getDocument(id) {
  return request(`/documents/${id}/`);
}
 
export function deleteDocument(id) {
  return request(`/documents/${id}/`, { method: "DELETE" });
}
 
export function retryDocument(id) {
  return request(`/documents/${id}/retry/`, { method: "POST" });
}
 
// ---------------------------------------------------------------------
// Query (Phase 3 endpoints)
// ---------------------------------------------------------------------
export function runQuery({ question, documentIds, topK }) {
  const body = { question };
  if (documentIds && documentIds.length > 0) body.document_ids = documentIds;
  if (topK) body.top_k = topK;
  return request("/query/", { method: "POST", body });
}
 
export function listQueryHistory() {
  return request("/queries/");
}
 
export { ApiError };
 
