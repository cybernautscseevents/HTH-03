'use client';

import React from 'react';
import { 
  User, 
  Calendar, 
  AlertTriangle, 
  Globe2, 
  CheckCircle2, 
  Fingerprint, 
  HeartPulse,
  Clock
} from 'lucide-react';

interface PatientBannerProps {
  patient: {
    first_name: string;
    last_name: string;
    age: number;
    gender: string;
    blood_group: string;
    mrn: string;
    preferred_language: string;
  };
  consultation: {
    id: string;
    status: string;
    specialty: string;
    consent_obtained: boolean;
  };
}

export const PatientBanner: React.FC<PatientBannerProps> = ({
  patient,
  consultation,
}) => {
  return (
    <div className="w-full glass-panel rounded-xl p-4 sm:p-5 border border-slate-800 shadow-xl mb-6">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        {/* Left: Patient Identity */}
        <div className="flex items-start sm:items-center gap-4">
          <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 flex items-center justify-center shrink-0 text-slate-300">
            <User className="h-6 w-6 text-teal-400" />
          </div>

          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-lg sm:text-xl font-bold text-white tracking-tight">
                {patient.first_name} {patient.last_name}
              </h1>
              <span className="px-2 py-0.5 text-xs font-semibold bg-slate-800 text-slate-300 rounded border border-slate-700">
                {patient.age}Y • {patient.gender.toUpperCase()}
              </span>
              <span className="px-2 py-0.5 text-xs font-semibold bg-slate-800 text-rose-300 rounded border border-slate-700">
                {patient.blood_group}
              </span>
              <span className="text-xs text-slate-400 flex items-center gap-1 font-mono">
                <Fingerprint className="h-3.5 w-3.5 text-slate-500" />
                {patient.mrn}
              </span>
            </div>

            <div className="flex flex-wrap items-center gap-3 sm:gap-4 mt-2 text-xs text-slate-400">
              <div className="flex items-center gap-1.5">
                <Globe2 className="h-3.5 w-3.5 text-teal-400" />
                <span>Primary: Kannada + English (Code-mixed)</span>
              </div>
              <div className="flex items-center gap-1.5">
                <HeartPulse className="h-3.5 w-3.5 text-sky-400" />
                <span>History: Essential HTN (1 yr, Amlodipine 5mg)</span>
              </div>
              <div className="flex items-center gap-1.5 text-amber-300 font-medium">
                <AlertTriangle className="h-3.5 w-3.5 text-amber-400" />
                <span>Allergy: Penicillin (Rash)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Encounter Status & DPDP Consent */}
        <div className="flex flex-wrap items-center gap-2 sm:gap-3 pt-2 lg:pt-0 border-t lg:border-t-0 border-slate-800/80">
          {/* ABHA Badge */}
          <div className="px-3 py-1 bg-slate-900 border border-slate-800 rounded-lg flex items-center gap-2">
            <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">ABHA ID</span>
            <span className="text-xs font-mono text-teal-300">91-8822-4411-9988</span>
          </div>

          {/* Consent Status */}
          <div className="px-3 py-1 bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 rounded-lg flex items-center gap-1.5 text-xs font-medium">
            <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />
            <span>DPDP Consent Verified</span>
          </div>

          {/* OPD Status */}
          <div className="px-3 py-1 bg-teal-950/40 border border-teal-500/30 text-teal-300 rounded-lg flex items-center gap-1.5 text-xs font-medium">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-teal-500"></span>
            </span>
            <span>OPD Room 4 Active</span>
          </div>
        </div>
      </div>
    </div>
  );
};
export default PatientBanner;
