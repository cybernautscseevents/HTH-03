'use client';

import React, { useState } from 'react';
import { Navbar } from '@/components/Navbar';
import { PatientBanner } from '@/components/PatientBanner';
import { AmbientRecorder } from '@/components/AmbientRecorder';
import { TranscriptStream, TranscriptSegment } from '@/components/TranscriptStream';
import { ClinicalNoteEditor } from '@/components/ClinicalNoteEditor';
import { EvidenceDrawer } from '@/components/EvidenceDrawer';
import { SafetyAlertsModal } from '@/components/SafetyAlertsModal';
import { PatientSummaryView } from '@/components/PatientSummaryView';
import { EvaluationDashboard } from '@/components/EvaluationDashboard';
import { FHIRExportModal } from '@/components/FHIRExportModal';
import { PrivacyCenterModal } from '@/components/PrivacyCenterModal';
import { PatientTimeline } from '@/components/PatientTimeline';
import { Sparkles, Info, ShieldAlert } from 'lucide-react';

// Pre-seeded high fidelity synthetic consultation data for Indian OPD
const INITIAL_PATIENT = {
  first_name: 'Rahul',
  last_name: 'Kumar',
  age: 42,
  gender: 'male',
  blood_group: 'B+',
  mrn: 'MRN-2026-0001',
  preferred_language: 'kn',
};

const INITIAL_CONSULTATION = {
  id: 'consult-demo-001',
  status: 'completed',
  specialty: 'General Medicine',
  consent_obtained: true,
};

const INITIAL_SEGMENTS: TranscriptSegment[] = [
  {
    id: 'seg-001',
    segment_index: 0,
    speaker: 'Doctor (Dr. Priya)',
    start_time: 0.0,
    end_time: 4.8,
    original_text: 'Namaskara Rahul avare. Kootkoli. Yenu samasye aagide?',
    english_translation: 'Hello Rahul. Please have a seat. What problem brings you here today?',
    language: 'kn-IN',
    confidence: 0.98,
  },
  {
    id: 'seg-002',
    segment_index: 1,
    speaker: 'Patient (Rahul K)',
    start_time: 5.5,
    end_time: 14.2,
    original_text: 'Doctor, nanage 3 dinadinda tumba jwara ide. Tingalina ratri shuru aaythu. Swalpa tale novu kooda ide.',
    english_translation: 'Doctor, I have high fever since 3 days. It started on Monday night. I also have some headache.',
    language: 'kn-IN',
    confidence: 0.96,
  },
  {
    id: 'seg-004',
    segment_index: 2,
    speaker: 'Doctor (Dr. Priya)',
    start_time: 15.0,
    end_time: 21.0,
    original_text: 'Temperature measure maadidra mane alli? How high did it go?',
    english_translation: 'Did you measure temperature at home? How high did it go?',
    language: 'Code-mixed',
    confidence: 0.97,
  },
  {
    id: 'seg-006',
    segment_index: 3,
    speaker: 'Patient (Rahul K)',
    start_time: 22.0,
    end_time: 28.5,
    original_text: 'Haudhu doctor, ninne check maadidde thermometer alli, 101.5°F toristhithu.',
    english_translation: 'Yes doctor, I checked yesterday with thermometer, it showed 101.5°F.',
    language: 'kn-IN',
    confidence: 0.95,
  },
  {
    id: 'seg-008',
    segment_index: 4,
    speaker: 'Patient (Rahul K)',
    start_time: 38.0,
    end_time: 46.0,
    original_text: 'Kasa kasa kheduttide doctor, ratri adre innoo jasthi novu mathu khansi barutte.',
    english_translation: 'Dry cough with irritation, doctor. At night the cough and discomfort becomes worse.',
    language: 'kn-IN',
    confidence: 0.94,
  },
  {
    id: 'seg-010',
    segment_index: 5,
    speaker: 'Patient (Rahul K)',
    start_time: 48.0,
    end_time: 54.0,
    original_text: 'Mooku olaginda neeru barthide, swalpa shardi aagide.',
    english_translation: 'Water running from nose, mild cold sensation.',
    language: 'kn-IN',
    confidence: 0.91,
  },
  {
    id: 'seg-012',
    segment_index: 6,
    speaker: 'Patient (Rahul K)',
    start_time: 58.0,
    end_time: 66.0,
    original_text: 'Illa doctor, edeya novu illa, usiru kattuvike yenu illa.',
    english_translation: 'No doctor, no chest pain, no breathing difficulty at all.',
    language: 'kn-IN',
    confidence: 0.96,
  },
  {
    id: 'seg-014',
    segment_index: 7,
    speaker: 'Patient (Rahul K)',
    start_time: 70.0,
    end_time: 77.0,
    original_text: 'Vomiting illa doctor, loose stools aagilla.',
    english_translation: 'No vomiting, no loose stools.',
    language: 'kn-IN',
    confidence: 0.95,
  },
  {
    id: 'seg-016',
    segment_index: 8,
    speaker: 'Patient (Rahul K)',
    start_time: 82.0,
    end_time: 90.0,
    original_text: 'Maikai tumba novu ide, tale bisi aagide.',
    english_translation: 'Severe body aches all over and feeling hot in head.',
    language: 'kn-IN',
    confidence: 0.93,
  },
  {
    id: 'seg-018',
    segment_index: 9,
    speaker: 'Doctor (Dr. Priya)',
    start_time: 92.0,
    end_time: 98.0,
    original_text: 'Yaavadaadru aushadhi ge allergy ideya? Any drug allergies?',
    english_translation: 'Are you allergic to any medicines? Any drug allergies?',
    language: 'Code-mixed',
    confidence: 0.96,
  },
  {
    id: 'seg-020',
    segment_index: 10,
    speaker: 'Doctor (Dr. Priya)',
    start_time: 104.0,
    end_time: 114.0,
    original_text: 'BP ge Amlodipine 5mg rooz togothidira? Continue that as usual.',
    english_translation: 'Taking Amlodipine 5mg daily for blood pressure? Continue that as usual.',
    language: 'Code-mixed',
    confidence: 0.92,
  },
  {
    id: 'seg-021',
    segment_index: 11,
    speaker: 'Doctor (Dr. Priya)',
    start_time: 118.0,
    end_time: 126.0,
    original_text: 'BP 140/90 mmHg ide. Swalpa high ide eega, fever iruvudarinda.',
    english_translation: 'Blood pressure is 140/90 mmHg. Slightly high right now due to fever.',
    language: 'kn-IN',
    confidence: 0.93,
  },
  {
    id: 'seg-022',
    segment_index: 12,
    speaker: 'Doctor (Dr. Priya)',
    start_time: 132.0,
    end_time: 144.0,
    original_text: 'Paracetamol 500mg tablet dinakke 3 sala oota aada mele thagolli, 3 days ge.',
    english_translation: 'Take Paracetamol 500mg tablet three times daily after meals for 3 days.',
    language: 'Code-mixed',
    confidence: 0.94,
  },
  {
    id: 'seg-023',
    segment_index: 13,
    speaker: 'Doctor (Dr. Priya)',
    start_time: 148.0,
    end_time: 162.0,
    original_text: 'Cough syrup 5ml thagolli BD. 2 dina aada mele barbeku. Paravagilla, husharagi hogubanni.',
    english_translation: 'Take cough syrup 5ml twice daily. Review after 2 days. Take care.',
    language: 'Code-mixed',
    confidence: 0.92,
  },
];

const INITIAL_SAFETY_FLAGS = [
  {
    id: 'FLAG-ALLERGY-01',
    severity: 'warning',
    category: 'allergy',
    message: 'Patient record contains documented Penicillin allergy. Verify all prescribed antibiotic classes.',
    recommendation: 'Ensure no Beta-Lactam antibiotics (Amoxicillin/Augmentin) are prescribed.',
    resolved: false,
  },
  {
    id: 'FLAG-VITAL-01',
    severity: 'info',
    category: 'vitals',
    message: 'Elevated Blood Pressure recorded (140/90 mmHg) in known hypertensive on Amlodipine.',
    recommendation: 'Recheck resting blood pressure at follow-up after fever resolves.',
    resolved: false,
  },
];

const DEMO_FHIR_BUNDLE = {
  resourceType: 'Bundle',
  id: 'bundle-clinsribe-demo-001',
  meta: {
    profile: ['https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle'],
  },
  type: 'document',
  timestamp: new Date().toISOString(),
  entry: [
    {
      fullUrl: 'urn:uuid:pat-demo-001',
      resource: {
        resourceType: 'Patient',
        id: 'pat-demo-001',
        identifier: [{ system: 'https://abdm.gov.in/abha', value: '91-8822-4411-9988' }],
        name: [{ text: 'Rahul Kumar' }],
        gender: 'male',
        birthDate: '1984-05-15',
      },
    },
    {
      fullUrl: 'urn:uuid:doc-demo-001',
      resource: {
        resourceType: 'Practitioner',
        id: 'doc-demo-001',
        identifier: [{ system: 'https://nmc.org.in/registration', value: 'KMC-2019-45678' }],
        name: [{ text: 'Dr. Priya Sharma' }],
      },
    },
    {
      fullUrl: 'urn:uuid:enc-demo-001',
      resource: {
        resourceType: 'Encounter',
        id: 'enc-demo-001',
        status: 'finished',
        class: { code: 'AMB', display: 'ambulatory' },
        subject: { reference: 'Patient/pat-demo-001' },
      },
    },
    {
      fullUrl: 'urn:uuid:cond-001',
      resource: {
        resourceType: 'Condition',
        id: 'cond-001',
        clinicalStatus: { coding: [{ code: 'active' }] },
        code: { text: 'Acute Febrile Illness with Upper Respiratory Tract Symptoms' },
        subject: { reference: 'Patient/pat-demo-001' },
      },
    },
    {
      fullUrl: 'urn:uuid:med-001',
      resource: {
        resourceType: 'MedicationRequest',
        id: 'med-001',
        status: 'active',
        intent: 'order',
        medicationCodeableConcept: { text: 'Paracetamol 500mg' },
        dosageInstruction: [{ text: '1 tablet TDS after meals for 3 days' }],
      },
    },
  ],
};

export default function Home() {
  const [activeTab, setActiveTab] = useState<'scribe' | 'timeline' | 'evaluation' | 'privacy'>('scribe');
  const [selectedSpecialty, setSelectedSpecialty] = useState<string>('General Medicine');
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [isApproved, setIsApproved] = useState<boolean>(false);

  // Evidence Drawer State
  const [selectedEvidenceId, setSelectedEvidenceId] = useState<string | null>(null);
  const [isEvidenceOpen, setIsEvidenceOpen] = useState<boolean>(false);

  // Audio Playback Seek
  const [activeAudioTime, setActiveAudioTime] = useState<number>(0);

  // Modals
  const [isSafetyOpen, setIsSafetyOpen] = useState<boolean>(false);
  const [isFHIROpen, setIsFHIROpen] = useState<boolean>(false);
  const [isPatientSummaryOpen, setIsPatientSummaryOpen] = useState<boolean>(false);
  const [isPrivacyOpen, setIsPrivacyOpen] = useState<boolean>(false);

  // Data
  const [safetyFlags, setSafetyFlags] = useState<any[]>(INITIAL_SAFETY_FLAGS);

  // Trigger Evidence Inspector
  const handleSelectEvidence = (segmentId: string) => {
    setSelectedEvidenceId(segmentId);
    setIsEvidenceOpen(true);
  };

  // Seek and play snippet
  const handlePlaySnippet = (startTime: number) => {
    setActiveAudioTime(startTime);
  };

  // Run Ambient OPD Demo Simulation
  const handleRunDemoPipeline = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      setIsRecording(false);
      setSelectedEvidenceId('seg-002');
      setIsEvidenceOpen(true);
    }, 1200);
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col text-slate-100">
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        selectedSpecialty={selectedSpecialty}
        setSelectedSpecialty={setSelectedSpecialty}
        onOpenFHIR={() => setIsFHIROpen(true)}
        onOpenSafety={() => setIsSafetyOpen(true)}
        safetyFlagCount={safetyFlags.length}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Safety Alert Strip (if flags present) */}
        {safetyFlags.length > 0 && activeTab === 'scribe' && (
          <div className="mb-4 p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl flex items-center justify-between text-xs text-amber-200">
            <div className="flex items-center gap-2">
              <ShieldAlert className="h-4 w-4 text-amber-400 shrink-0" />
              <span>
                <strong>{safetyFlags.length} Clinical Guardrail Alerts:</strong> Documented Penicillin allergy and elevated BP detected.
              </span>
            </div>
            <button
              onClick={() => setIsSafetyOpen(true)}
              className="px-2.5 py-1 bg-amber-500/20 hover:bg-amber-500/30 text-amber-200 border border-amber-500/40 rounded-lg font-medium transition-colors"
            >
              Review Flags
            </button>
          </div>
        )}

        {/* Tab Content: Ambient Scribe */}
        {activeTab === 'scribe' && (
          <>
            {/* Patient Header Banner */}
            <PatientBanner
              patient={INITIAL_PATIENT}
              consultation={INITIAL_CONSULTATION}
            />

            {/* Ambient Microphone & Waveform Recorder Bar */}
            <AmbientRecorder
              isRecording={isRecording}
              onStartRecording={() => setIsRecording(true)}
              onStopRecording={() => setIsRecording(false)}
              onRunDemoPipeline={handleRunDemoPipeline}
              isProcessing={isProcessing}
              activeSegmentTime={activeAudioTime}
              onSeekAudio={(t) => setActiveAudioTime(t)}
            />

            {/* Two-Column Core Layout: Transcript Stream vs Clinical Note Editor */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left Column (5 cols): Multilingual Transcript Stream */}
              <div className="lg:col-span-5 h-[620px]">
                <TranscriptStream
                  segments={INITIAL_SEGMENTS}
                  highlightedSegmentId={selectedEvidenceId}
                  onSelectSegment={(segId, startTime) => {
                    setSelectedEvidenceId(segId);
                    setActiveAudioTime(startTime);
                    setIsEvidenceOpen(true);
                  }}
                />
              </div>

              {/* Right Column (7 cols): Structured Clinical Note Editor */}
              <div className="lg:col-span-7 h-[620px]">
                <ClinicalNoteEditor
                  noteContent={null}
                  isApproved={isApproved}
                  onApproveNote={() => setIsApproved(true)}
                  onSelectEvidence={handleSelectEvidence}
                  onViewPatientSummary={() => setIsPatientSummaryOpen(true)}
                  specialty={selectedSpecialty}
                />
              </div>
            </div>
          </>
        )}

        {/* Tab Content: Patient Timeline */}
        {activeTab === 'timeline' && (
          <PatientTimeline />
        )}

        {/* Tab Content: Evaluation Dashboard */}
        {activeTab === 'evaluation' && (
          <EvaluationDashboard />
        )}

        {/* Tab Content: Privacy Center */}
        {activeTab === 'privacy' && (
          <div className="glass-panel rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-lg font-bold text-white">DPDP & Security Settings</h2>
                <p className="text-xs text-slate-400">Configure compliance controls directly</p>
              </div>
              <button
                onClick={() => setIsPrivacyOpen(true)}
                className="px-3 py-1.5 bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold rounded-lg text-xs"
              >
                Open Full Audit Logs
              </button>
            </div>
            <p className="text-xs text-slate-300">
              ClinScribe AI is built with security-first architecture adhering to Indian Digital Personal Data Protection Act 2023 and ABDM NRCES specifications.
            </p>
          </div>
        )}
      </main>

      {/* Flyout Evidence Drawer */}
      <EvidenceDrawer
        isOpen={isEvidenceOpen}
        onClose={() => setIsEvidenceOpen(false)}
        selectedEvidenceId={selectedEvidenceId}
        onPlayAudioSnippet={handlePlaySnippet}
      />

      {/* Modals */}
      <SafetyAlertsModal
        isOpen={isSafetyOpen}
        onClose={() => setIsSafetyOpen(false)}
        flags={safetyFlags}
        onAcknowledgeFlag={(id) => {
          setSafetyFlags(safetyFlags.filter((f) => f.id !== id));
        }}
      />

      <PatientSummaryView
        isOpen={isPatientSummaryOpen}
        onClose={() => setIsPatientSummaryOpen(false)}
      />

      <FHIRExportModal
        isOpen={isFHIROpen}
        onClose={() => setIsFHIROpen(false)}
        fhirBundle={DEMO_FHIR_BUNDLE}
      />

      <PrivacyCenterModal
        isOpen={isPrivacyOpen}
        onClose={() => setIsPrivacyOpen(false)}
      />

      {/* Footer Legal & Clinical Safety Disclaimer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-4 px-4 sm:px-6 lg:px-8 mt-auto text-center">
        <p className="text-[11px] text-slate-400 flex items-center justify-center gap-1.5 flex-wrap">
          <span>⚕️ ClinScribe AI Prototype Demonstration (HC-02).</span>
          <span className="text-slate-500">•</span>
          <span>Synthetic patient data for demonstration purposes only.</span>
          <span className="text-slate-500">•</span>
          <span className="text-teal-400 font-medium">The treating doctor remains the final decision-maker.</span>
        </p>
      </footer>
    </div>
  );
}
