'use client';

import React, { useState } from 'react';
import { 
  X, 
  Lock, 
  ShieldCheck, 
  EyeOff, 
  Trash2, 
  CheckCircle2, 
  FileCheck,
  History
} from 'lucide-react';

interface PrivacyCenterModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const PrivacyCenterModal: React.FC<PrivacyCenterModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [consentGranted, setConsentGranted] = useState<boolean>(true);
  const [piiMasking, setPiiMasking] = useState<boolean>(true);
  const [ephemeralAudio, setEphemeralAudio] = useState<boolean>(true);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-2xl bg-slate-950 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 bg-slate-900/60 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-teal-500/10 text-teal-400 rounded-xl border border-teal-500/30">
              <Lock className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white">
                  Privacy, Security & DPDP Compliance Center
                </h3>
                <span className="px-2 py-0.5 text-[10px] font-semibold bg-teal-500/20 text-teal-300 border border-teal-500/30 rounded-full">
                  DPDP Act 2023
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Healthcare data governance adhering to Indian privacy regulations and ABDM standards
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

        {/* Settings Body */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4 text-xs">
          {/* 1. Explicit Consent */}
          <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800 flex items-center justify-between">
            <div>
              <div className="font-bold text-white flex items-center gap-1.5">
                <ShieldCheck className="h-4 w-4 text-emerald-400" />
                <span>Explicit Patient Recording Consent</span>
              </div>
              <p className="text-slate-400 text-[11px] mt-0.5">
                DPDP Act Section 6 requirement: Ambient recording requires active notice and consent.
              </p>
            </div>
            <button
              onClick={() => setConsentGranted(!consentGranted)}
              className={`px-3 py-1.5 rounded-lg font-bold transition-colors ${
                consentGranted
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                  : 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
              }`}
            >
              {consentGranted ? 'Consent Active' : 'Consent Revoked'}
            </button>
          </div>

          {/* 2. De-identification */}
          <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800 flex items-center justify-between">
            <div>
              <div className="font-bold text-white flex items-center gap-1.5">
                <EyeOff className="h-4 w-4 text-cyan-400" />
                <span>PII De-Identification & Masking</span>
              </div>
              <p className="text-slate-400 text-[11px] mt-0.5">
                Redacts phone numbers, residential addresses, and Aadhaar identifiers before cloud processing.
              </p>
            </div>
            <button
              onClick={() => setPiiMasking(!piiMasking)}
              className={`px-3 py-1.5 rounded-lg font-bold transition-colors ${
                piiMasking
                  ? 'bg-teal-500/20 text-teal-300 border border-teal-500/40'
                  : 'bg-slate-800 text-slate-400 border border-slate-700'
              }`}
            >
              {piiMasking ? 'Masking ON' : 'Masking OFF'}
            </button>
          </div>

          {/* 3. Ephemeral Audio */}
          <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800 flex items-center justify-between">
            <div>
              <div className="font-bold text-white flex items-center gap-1.5">
                <Trash2 className="h-4 w-4 text-amber-400" />
                <span>Ephemeral Audio Retention</span>
              </div>
              <p className="text-slate-400 text-[11px] mt-0.5">
                Deletes raw audio buffer immediately upon clinical note approval to minimize storage risk.
              </p>
            </div>
            <button
              onClick={() => setEphemeralAudio(!ephemeralAudio)}
              className={`px-3 py-1.5 rounded-lg font-bold transition-colors ${
                ephemeralAudio
                  ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                  : 'bg-slate-800 text-slate-400 border border-slate-700'
              }`}
            >
              {ephemeralAudio ? 'Purge on Approval' : 'Retain 90 Days'}
            </button>
          </div>

          {/* 4. Immutable Audit Trail */}
          <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800">
            <span className="font-bold text-white flex items-center gap-1.5 mb-2">
              <History className="h-4 w-4 text-indigo-400" />
              <span>Immutable Audit Trail (Recent Activity)</span>
            </span>
            <div className="space-y-1.5 font-mono text-[10px] text-slate-400">
              <div className="p-1.5 bg-slate-950 rounded border border-slate-800 flex justify-between">
                <span>[LOGIN] Doctor authenticated via JWT (KMC-2019-45678)</span>
                <span className="text-slate-500">Today 10:15:02</span>
              </div>
              <div className="p-1.5 bg-slate-950 rounded border border-slate-800 flex justify-between">
                <span>[CONSENT] Patient Rahul Kumar granted recording consent</span>
                <span className="text-slate-500">Today 10:16:11</span>
              </div>
              <div className="p-1.5 bg-slate-950 rounded border border-slate-800 flex justify-between">
                <span>[TRANSCRIBE] AI4Bharat IndicConformer processed audio buffer</span>
                <span className="text-slate-500">Today 10:18:45</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-900/60 flex items-center justify-between text-xs text-slate-400">
          <span>Encrypted at rest (AES-256) and in transit (TLS 1.3)</span>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-bold transition-colors"
          >
            Close Privacy Center
          </button>
        </div>
      </div>
    </div>
  );
};
export default PrivacyCenterModal;
