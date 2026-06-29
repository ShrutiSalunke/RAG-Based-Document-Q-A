// File location: frontend/src/components/Sidebar.jsx
import { Library, Upload, FileText, MessageSquare, History, LogOut } from "lucide-react";
 
const NAV_ITEMS = [
  { id: "upload", label: "Upload", icon: Upload },
  { id: "documents", label: "Documents", icon: FileText },
  { id: "query", label: "Ask", icon: MessageSquare },
  { id: "history", label: "History", icon: History },
];
 
export default function Sidebar({ activeView, onNavigate, documentCount, onLogout }) {
  return (
    <aside className="w-60 flex-shrink-0 h-screen border-r border-line bg-paper-raised flex flex-col">
      <div className="flex items-center gap-2.5 px-5 h-16 border-b border-line">
        <div className="w-8 h-8 rounded-md bg-ink flex items-center justify-center flex-shrink-0">
          <Library className="w-4.5 h-4.5 text-amber-soft" strokeWidth={1.75} />
        </div>
        <span className="font-display text-base text-ink tracking-tight">Archive</span>
      </div>
 
      <nav className="flex-1 px-3 py-4 space-y-0.5">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = activeView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition ${
                isActive
                  ? "bg-ink text-paper"
                  : "text-ink-soft hover:bg-line-soft"
              }`}
            >
              <Icon className="w-4 h-4" strokeWidth={1.85} />
              {item.label}
              {item.id === "documents" && documentCount > 0 && (
                <span
                  className={`ml-auto text-xs font-mono px-1.5 py-0.5 rounded-full ${
                    isActive ? "bg-paper/15 text-paper" : "bg-line-soft text-slate"
                  }`}
                >
                  {documentCount}
                </span>
              )}
            </button>
          );
        })}
      </nav>
 
      <div className="px-3 py-4 border-t border-line">
        <button
          onClick={onLogout}
          className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate hover:bg-line-soft hover:text-ink-soft transition"
        >
          <LogOut className="w-4 h-4" strokeWidth={1.85} />
          Sign out
        </button>
      </div>
    </aside>
  );
}
 
