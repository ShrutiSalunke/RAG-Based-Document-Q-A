// File location: frontend/src/components/LoginScreen.jsx
import { useState } from "react";
import { Library, ArrowRight, AlertCircle } from "lucide-react";
 
export default function LoginScreen({ onLogin, isLoading, error }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
 
  function handleSubmit(e) {
    e.preventDefault();
    if (username.trim() && password) onLogin(username.trim(), password);
  }
 
  return (
    <div className="min-h-screen flex items-center justify-center bg-paper px-6">
      <div className="w-full max-w-sm">
        <div className="flex items-center gap-2.5 justify-center mb-8">
          <div className="w-9 h-9 rounded-md bg-ink flex items-center justify-center">
            <Library className="w-5 h-5 text-amber-soft" strokeWidth={1.75} />
          </div>
          <span className="font-display text-xl text-ink tracking-tight">Archive</span>
        </div>
 
        <div className="bg-paper-raised border border-line rounded-xl p-7 shadow-[0_1px_3px_rgba(20,33,61,0.06)]">
          <h1 className="font-display text-lg text-ink mb-1">Sign in</h1>
          <p className="text-sm text-slate mb-6">Use your project credentials to continue.</p>
 
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="username" className="block text-xs font-medium text-ink-soft mb-1.5">
                Username
              </label>
              <input
                id="username"
                type="text"
                autoComplete="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full rounded-lg border border-line bg-paper px-3 py-2 text-sm text-ink placeholder:text-slate-light focus:outline-none focus:border-amber focus:ring-2 focus:ring-amber/20 transition"
                placeholder="admin"
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-xs font-medium text-ink-soft mb-1.5">
                Password
              </label>
              <input
                id="password"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border border-line bg-paper px-3 py-2 text-sm text-ink placeholder:text-slate-light focus:outline-none focus:border-amber focus:ring-2 focus:ring-amber/20 transition"
                placeholder="••••••••"
              />
            </div>
 
            {error && (
              <div className="flex items-start gap-2 text-sm text-error bg-error-soft rounded-lg px-3 py-2">
                <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" strokeWidth={1.75} />
                <span>{error}</span>
              </div>
            )}
 
            <button
              type="submit"
              disabled={isLoading || !username.trim() || !password}
              className="w-full flex items-center justify-center gap-1.5 rounded-lg bg-ink text-paper text-sm font-medium py-2.5 hover:bg-ink-soft disabled:opacity-40 disabled:cursor-not-allowed transition"
            >
              {isLoading ? "Signing in…" : "Sign in"}
              {!isLoading && <ArrowRight className="w-4 h-4" strokeWidth={2} />}
            </button>
          </form>
        </div>
 
        <p className="text-center text-xs text-slate-light mt-6">
          RAG Document Query Engine · Major Project 21CSA699A
        </p>
      </div>
    </div>
  );
}
 
