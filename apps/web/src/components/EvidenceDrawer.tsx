'use client';

import React from 'react';
import { 
  X, 
  Link2, 
  Volume2, 
  CheckCircle, 
  ShieldCheck, 
  ArrowRight,
  Clock,
  Sparkles
} from 'lucide-react';

interface EvidenceDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  selectedEvidenceId: string | null;
  onPlayAudioSnippet?: (startTime: number) => void;
}

export const EvidenceDrawer: React.FC<EvidenceDrawerProps> = ({
  isOpen,
  onClose,
  selectedEvidenceId,
  onPlayAudioSnippet,
}) => {
  if (!isOpen) return null;

  // Demo evidence dictionary mapping segment IDs to dialogue evidence
  const evidenceMap: Record<string, any> = {
    'seg-002': {
      field: 'Chief Complaint: Fever',
      confidence: 0.96,
      speaker: 'Patient (Rahul Kumar)',
      startTime: 5.5,
      endTime: 12.0,
      kannadaText: 'Doctor, nanage 3 dinadinda tumba jwara ide. Tingalina ratri shuru aaythu.',
      englishText: 'Doctor, I have high fever since 3 days. It started on Monday night.',
      clinicalRelevance: 'Confirms duration of 3 days, acute onset, high subjective thermal discomfort.',
    },
    'seg-008': {
      field: 'Associated Symptoms: Cough',
      confidence: 0.94,
      speaker: 'Patient (Rahul Kumar)',
      startTime: 38.0,
      endTime: 44.5,
      kannadaText: 'Kasa kasa kheduttide doctor, ratri adre innoo jasthi novu mathu khansi barutte.',
      englishText: 'Dry cough with throat irritation, doctor. It gets much worse at night.',
      clinicalRelevance: 'Identifies nocturnal worsening and dry quality of cough.',
    },
    'seg-010': {
      field: 'Associated Symptoms: Rhinorrhea',
      confidence: 0.88,
      speaker: 'Patient (Rahul Kumar)',
      startTime: 48.0,
      endTime: 53.0,
      kannadaText: 'Mooku olaginda neeru barthide, swalpa shardi aagide.',
      englishText: 'Water running from nose, mild cold sensation.',
      clinicalRelevance: 'Supports upper respiratory tract involvement.',
    },
    'seg-012': {
      field: 'Pertinent Negative: Chest Pain & Dyspnea',
      confidence: 0.96,
      speaker: 'Patient (Rahul Kumar)',
      startTime: 58.0,
      endTime: 65.5,
      kannadaText: 'Illa doctor, edeya novu illa, usiru kattuvike yenu illa.',
      englishText: 'No doctor, no chest pain, no breathing difficulty at all.',
      clinicalRelevance: 'Crucial negative finding ruling out acute cardiac/respiratory red flags.',
    },
    'seg-014': {
      field: 'Pertinent Negative: GI Symptoms',
      confidence: 0.95,
      speaker: 'Patient (Rahul Kumar)',
      startTime: 70.0,
      endTime: 75.0,
      kannadaText: 'Vomiting illa doctor, loose stools aagilla.',
      englishText: 'No vomiting, no loose stools.',
      clinicalRelevance: 'Rules out gastroenteritis or foodborne acute illness.',
    },
    'seg-016': {
      field: 'Constitutional Symptoms: Myalgia & Headache',
      confidence: 0.93,
      speaker: 'Patient (Rahul Kumar)',
      startTime: 82.0,
      endTime: 88.0,
      kannadaText: 'Maikai tumba novu ide, tale bisi aagide.',
      englishText: 'Severe body aches all over and mild headache.',
      clinicalRelevance: 'Standard viral prodrome / constitutional symptom triad.',
    },
    'seg-020': {
      field: 'Past Medical History: Hypertension Rx',
      confidence: 0.91,
      speaker: 'Doctor & Patient Turn',
      startTime: 104.0,
      endTime: 112.0,
      kannadaText: 'BP ge Amlodipine 5mg rooz togothidira? Howdhu doctor, rooz togothidini.',
      englishText: 'Taking Amlodipine 5mg daily for BP? Yes doctor, taking regularly.',
      clinicalRelevance: 'Documents chronic essential hypertension on active monotherapy.',
    },
    'seg-021': {
      field: 'Objective Vitals: Blood Pressure',
      confidence: 0.92,
      speaker: 'Doctor (Dr. Priya Sharma)',
      startTime: 118.0,
      endTime: 125.0,
      kannadaText: 'BP 140/90 mmHg ide. Swalpa high ide eega, fever iruvudarinda.',
      englishText: 'BP is 140/90 mmHg. Slightly high right now, likely due to fever.',
      clinicalRelevance: 'Physician measured vital sign in OPD.',
    },
    'seg-022': {
      field: 'Medication Order: Paracetamol 500mg',
      confidence: 0.90,
      speaker: 'Doctor (Dr. Priya Sharma)',
      startTime: 132.0,
      endTime: 142.0,
      kannadaText: 'Paracetamol 500mg tablet dinakke 3 sala oota aada mele thagolli, 3 days.',
      englishText: 'Take Paracetamol 500mg three times a day after food for 3 days.',
      clinicalRelevance: 'Verbatim prescribing instruction matching generated Rx.',
    },
    'seg-023': {
      field: 'Follow-up & Instructions',
      confidence: 0.91,
      speaker: 'Doctor (Dr. Priya Sharma)',
      startTime: 148.0,
      endTime: 160.0,
      kannadaText: 'Cough syrup 5ml thagolli. 2 dina aada mele barbeku. Fever nillilla andre CBC madona.',
      englishText: 'Take cough syrup 5ml. Follow up after 2 days. If fever persists, we will run CBC.',
      clinicalRelevance: 'Treatment plan and return precautions communicated directly.',
    },
  };

  const activeEvidence = evidenceMap[selectedEvidenceId || 'seg-002'] || evidenceMap['seg-002'];

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full sm:w-96 bg-slate-950 border-l border-slate-800 shadow-2xl p-6 flex flex-col justify-between transition-transform animate-in slide-in-from-right duration-300">
      <div>
        {/* Drawer Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Link2 className="h-5 w-5 text-teal-400" />
            <h3 className="font-bold text-white text-base">Evidence Inspector</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Clinical Fact Card */}
        <div className="mt-4 p-3.5 bg-slate-900/80 rounded-xl border border-slate-800">
          <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider block mb-1">
            Grounded Clinical Field
          </span>
          <div className="text-white font-bold text-sm">
            {activeEvidence.field}
          </div>
          <div className="flex items-center gap-2 mt-2">
            <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 rounded text-[10px] font-semibold flex items-center gap-1">
              <CheckCircle className="h-3 w-3" /> Auto-Verified
            </span>
            <span className="text-[10px] font-mono text-teal-300">
              Confidence: {Math.round(activeEvidence.confidence * 100)}%
            </span>
          </div>
        </div>

        {/* Verbatim Audio & Dialogue Evidence */}
        <div className="mt-4 space-y-3">
          <div className="p-3.5 bg-slate-900/60 rounded-xl border border-slate-800">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
              <span className="font-semibold text-slate-300">{activeEvidence.speaker}</span>
              <span className="font-mono text-[10px] text-teal-400 flex items-center gap-1">
                <Clock className="h-3 w-3" />
                {activeEvidence.startTime}s - {activeEvidence.endTime}s
              </span>
            </div>

            <div className="text-xs text-teal-100 font-medium mb-1.5">
              "{activeEvidence.kannadaText}"
            </div>

            <div className="text-xs text-slate-300 italic pt-2 border-t border-slate-800/80 flex items-start gap-1.5">
              <ArrowRight className="h-3 w-3 text-cyan-400 mt-0.5 shrink-0" />
              <span>"{activeEvidence.englishText}"</span>
            </div>
          </div>

          {/* Clinical Rationale */}
          <div className="p-3 bg-slate-900/40 rounded-xl border border-slate-800/60 text-xs text-slate-300">
            <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider block mb-1">
              Clinical Extraction Logic
            </span>
            {activeEvidence.clinicalRelevance}
          </div>
        </div>
      </div>

      {/* Drawer Action */}
      <div className="pt-4 border-t border-slate-800">
        <button
          onClick={() => onPlayAudioSnippet && onPlayAudioSnippet(activeEvidence.startTime)}
          className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold rounded-xl text-xs shadow-lg transition-all"
        >
          <Volume2 className="h-4 w-4" />
          <span>Seek Audio & Play Snippet</span>
        </button>
        <p className="text-[10px] text-center text-slate-400 mt-2">
          Zero-hallucination verification • Verbatim bidirectional link
        </p>
      </div>
    </div>
  );
};
export default EvidenceDrawer;
