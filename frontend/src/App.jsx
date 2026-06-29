
 
import { useState } from "react";
import { useAuth } from "./hooks/useAuth.js";
import { useDocuments } from "./hooks/useDocuments.js";
import * as api from "./lib/api.js";
 
import LoginScreen from "./components/LoginScreen.jsx";
import Sidebar from "./components/Sidebar.jsx";
import UploadView from "./components/UploadView.jsx";
import DocumentsView from "./components/DocumentsView.jsx";
import QueryView from "./components/QueryView.jsx";
import HistoryView from "./components/HistoryView.jsx";
 
export default function App() {
  const { isLoggedIn, isLoading: isLoggingIn, error: loginError, login, logout } = useAuth();
  const [activeView, setActiveView] = useState("upload");
 
  const { documents, isLoading: isLoadingDocs, upload, remove, retry } = useDocuments(isLoggedIn);
 
  if (!isLoggedIn) {
    return <LoginScreen onLogin={login} isLoading={isLoggingIn} error={loginError} />;
  }
 
  return (
    <div className="flex">
      <Sidebar
        activeView={activeView}
        onNavigate={setActiveView}
        documentCount={documents.length}
        onLogout={logout}
      />
 
      <main className="flex-1 h-screen overflow-y-auto">
        {activeView === "upload" && (
          <UploadView onUpload={upload} onNavigateToDocuments={() => setActiveView("documents")} />
        )}
 
        {activeView === "documents" && (
          <DocumentsView
            documents={documents}
            isLoading={isLoadingDocs}
            onDelete={remove}
            onRetry={retry}
            onNavigateToUpload={() => setActiveView("upload")}
          />
        )}
 
        {activeView === "query" && (
          <QueryView documents={documents} onQuery={api.runQuery} />
        )}
 
        {activeView === "history" && <HistoryView />}
      </main>
    </div>
  );
}
 
