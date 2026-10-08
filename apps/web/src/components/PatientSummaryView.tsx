'use client';

import React, { useState } from 'react';
import { 
  X, 
  Languages, 
  Printer, 
  Share2, 
  CheckCircle2, 
  AlertTriangle,
  Clock,
  Pill,
  Heart
} from 'lucide-react';

interface PatientSummaryViewProps {
  isOpen: boolean;
  onClose: () => void;
}

export const PatientSummaryView: React.FC<PatientSummaryViewProps> = ({
  isOpen,
  onClose,
}) => {
  const [selectedLang, setSelectedLang] = useState<'kn' | 'hi' | 'en'>('kn');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-2xl bg-slate-950 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 bg-slate-900/60 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-teal-500/10 text-teal-400 rounded-xl border border-teal-500/30">
              <Languages className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">
                Multilingual Patient Summary Leaflet
              </h3>
              <p className="text-xs text-slate-400">
                Patient-friendly discharge instructions in primary regional language
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

        {/* Language Tabs */}
        <div className="px-5 py-3 border-b border-slate-800/80 bg-slate-900/40 flex items-center justify-between">
          <div className="flex bg-slate-900 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setSelectedLang('kn')}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                selectedLang === 'kn'
                  ? 'bg-teal-500 text-slate-950 shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              ಕನ್ನಡ (Kannada)
            </button>
            <button
              onClick={() => setSelectedLang('hi')}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                selectedLang === 'hi'
                  ? 'bg-teal-500 text-slate-950 shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              हिंदी (Hindi)
            </button>
            <button
              onClick={() => setSelectedLang('en')}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                selectedLang === 'en'
                  ? 'bg-teal-500 text-slate-950 shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              English
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => window.print()}
              className="p-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 rounded-lg border border-slate-800 text-xs flex items-center gap-1.5 transition-colors"
            >
              <Printer className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">Print OPD Leaflet</span>
            </button>
          </div>
        </div>

        {/* Leaflet Content */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4 text-xs leading-relaxed">
          {selectedLang === 'kn' && (
            <div className="space-y-4 font-sans text-slate-200">
              <div className="p-4 bg-teal-950/20 rounded-xl border border-teal-500/30">
                <h4 className="font-bold text-teal-300 text-sm mb-1">
                  ಆರೋಗ್ಯ ಸಾರಾಂಶ — ರಾಹುಲ್ ಕುಮಾರ್ (Rahul Kumar)
                </h4>
                <p className="text-slate-300">
                  ನಿಮಗೆ ಸಾಮಾನ್ಯ ಶೀತ ಮತ್ತು ಜ್ವರ (Viral Fever & Cold) ಕಂಡುಬಂದಿದೆ. ಆತಂಕಪಡುವ ಅಗತ್ಯವಿಲ್ಲ, ಕೆಳಗಿನ ಸೂಚನೆಗಳನ್ನು ಪಾಲಿಸಿ.
                </p>
              </div>

              <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800">
                <h5 className="font-bold text-white text-xs mb-2 flex items-center gap-1.5">
                  <Pill className="h-4 w-4 text-teal-400" />
                  ಔಷಧಿಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳುವ ಕ್ರಮ:
                </h5>
                <ul className="space-y-2 list-disc list-inside text-slate-300">
                  <li><strong>ಪ್ಯಾರಾಸಿಟಮಾಲ್ 500mg (Paracetamol):</strong> ದಿನಕ್ಕೆ 3 ಬಾರಿ ಊಟದ ನಂತರ (ಜ್ವರವಿದ್ದರೆ ಮಾತ್ರ). 3 ದಿನಗಳ ಕಾಲ.</li>
                  <li><strong>ಕೆಮ್ಮಿನ ಸಿರಪ್ (Cough Syrup):</strong> 5ml ದಿನಕ್ಕೆ 2 ಬಾರಿ (ಬೆಳಿಗ್ಗೆ ಮತ್ತು ರಾತ್ರಿ).</li>
                  <li><strong>ಬಿಪಿ ಮಾತ್ರೆ (Amlodipine 5mg):</strong> ನಿಮ್ಮ ಹಳೆಯ ಬಿಪಿ ಮಾತ್ರೆ ತಪ್ಪದೇ ಪ್ರತಿದಿನ ಬೆಳಿಗ್ಗೆ ಮುಂದುವರಿಸಿ.</li>
                </ul>
              </div>

              <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800">
                <h5 className="font-bold text-white text-xs mb-2 flex items-center gap-1.5">
                  <Heart className="h-4 w-4 text-sky-400" />
                  ಆಹಾರ ಮತ್ತು ವಿಶ್ರಾಂತಿ:
                </h5>
                <p className="text-slate-300">
                  ಬಿಸಿ ನೀರು ಅಥವಾ ಗಂಜಿ ಸೇವಿಸಿ. ದಿನಕ್ಕೆ ಕನಿಷ್ಠ 8-10 ಲೋಟ ನೀರು ಕುಡಿಯಿರಿ. ಸಾಕಷ್ಟು ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ ಮತ್ತು ಬಿಸಿ ನೀರಿನ ಹಬೆ ತೆಗೆದುಕೊಳ್ಳಿ.
                </p>
              </div>

              <div className="p-4 bg-rose-950/20 rounded-xl border border-rose-500/30">
                <h5 className="font-bold text-rose-300 text-xs mb-1 flex items-center gap-1.5">
                  <AlertTriangle className="h-4 w-4 text-rose-400" />
                  ತಕ್ಷಣ ಆಸ್ಪತ್ರೆಗೆ ಯಾವಾಗ ಬರಬೇಕು?
                </h5>
                <p className="text-rose-200">
                  ಉಸಿರಾಟದಲ್ಲಿ ತೊಂದರೆ ಕಂಡುಬಂದರೆ, ಎದೆ ನೋವು ಬಂದರೆ, ಅಥವಾ ಜ್ವರ 102°F ಗಿಂತ ಹೆಚ್ಚಾದರೆ ತಕ್ಷಣ ಹತ್ತಿರದ ಆಸ್ಪತ್ರೆಗೆ ಬನ್ನಿ.
                </p>
              </div>
            </div>
          )}

          {selectedLang === 'hi' && (
            <div className="space-y-4 font-sans text-slate-200">
              <div className="p-4 bg-teal-950/20 rounded-xl border border-teal-500/30">
                <h4 className="font-bold text-teal-300 text-sm mb-1">
                  स्वास्थ्य परामर्श पर्ची — राहुल कुमार (Rahul Kumar)
                </h4>
                <p className="text-slate-300">
                  आपको मौसमी वायरल बुखार और सर्दी-खांसी है। घबराने की कोई बात नहीं है, नीचे दी गई सलाह का पालन करें।
                </p>
              </div>

              <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800">
                <h5 className="font-bold text-white text-xs mb-2 flex items-center gap-1.5">
                  <Pill className="h-4 w-4 text-teal-400" />
                  दवाइयाँ लेने का नियम:
                </h5>
                <ul className="space-y-2 list-disc list-inside text-slate-300">
                  <li><strong>पैरासिटामोल 500mg:</strong> दिन में 3 बार खाना खाने के बाद (3 दिन तक)।</li>
                  <li><strong>खांसी का सिरप:</strong> 5ml दिन में 2 बार (सुबह और रात)।</li>
                  <li><strong>बीपी की दवा (Amlodipine 5mg):</strong> रोज़ सुबह जैसे लेते हैं, नियमित लेते रहें।</li>
                </ul>
              </div>

              <div className="p-4 bg-rose-950/20 rounded-xl border border-rose-500/30">
                <h5 className="font-bold text-rose-300 text-xs mb-1 flex items-center gap-1.5">
                  <AlertTriangle className="h-4 w-4 text-rose-400" />
                  आपातकालीन चेतावनी:
                </h5>
                <p className="text-rose-200">
                  यदि सांस लेने में तकलीफ़ हो, सीने में दर्द हो, या बुखार 102°F से अधिक हो जाए, तो तुरंत ओपीडी या आपातकालीन कक्ष में संपर्क करें।
                </p>
              </div>
            </div>
          )}

          {selectedLang === 'en' && (
            <div className="space-y-4 font-sans text-slate-200">
              <div className="p-4 bg-teal-950/20 rounded-xl border border-teal-500/30">
                <h4 className="font-bold text-teal-300 text-sm mb-1">
                  Discharge Summary — Rahul Kumar (MRN-2026-0001)
                </h4>
                <p className="text-slate-300">
                  Diagnosis: Acute viral febrile illness with mild upper respiratory tract infection.
                </p>
              </div>

              <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800">
                <h5 className="font-bold text-white text-xs mb-2 flex items-center gap-1.5">
                  <Pill className="h-4 w-4 text-teal-400" />
                  Prescribed Medication Instructions:
                </h5>
                <ul className="space-y-2 list-disc list-inside text-slate-300">
                  <li><strong>Tab. Paracetamol 500mg:</strong> 1 tablet three times daily after food for 3 days.</li>
                  <li><strong>Cough Syrup:</strong> 5ml twice daily for 5 days.</li>
                  <li><strong>Tab. Amlodipine 5mg:</strong> Continue your regular blood pressure medication every morning.</li>
                </ul>
              </div>

              <div className="p-4 bg-rose-950/20 rounded-xl border border-rose-500/30">
                <h5 className="font-bold text-rose-300 text-xs mb-1 flex items-center gap-1.5">
                  <AlertTriangle className="h-4 w-4 text-rose-400" />
                  Emergency Red Flags:
                </h5>
                <p className="text-rose-200">
                  Seek immediate emergency care if you experience shortness of breath, chest pressure, persistent vomiting, or fever exceeding 102°F.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-900/60 flex items-center justify-between">
          <span className="text-[11px] text-slate-400">
            Compliant with ABDM patient digital record access standards.
          </span>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-bold transition-colors"
          >
            Close Leaflet
          </button>
        </div>
      </div>
    </div>
  );
};
export default PatientSummaryView;
