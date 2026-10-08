'use client';

import React, { useState } from 'react';
import { 
  X, 
  FileCode, 
  Copy, 
  Download, 
  CheckCircle, 
  ShieldCheck, 
  Layers
} from 'lucide-react';

interface FHIRExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  fhirBundle: any;
}

export const FHIRExportModal: React.FC<FHIRExportModalProps> = ({
  isOpen,
  onClose,
  fhirBundle,
}) => {
  const [copied, setCopied] = useState<boolean>(false);

  if (!isOpen) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(fhirBundle, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(fhirBundle, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `clinscribe_fhir_bundle_${Date.now()}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-3xl bg-slate-950 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 bg-slate-900/60 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-cyan-500/10 text-cyan-400 rounded-xl border border-cyan-500/30">
              <FileCode className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white">
                  ABDM / HL7 FHIR R4 Bundle Export
                </h3>
                <span className="px-2 py-0.5 text-[10px] font-semibold bg-teal-500/20 text-teal-300 border border-teal-500/30 rounded-full">
                  NRCES Profile Ready
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Interoperable Electronic Health Record format for Ayushman Bharat Digital Mission
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

        {/* Resources Badges Header */}
        <div className="px-5 py-3 border-b border-slate-800/80 bg-slate-900/40 flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-1.5 text-xs">
            <span className="text-slate-400 text-[11px] mr-1">Contained Resources:</span>
            <span className="px-2 py-0.5 bg-slate-800 text-teal-300 rounded border border-slate-700 font-mono text-[10px]">Patient</span>
            <span className="px-2 py-0.5 bg-slate-800 text-cyan-300 rounded border border-slate-700 font-mono text-[10px]">Practitioner</span>
            <span className="px-2 py-0.5 bg-slate-800 text-sky-300 rounded border border-slate-700 font-mono text-[10px]">Encounter</span>
            <span className="px-2 py-0.5 bg-slate-800 text-amber-300 rounded border border-slate-700 font-mono text-[10px]">Condition</span>
            <span className="px-2 py-0.5 bg-slate-800 text-rose-300 rounded border border-slate-700 font-mono text-[10px]">MedicationRequest</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg border border-slate-700 text-xs flex items-center gap-1.5 transition-colors"
            >
              <Copy className="h-3 w-3" />
              <span>{copied ? 'Copied!' : 'Copy JSON'}</span>
            </button>
            <button
              onClick={handleDownload}
              className="px-3 py-1 bg-teal-500 hover:bg-teal-400 text-slate-950 font-semibold rounded-lg text-xs flex items-center gap-1.5 transition-colors"
            >
              <Download className="h-3 w-3" />
              <span>Download .json</span>
            </button>
          </div>
        </div>

        {/* JSON Code Viewer */}
        <div className="flex-1 overflow-y-auto p-5 bg-slate-950">
          <pre className="font-mono text-xs text-teal-300 bg-slate-900/80 p-4 rounded-xl border border-slate-800 leading-relaxed overflow-x-auto selection:bg-teal-500/30">
            {JSON.stringify(fhirBundle, null, 2)}
          </pre>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-900/60 flex items-center justify-between text-xs text-slate-400">
          <span>Standards: HL7 FHIR R4 • NRCES NDHM Profile v1.0</span>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-bold transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
export default FHIRExportModal;
