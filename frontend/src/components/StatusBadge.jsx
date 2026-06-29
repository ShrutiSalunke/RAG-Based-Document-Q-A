// File location: frontend/src/components/StatusBadge.jsx
import { Clock, Loader2, CheckCircle2, XCircle } from "lucide-react";
 
const STATUS_CONFIG = {
  pending: { label: "Pending", icon: Clock, className: "text-slate bg-line-soft" },
  processing: { label: "Processing", icon: Loader2, className: "text-amber-deep bg-amber-soft", spin: true },
  ready: { label: "Ready", icon: CheckCircle2, className: "text-success bg-success-soft" },
  failed: { label: "Failed", icon: XCircle, className: "text-error bg-error-soft" },
};
 
export default function StatusBadge({ status }) {
  const config = STATUS_CONFIG[status] || STATUS_CONFIG.pending;
  const Icon = config.icon;
 
  return (
    <span
      className={`inline-flex items-center gap-1.5 text-xs font-medium px-2 py-1 rounded-full ${config.className}`}
    >
      <Icon className={`w-3 h-3 ${config.spin ? "animate-spin" : ""}`} strokeWidth={2} />
      {config.label}
    </span>
  );
}
