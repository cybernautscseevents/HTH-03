'use client';

import React from 'react';
import { 
  X, 
  AlertTriangle, 
  ShieldAlert, 
  CheckCircle, 
  AlertOctagon,
  FileText,
  HeartPulse
} from 'lucide-react';

interface SafetyAlertsModalProps {
  isOpen: boolean;
  onClose: () => void;
  flags: any[];
  onAcknowledgeFlag?: (flagId: string) => void;
}

export const SafetyAlertsModal: React.FC<SafetyAlertsModalProps> = ({
  isOpen,
  onClose,
  flags,
  onAcknowledgeFlag,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-2xl bg-slate-950 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 bg-slate-900/60 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-amber-500/10 text-amber-400 rounded-xl border border-amber-500/30">
              <ShieldAlert className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">
                Clinical Safety & Guardrail Alerts
              </h3>
              <p className="text-xs text-slate-400">
                Rule-based checks against drug allergies, red flags, and contraindications
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Alerts List */}
        <div className="flex-1 overflow-y-auto p-5 space-y-3.5">
          {flags.map((flag, idx) => {
            const isCritical = flag.severity === 'critical';
            const isWarning = flag.severity === 'warning';

            return (
              <div
                key={flag.id || idx}
                className={`p-4 rounded-xl border transition-all ${
                  isCritical
                    ? 'bg-rose-950/20 border-rose-500/40 text-rose-200'
                    : isWarning
                    ? 'bg-amber-950/20 border-amber-500/40 text-amber-200'
                    : 'bg-slate-900/60 border-slate-800 text-slate-300'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-start gap-3">
                    {isCritical ? (
                      <AlertOctagon className="h-5 w-5 text-rose-400 shrink-0 mt-0.5" />
                    ) : (
                      <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
                    )}
                    <div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded border ${
                            isCritical
                              ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                              : 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                          }`}
                        >
                          {flag.severity}
                        </span>
                        <span className="text-xs font-semibold text-white">
                          {flag.category?.toUpperCase() || 'SAFETY RULE'}
                        </span>
                      </div>
                      <p className="text-xs mt-1.5 leading-relaxed text-slate-200 font-medium">
                        {flag.message}
                      </p>
                      {flag.recommendation && (
                        <p className="text-[11px] text-slate-400 mt-1 italic">
                          Recommendation: {flag.recommendation}
                        </p>
                      )}
                    </div>
                  </div>

                  <button
                    onClick={() => onAcknowledgeFlag && onAcknowledgeFlag(flag.id)}
                    className="shrink-0 px-2.5 py-1 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 rounded-lg text-xs font-medium transition-colors"
                  >
                    Acknowledge
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-900/60 flex items-center justify-between">
          <p className="text-[11px] text-slate-400">
            Safety flags do not block clinical sign-off, but require explicit physician acknowledgement.
          </p>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-bold transition-colors"
          >
            Close Panel
          </button>
        </div>
      </div>
    </div>
  );
};
export default SafetyAlertsModal;
