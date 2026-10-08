'use client';

import React from 'react';
import { 
  Stethoscope, 
  ShieldCheck, 
  Activity, 
  FileText, 
  BarChart3, 
  Lock, 
  Sparkles,
  UserCheck
} from 'lucide-react';

interface NavbarProps {
  activeTab: 'scribe' | 'timeline' | 'evaluation' | 'privacy';
  setActiveTab: (tab: 'scribe' | 'timeline' | 'evaluation' | 'privacy') => void;
  onOpenFHIR: () => void;
  onOpenSafety: () => void;
  safetyFlagCount: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  onOpenFHIR,
  onOpenSafety,
  safetyFlagCount,
}) => {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-teal-500 to-cyan-400 p-0.5 shadow-lg shadow-teal-500/20">
            <div className="h-full w-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Stethoscope className="h-5 w-5 text-teal-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-teal-300 via-cyan-200 to-white bg-clip-text text-transparent">
                ClinScribe AI
              </span>
              <span className="px-2 py-0.5 text-[10px] font-semibold bg-teal-500/10 text-teal-300 border border-teal-500/30 rounded-full">
                HC-02 Indian OPD
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">
              From Conversation to Clinical Intelligence
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1 sm:gap-2">
          <button
            onClick={() => setActiveTab('scribe')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'scribe'
                ? 'bg-teal-500/20 text-teal-300 border border-teal-500/40 shadow-sm shadow-teal-500/10'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
            }`}
          >
            <Activity className="h-3.5 w-3.5" />
            <span>Ambient Scribe</span>
          </button>

          <button
            onClick={() => setActiveTab('evaluation')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'evaluation'
                ? 'bg-teal-500/20 text-teal-300 border border-teal-500/40'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
            }`}
          >
            <BarChart3 className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Metrics & Evaluation</span>
            <span className="sm:hidden">Metrics</span>
          </button>

          <button
            onClick={() => setActiveTab('privacy')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'privacy'
                ? 'bg-teal-500/20 text-teal-300 border border-teal-500/40'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
            }`}
          >
            <Lock className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">DPDP & Compliance</span>
            <span className="sm:hidden">DPDP</span>
          </button>
        </nav>

        {/* Quick Actions & Doctor Profile */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Safety Alert Indicator Button */}
          {safetyFlagCount > 0 && (
            <button
              onClick={onOpenSafety}
              className="relative flex items-center gap-1.5 px-2.5 py-1.5 bg-amber-500/15 text-amber-300 border border-amber-500/30 rounded-lg text-xs font-medium hover:bg-amber-500/25 transition-all animate-pulse"
              title="Clinical safety alerts detected"
            >
              <ShieldCheck className="h-3.5 w-3.5 text-amber-400" />
              <span>{safetyFlagCount} Flags</span>
            </button>
          )}

          {/* FHIR Export Trigger */}
          <button
            onClick={onOpenFHIR}
            className="flex items-center gap-1.5 px-2.5 py-1.5 bg-slate-900 text-slate-300 border border-slate-700/60 rounded-lg text-xs font-medium hover:bg-slate-800 hover:text-white transition-all"
            title="Export to ABDM / FHIR R4 Bundle"
          >
            <FileText className="h-3.5 w-3.5 text-cyan-400" />
            <span className="hidden md:inline">ABDM FHIR</span>
          </button>

          {/* Doctor Badge */}
          <div className="flex items-center gap-2.5 pl-2 sm:pl-3 border-l border-slate-800">
            <div className="h-8 w-8 rounded-full bg-slate-800 border border-teal-500/40 flex items-center justify-center text-teal-300 text-xs font-semibold">
              PS
            </div>
            <div className="hidden lg:block text-left">
              <div className="text-xs font-medium text-slate-200">Dr. Priya Sharma</div>
              <div className="text-[10px] text-slate-400">Gen Medicine • KMC-2019</div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
export default Navbar;
