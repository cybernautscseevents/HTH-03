'use client';

import React, { useState } from 'react';
import { 
  FileText, 
  CheckCircle, 
  Edit3, 
  Link2, 
  AlertCircle, 
  Stethoscope, 
  Pill, 
  Activity, 
  HelpCircle,
  ShieldCheck,
  Printer,
  Share2,
  Copy,
  Languages
} from 'lucide-react';

interface ClinicalNoteEditorProps {
  noteContent: any;
  isApproved: boolean;
  onApproveNote: () => void;
  onSelectEvidence: (segmentId: string) => void;
  onViewPatientSummary: () => void;
}

export const ClinicalNoteEditor: React.FC<ClinicalNoteEditorProps> = ({
  noteContent,
  isApproved,
  onApproveNote,
  onSelectEvidence,
  onViewPatientSummary,
}) => {
  const [activeTab, setActiveTab] = useState<'soap' | 'rx' | 'summary'>('soap');
  const [copied, setCopied] = useState<boolean>(false);

  const handleCopyNote = () => {
    navigator.clipboard.writeText(JSON.stringify(noteContent, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col h-full glass-panel rounded-xl border border-slate-800 overflow-hidden">
      {/* Note Header & Action Bar */}
      <div className="p-4 border-b border-slate-800/80 bg-slate-900/60 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <FileText className="h-4 w-4 text-teal-400" />
          <h2 className="text-sm font-bold text-white tracking-wide">
            Structured Clinical Note (Indian OPD)
          </h2>
          {isApproved ? (
            <span className="px-2 py-0.5 text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 rounded-full flex items-center gap-1">
              <CheckCircle className="h-3 w-3" /> Signed by Dr. Priya
            </span>
          ) : (
            <span className="px-2 py-0.5 text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40 rounded-full flex items-center gap-1">
              <Edit3 className="h-3 w-3" /> Pending Review
            </span>
          )}
        </div>

        {/* Header Tabs & Actions */}
        <div className="flex items-center gap-2">
          <div className="flex bg-slate-800 p-0.5 rounded-lg border border-slate-700 text-xs">
            <button
              onClick={() => setActiveTab('soap')}
              className={`px-2.5 py-1 rounded font-medium transition-colors ${
                activeTab === 'soap' ? 'bg-teal-500/20 text-teal-300' : 'text-slate-400 hover:text-white'
              }`}
            >
              SOAP Note
            </button>
            <button
              onClick={() => setActiveTab('rx')}
              className={`px-2.5 py-1 rounded font-medium transition-colors ${
                activeTab === 'rx' ? 'bg-teal-500/20 text-teal-300' : 'text-slate-400 hover:text-white'
              }`}
            >
              Prescription (Rx)
            </button>
          </div>

          <button
            onClick={onViewPatientSummary}
            className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 rounded-lg flex items-center gap-1 transition-colors"
            title="Generate patient leaflet in Kannada / Hindi"
          >
            <Languages className="h-3 w-3" />
            <span>Patient Leaflet</span>
          </button>

          <button
            onClick={handleCopyNote}
            className="p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg border border-slate-700 transition-colors"
            title="Copy Note JSON"
          >
            <Copy className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      {/* Note Content Body */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4 max-h-[600px] text-xs">
        {activeTab === 'soap' && (
          <>
            {/* 1. Chief Complaint */}
            <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-bold text-slate-300 uppercase tracking-wider text-[11px]">
                  Chief Complaint
                </span>
                <button
                  onClick={() => onSelectEvidence('seg-002')}
                  className="px-2 py-0.5 bg-teal-500/10 hover:bg-teal-500/20 text-teal-300 rounded border border-teal-500/30 flex items-center gap-1 text-[10px]"
                >
                  <Link2 className="h-2.5 w-2.5" />
                  <span>Grounding: seg-002 (96%)</span>
                </button>
              </div>
              <p className="text-slate-100 font-semibold text-sm">
                Fever — 3 days duration (Onset Monday night, max recorded 101.5°F)
              </p>
            </div>

            {/* 2. History of Present Illness (HPI) */}
            <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-bold text-slate-300 uppercase tracking-wider text-[11px]">
                  History of Present Illness (HPI)
                </span>
                <span className="text-[10px] text-slate-400 font-mono">Synthesized Narrative</span>
              </div>
              <p className="text-slate-200 leading-relaxed">
                42-year-old male presents with fever of 3 days duration. Fever started on Monday night, initially mild, worsened from Tuesday. Highest recorded temperature was 101.5°F yesterday. Associated with dry cough worse at night, mild rhinorrhea, generalized myalgia, and headache. Patient denies chest pain, breathlessness, vomiting, or diarrhea.
              </p>
            </div>

            {/* 3. Associated Symptoms & Negative Findings Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {/* Positive Symptoms */}
              <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="font-bold text-slate-300 uppercase tracking-wider text-[11px] block mb-2">
                  Associated Symptoms
                </span>
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between p-1.5 bg-slate-950 rounded border border-slate-800">
                    <span className="text-slate-200">Dry cough (nocturnal aggravation)</span>
                    <button onClick={() => onSelectEvidence('seg-008')} className="text-teal-400 text-[10px] font-mono hover:underline">seg-008</button>
                  </div>
                  <div className="flex items-center justify-between p-1.5 bg-slate-950 rounded border border-slate-800">
                    <span className="text-slate-200">Running nose (mild)</span>
                    <button onClick={() => onSelectEvidence('seg-010')} className="text-teal-400 text-[10px] font-mono hover:underline">seg-010</button>
                  </div>
                  <div className="flex items-center justify-between p-1.5 bg-slate-950 rounded border border-slate-800">
                    <span className="text-slate-200">Body pain & mild headache</span>
                    <button onClick={() => onSelectEvidence('seg-016')} className="text-teal-400 text-[10px] font-mono hover:underline">seg-016</button>
                  </div>
                </div>
              </div>

              {/* Negative / Pertinent Absent Findings */}
              <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-emerald-400 uppercase tracking-wider text-[11px]">
                    Negative Findings (Absence Verified)
                  </span>
                </div>
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between p-1.5 bg-emerald-950/20 rounded border border-emerald-500/20">
                    <span className="text-emerald-300 font-medium">No chest pain (Denies edeya novu)</span>
                    <button onClick={() => onSelectEvidence('seg-012')} className="text-emerald-400 text-[10px] font-mono hover:underline">seg-012</button>
                  </div>
                  <div className="flex items-center justify-between p-1.5 bg-emerald-950/20 rounded border border-emerald-500/20">
                    <span className="text-emerald-300 font-medium">No breathlessness (Denies usiru kattuvike)</span>
                    <button onClick={() => onSelectEvidence('seg-012')} className="text-emerald-400 text-[10px] font-mono hover:underline">seg-012</button>
                  </div>
                  <div className="flex items-center justify-between p-1.5 bg-emerald-950/20 rounded border border-emerald-500/20">
                    <span className="text-emerald-300 font-medium">No vomiting or loose stools</span>
                    <button onClick={() => onSelectEvidence('seg-014')} className="text-emerald-400 text-[10px] font-mono hover:underline">seg-014</button>
                  </div>
                </div>
              </div>
            </div>

            {/* 4. Vitals & Medical History */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="font-bold text-slate-300 uppercase tracking-wider text-[11px]">
                    Recorded Vitals
                  </span>
                  <button onClick={() => onSelectEvidence('seg-021')} className="text-teal-400 text-[10px] font-mono hover:underline">seg-021</button>
                </div>
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-slate-950 rounded border border-slate-800 text-center flex-1">
                    <span className="text-[10px] text-slate-400 block">Blood Pressure</span>
                    <span className="text-sm font-bold text-amber-300">140/90 mmHg</span>
                  </div>
                  <div className="p-2 bg-slate-950 rounded border border-slate-800 text-center flex-1">
                    <span className="text-[10px] text-slate-400 block">Temperature</span>
                    <span className="text-sm font-bold text-rose-300">101.5°F</span>
                  </div>
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="font-bold text-slate-300 uppercase tracking-wider text-[11px]">
                    Past Medical & Rx
                  </span>
                  <button onClick={() => onSelectEvidence('seg-020')} className="text-teal-400 text-[10px] font-mono hover:underline">seg-020</button>
                </div>
                <p className="text-slate-200">
                  <strong className="text-white">Hypertension:</strong> Diagnosed 1 year ago. Currently on Tab. Amlodipine 5mg OD.
                </p>
                <p className="text-amber-300 mt-1 font-medium text-[11px]">
                  ⚠️ Chart Allergy: Penicillin
                </p>
              </div>
            </div>

            {/* 5. Assessment (AI Suggestion Badge) */}
            <div className="p-3.5 rounded-xl bg-slate-900/60 border border-teal-500/30">
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-slate-200 uppercase tracking-wider text-[11px]">
                    Clinical Assessment
                  </span>
                  <span className="px-2 py-0.5 text-[9px] bg-teal-500/10 text-teal-300 border border-teal-500/30 rounded-full">
                    AI Suggestion — Physician Review Required
                  </span>
                </div>
              </div>
              <p className="text-white font-bold text-sm">
                Acute Febrile Illness with Upper Respiratory Tract Symptoms
              </p>
              <p className="text-slate-400 text-[11px] mt-1">
                Differential: Viral upper respiratory tract infection vs seasonal influenza. Under evaluation.
              </p>
            </div>
          </>
        )}

        {/* Prescription View */}
        {activeTab === 'rx' && (
          <div className="space-y-3">
            <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="font-bold text-slate-300 uppercase tracking-wider text-[11px] block mb-2">
                Medication Orders (Prescription)
              </span>
              <div className="space-y-2">
                <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-between">
                  <div>
                    <div className="font-bold text-white text-xs">1. Tab. Paracetamol 500mg</div>
                    <div className="text-slate-400 text-[11px]">1 tablet every 6 hours SOS / TDS (after food) • 3 days</div>
                  </div>
                  <button onClick={() => onSelectEvidence('seg-022')} className="text-teal-400 text-[10px] font-mono hover:underline">seg-022</button>
                </div>

                <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-between">
                  <div>
                    <div className="font-bold text-white text-xs">2. Cough Syrup (Expectorant/Suppressant)</div>
                    <div className="text-slate-400 text-[11px]">5ml twice daily (BD) • 5 days</div>
                  </div>
                  <button onClick={() => onSelectEvidence('seg-023')} className="text-teal-400 text-[10px] font-mono hover:underline">seg-023</button>
                </div>

                <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-between">
                  <div>
                    <div className="font-bold text-white text-xs">3. Tab. Amlodipine 5mg (Continue Current Rx)</div>
                    <div className="text-slate-400 text-[11px]">1 tablet once daily morning (OD) • Ongoing</div>
                  </div>
                  <button onClick={() => onSelectEvidence('seg-020')} className="text-teal-400 text-[10px] font-mono hover:underline">seg-020</button>
                </div>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="font-bold text-slate-300 uppercase tracking-wider text-[11px] block mb-1">
                Ordered Investigations & Advice
              </span>
              <p className="text-slate-200">
                • <strong>Labs:</strong> Complete Blood Count (CBC)
              </p>
              <p className="text-slate-200">
                • <strong>Imaging:</strong> Chest X-ray (PA view)
              </p>
              <p className="text-slate-300 mt-2">
                • <strong>Doctor Advice:</strong> Adequate fluid intake, steam inhalation, rest. Review in OPD after 2 days. Return immediately if breathlessness, persistent vomiting, or fever &gt; 102°F occurs.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Footer Doctor Approval Action */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-900/60 flex items-center justify-between">
        <div className="text-[11px] text-slate-400">
          {isApproved ? (
            <span className="text-emerald-400 font-medium">
              Verified & locked • Final EHR ready
            </span>
          ) : (
            <span>Doctor retains full clinical authority to edit or reject note</span>
          )}
        </div>

        <button
          onClick={onApproveNote}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all shadow-md ${
            isApproved
              ? 'bg-emerald-600 text-white cursor-default'
              : 'bg-teal-500 hover:bg-teal-400 text-slate-950 active:scale-95'
          }`}
        >
          <ShieldCheck className="h-4 w-4" />
          <span>{isApproved ? 'Approved & Locked' : 'Approve & Sign Clinical Record'}</span>
        </button>
      </div>
    </div>
  );
};
export default ClinicalNoteEditor;
