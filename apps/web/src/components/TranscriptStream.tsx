'use client';

import React, { useState } from 'react';
import { 
  Languages, 
  Play, 
  CheckCircle, 
  Volume2, 
  Sparkles, 
  HelpCircle,
  Clock,
  ArrowRight
} from 'lucide-react';

export interface TranscriptSegment {
  id: string;
  segment_index: number;
  speaker: string;
  start_time: number;
  end_time: number;
  original_text: string;
  english_translation: string;
  language: string;
  confidence: number;
}

interface TranscriptStreamProps {
  segments: TranscriptSegment[];
  highlightedSegmentId?: string | null;
  onSelectSegment?: (segmentId: string, startTime: number) => void;
}

export const TranscriptStream: React.FC<TranscriptStreamProps> = ({
  segments,
  highlightedSegmentId,
  onSelectSegment,
}) => {
  const [showEnglishOnly, setShowEnglishOnly] = useState<boolean>(false);

  const formatSeconds = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="flex flex-col h-full glass-panel rounded-xl border border-slate-800 overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-slate-800/80 bg-slate-900/60 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Languages className="h-4 w-4 text-teal-400" />
          <h2 className="text-sm font-bold text-white tracking-wide">
            Multilingual Dialogue Stream
          </h2>
          <span className="px-2 py-0.5 text-[10px] bg-slate-800 text-slate-300 rounded font-mono">
            {segments.length} Turns
          </span>
        </div>

        {/* Translation Toggle */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowEnglishOnly(!showEnglishOnly)}
            className="text-[11px] px-2 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 transition-colors"
          >
            {showEnglishOnly ? 'Show Original Kannada/Mixed' : 'Show English Translation'}
          </button>
        </div>
      </div>

      {/* Segments List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 max-h-[600px]">
        {segments.map((seg) => {
          const isHighlighted = highlightedSegmentId === seg.id;
          const isDoctor = seg.speaker.toLowerCase().includes('doctor');

          return (
            <div
              key={seg.id}
              onClick={() => onSelectSegment && onSelectSegment(seg.id, seg.start_time)}
              className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                isHighlighted
                  ? 'bg-teal-500/15 border-teal-400 shadow-md shadow-teal-500/10 scale-[1.01]'
                  : isDoctor
                  ? 'bg-slate-900/70 border-slate-800 hover:border-slate-700'
                  : 'bg-slate-900/40 border-slate-800/60 hover:border-slate-700'
              }`}
            >
              {/* Speaker & Timestamp Bar */}
              <div className="flex items-center justify-between mb-1.5 text-xs">
                <div className="flex items-center gap-2">
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wide uppercase ${
                      isDoctor
                        ? 'bg-teal-500/20 text-teal-300 border border-teal-500/40'
                        : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/40'
                    }`}
                  >
                    {isDoctor ? 'Doctor (Dr. Priya)' : 'Patient (Rahul K)'}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400 flex items-center gap-1">
                    <Clock className="h-2.5 w-2.5" />
                    {formatSeconds(seg.start_time)} - {formatSeconds(seg.end_time)}
                  </span>
                </div>

                <div className="flex items-center gap-1.5 text-[10px] text-slate-400">
                  <span className="px-1.5 py-0.5 bg-slate-800 rounded font-mono text-[9px] text-slate-300">
                    {seg.language}
                  </span>
                  <span className="text-emerald-400 font-mono font-medium">
                    {Math.round(seg.confidence * 100)}%
                  </span>
                </div>
              </div>

              {/* Dialogue Text */}
              <div className="text-xs text-slate-200 leading-relaxed font-sans">
                {showEnglishOnly ? (
                  <p className="text-slate-100">{seg.english_translation}</p>
                ) : (
                  <>
                    <p className="font-medium text-slate-100">{seg.original_text}</p>
                    {seg.english_translation && seg.english_translation !== seg.original_text && (
                      <p className="text-[11px] text-slate-400 mt-1 italic flex items-center gap-1">
                        <ArrowRight className="h-2.5 w-2.5 text-teal-400 shrink-0" />
                        {seg.english_translation}
                      </p>
                    )}
                  </>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
export default TranscriptStream;
