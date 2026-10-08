'use client';

import React, { useState } from 'react';
import { 
  History, 
  Calendar, 
  ArrowRight, 
  TrendingUp, 
  FileText, 
  CheckCircle2, 
  Activity, 
  Pill,
  GitCompare,
  Stethoscope,
  ChevronRight
} from 'lucide-react';

interface TimelineEncounter {
  id: string;
  date: string;
  specialty: string;
  doctor: string;
  chiefComplaint: string;
  vitals: {
    bp: string;
    temp: string;
  };
  diagnoses: string[];
  medications: string[];
  status: string;
  keyChanges?: string;
}

const HISTORICAL_ENCOUNTERS: TimelineEncounter[] = [
  {
    id: 'enc-003-current',
    date: '08 OCT 2026 (Today)',
    specialty: 'General Medicine',
    doctor: 'Dr. Priya Sharma',
    chiefComplaint: 'Fever x 3 days, dry cough worse at night, body ache',
    vitals: { bp: '140/90 mmHg', temp: '101.5°F' },
    diagnoses: ['Acute Febrile Illness (Upper Respiratory Tract)'],
    medications: ['Paracetamol 500mg TDS', 'Cough Syrup 5ml BD', 'Amlodipine 5mg OD (continued)'],
    status: 'In Progress / AI Drafted',
    keyChanges: 'Acute fever onset; blood pressure transiently elevated (140/90 vs baseline 126/82).'
  },
  {
    id: 'enc-002-past',
    date: '15 SEP 2026 (3 Weeks Ago)',
    specialty: 'General Medicine',
    doctor: 'Dr. Priya Sharma',
    chiefComplaint: 'Routine Hypertension Follow-up; asymptomatic',
    vitals: { bp: '126/82 mmHg', temp: '98.4°F' },
    diagnoses: ['Essential Hypertension — Well Controlled'],
    medications: ['Amlodipine 5mg OD'],
    status: 'Completed',
    keyChanges: 'Blood pressure well controlled on Amlodipine 5mg. Advised sodium restriction.'
  },
  {
    id: 'enc-001-past',
    date: '12 MAY 2026 (5 Months Ago)',
    specialty: 'General Medicine',
    doctor: 'Dr. Rajesh Rao',
    chiefComplaint: 'Exertional headache, mild dizziness during physical activity',
    vitals: { bp: '152/96 mmHg', temp: '98.6°F' },
    diagnoses: ['New-Onset Stage 1 Essential Hypertension'],
    medications: ['Initiated Tab. Amlodipine 5mg OD'],
    status: 'Completed',
    keyChanges: 'Initial hypertension diagnosis. Baseline ECG, serum creatinine, and lipid profile normal.'
  }
];

export const PatientTimeline: React.FC = () => {
  const [selectedEncounter, setSelectedEncounter] = useState<TimelineEncounter>(HISTORICAL_ENCOUNTERS[0]);
  const [compareMode, setCompareMode] = useState<boolean>(false);
  const [compareEncounter, setCompareEncounter] = useState<TimelineEncounter>(HISTORICAL_ENCOUNTERS[1]);

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <History className="h-6 w-6 text-teal-400" />
            Longitudinal Patient Timeline & Encounter History
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Chronological OPD encounters, recurring clinical findings, and visit comparisons
          </p>
        </div>

        <button
          onClick={() => setCompareMode(!compareMode)}
          className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all shadow-md ${
            compareMode
              ? 'bg-teal-500 text-slate-950 font-bold'
              : 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700'
          }`}
        >
          <GitCompare className="h-3.5 w-3.5" />
          <span>{compareMode ? 'Exit Comparison' : 'Compare Visits'}</span>
        </button>
      </div>

      {/* Compare Visits Side-by-Side View */}
      {compareMode ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 p-5 glass-panel rounded-2xl border border-teal-500/30">
          {/* Visit A: Current Visit */}
          <div className="space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <span className="text-xs font-bold text-teal-300 uppercase tracking-wide">
                Current Encounter ({selectedEncounter.date})
              </span>
              <span className="px-2 py-0.5 text-[10px] bg-teal-500/10 text-teal-300 rounded border border-teal-500/30">
                {selectedEncounter.doctor}
              </span>
            </div>

            <div className="p-3 bg-slate-900/80 rounded-xl border border-slate-800 text-xs">
              <span className="font-semibold text-slate-400 block mb-1">Chief Complaints & Narrative</span>
              <p className="text-slate-200">{selectedEncounter.chiefComplaint}</p>
            </div>

            <div className="p-3 bg-slate-900/80 rounded-xl border border-slate-800 text-xs">
              <span className="font-semibold text-slate-400 block mb-1">Vital Signs</span>
              <div className="flex gap-4">
                <span className="text-slate-200 font-mono">BP: <strong className="text-amber-300">{selectedEncounter.vitals.bp}</strong></span>
                <span className="text-slate-200 font-mono">Temp: <strong className="text-rose-300">{selectedEncounter.vitals.temp}</strong></span>
              </div>
            </div>

            <div className="p-3 bg-slate-900/80 rounded-xl border border-slate-800 text-xs">
              <span className="font-semibold text-slate-400 block mb-1">Active Prescriptions</span>
              <ul className="list-disc list-inside space-y-1 text-slate-200">
                {selectedEncounter.medications.map((m, i) => <li key={i}>{m}</li>)}
              </ul>
            </div>
          </div>

          {/* Visit B: Previous Encounter */}
          <div className="space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-cyan-300 uppercase tracking-wide">
                  Comparing Against:
                </span>
                <select
                  value={compareEncounter.id}
                  onChange={(e) => {
                    const found = HISTORICAL_ENCOUNTERS.find(x => x.id === e.target.value);
                    if (found) setCompareEncounter(found);
                  }}
                  className="bg-slate-900 text-slate-200 border border-slate-700 text-xs rounded px-2 py-0.5"
                >
                  {HISTORICAL_ENCOUNTERS.filter(x => x.id !== selectedEncounter.id).map(enc => (
                    <option key={enc.id} value={enc.id}>{enc.date}</option>
                  ))}
                </select>
              </div>
              <span className="px-2 py-0.5 text-[10px] bg-slate-800 text-slate-400 rounded">
                {compareEncounter.doctor}
              </span>
            </div>

            <div className="p-3 bg-slate-900/80 rounded-xl border border-slate-800 text-xs">
              <span className="font-semibold text-slate-400 block mb-1">Chief Complaints & Narrative</span>
              <p className="text-slate-200">{compareEncounter.chiefComplaint}</p>
            </div>

            <div className="p-3 bg-slate-900/80 rounded-xl border border-slate-800 text-xs">
              <span className="font-semibold text-slate-400 block mb-1">Vital Signs</span>
              <div className="flex gap-4">
                <span className="text-slate-200 font-mono">BP: <strong className="text-emerald-300">{compareEncounter.vitals.bp}</strong></span>
                <span className="text-slate-200 font-mono">Temp: <strong className="text-slate-200">{compareEncounter.vitals.temp}</strong></span>
              </div>
            </div>

            <div className="p-3 bg-slate-900/80 rounded-xl border border-slate-800 text-xs">
              <span className="font-semibold text-slate-400 block mb-1">Active Prescriptions</span>
              <ul className="list-disc list-inside space-y-1 text-slate-200">
                {compareEncounter.medications.map((m, i) => <li key={i}>{m}</li>)}
              </ul>
            </div>
          </div>
        </div>
      ) : null}

      {/* Main Longitudinal Timeline Feed */}
      <div className="space-y-4">
        {HISTORICAL_ENCOUNTERS.map((enc, idx) => {
          const isLatest = idx === 0;

          return (
            <div
              key={enc.id}
              onClick={() => setSelectedEncounter(enc)}
              className={`p-5 rounded-2xl glass-panel border transition-all cursor-pointer ${
                selectedEncounter.id === enc.id
                  ? 'border-teal-500/50 bg-slate-900/90 shadow-lg shadow-teal-500/10'
                  : 'border-slate-800/80 hover:border-slate-700 bg-slate-900/40'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-xl ${isLatest ? 'bg-teal-500/20 text-teal-400 border border-teal-500/30' : 'bg-slate-800 text-slate-400'}`}>
                    <Calendar className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white flex items-center gap-2">
                      {enc.date}
                      {isLatest && (
                        <span className="px-2 py-0.5 text-[10px] font-bold bg-teal-500/20 text-teal-300 border border-teal-500/40 rounded-full">
                          Current Visit
                        </span>
                      )}
                    </h3>
                    <p className="text-xs text-slate-400">
                      {enc.specialty} • {enc.doctor}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 text-xs">
                  <div className="px-2.5 py-1 bg-slate-950 rounded-lg border border-slate-800 font-mono text-[11px]">
                    BP: <span className="text-amber-300 font-semibold">{enc.vitals.bp}</span>
                  </div>
                  <div className="px-2.5 py-1 bg-slate-950 rounded-lg border border-slate-800 font-mono text-[11px]">
                    Temp: <span className="text-rose-300 font-semibold">{enc.vitals.temp}</span>
                  </div>
                </div>
              </div>

              {/* Encounter Summary Details */}
              <div className="space-y-2 text-xs text-slate-300 mt-2">
                <p>
                  <strong className="text-slate-200">Presentation:</strong> {enc.chiefComplaint}
                </p>
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {enc.diagnoses.map((diag, i) => (
                    <span key={i} className="px-2 py-0.5 bg-slate-800 text-teal-300 rounded text-[10px] font-medium border border-slate-700">
                      {diag}
                    </span>
                  ))}
                  {enc.medications.map((med, i) => (
                    <span key={i} className="px-2 py-0.5 bg-slate-800/80 text-cyan-300 rounded text-[10px] font-mono border border-slate-700/60">
                      Rx: {med}
                    </span>
                  ))}
                </div>
                {enc.keyChanges && (
                  <p className="text-[11px] text-slate-400 italic pt-1 border-t border-slate-800/60">
                    Clinical observation: {enc.keyChanges}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
export default PatientTimeline;
