'use client';

import React, { useState, useEffect } from 'react';
import { 
  Mic, 
  MicOff, 
  Play, 
  Pause, 
  Square, 
  Sparkles, 
  Volume2, 
  Radio, 
  Sliders, 
  FastForward,
  RotateCcw
} from 'lucide-react';

interface AmbientRecorderProps {
  isRecording: boolean;
  onStartRecording: () => void;
  onStopRecording: () => void;
  onRunDemoPipeline: () => void;
  isProcessing: boolean;
  activeSegmentTime?: number;
  onSeekAudio?: (seconds: number) => void;
}

export const AmbientRecorder: React.FC<AmbientRecorderProps> = ({
  isRecording,
  onStartRecording,
  onStopRecording,
  onRunDemoPipeline,
  isProcessing,
  activeSegmentTime = 0,
  onSeekAudio,
}) => {
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [currentTime, setCurrentTime] = useState<number>(0);
  const duration = 165; // 2 min 45 sec synthetic consultation
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1);
  const [noiseFilterEnabled, setNoiseFilterEnabled] = useState<boolean>(true);

  // Sync seek audio time from parent
  useEffect(() => {
    if (activeSegmentTime && activeSegmentTime > 0) {
      setCurrentTime(activeSegmentTime);
      setIsPlaying(true);
    }
  }, [activeSegmentTime]);

  // Audio timer simulation
  useEffect(() => {
    let interval: any;
    if (isPlaying) {
      interval = setInterval(() => {
        setCurrentTime((prev) => {
          if (prev >= duration) {
            setIsPlaying(false);
            return 0;
          }
          return prev + 1;
        });
      }, 1000 / playbackSpeed);
    }
    return () => clearInterval(interval);
  }, [isPlaying, playbackSpeed, duration]);

  const formatTime = (secs: number) => {
    const mins = Math.floor(secs / 60);
    const remainder = Math.floor(secs % 60);
    return `${mins.toString().padStart(2, '0')}:${remainder.toString().padStart(2, '0')}`;
  };

  const handleScrubberChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = Number(e.target.value);
    setCurrentTime(val);
    if (onSeekAudio) onSeekAudio(val);
  };

  return (
    <div className="glass-panel rounded-xl p-4 sm:p-5 border border-slate-800 mb-6">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        {/* Left: Recording Status & Waveform */}
        <div className="flex items-center gap-4">
          <div className="relative">
            <button
              onClick={isRecording ? onStopRecording : onStartRecording}
              className={`h-14 w-14 rounded-2xl flex items-center justify-center transition-all shadow-lg ${
                isRecording
                  ? 'bg-rose-500 text-white shadow-rose-500/30 animate-pulse'
                  : 'bg-gradient-to-tr from-teal-500 to-cyan-400 text-slate-950 hover:brightness-110 shadow-teal-500/20'
              }`}
              title={isRecording ? 'Stop Recording' : 'Start Ambient Recording'}
            >
              {isRecording ? <Square className="h-6 w-6 fill-white" /> : <Mic className="h-6 w-6" />}
            </button>
            {isRecording && (
              <span className="absolute -top-1 -right-1 flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-rose-500"></span>
              </span>
            )}
          </div>

          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-white">
                {isRecording ? 'Ambient Listening Active' : 'OPD Ambient Microphone'}
              </span>
              <span className="px-2 py-0.5 text-[10px] font-medium bg-slate-800 text-teal-300 rounded border border-slate-700">
                AI4Bharat Conformer
              </span>
            </div>

            {/* Audio Waveform Animation */}
            <div className="flex items-center gap-1 mt-2 h-6">
              {isRecording ? (
                <>
                  <div className="w-1 bg-teal-400 rounded-full animate-wave-1"></div>
                  <div className="w-1 bg-teal-300 rounded-full animate-wave-2"></div>
                  <div className="w-1 bg-cyan-400 rounded-full animate-wave-3"></div>
                  <div className="w-1 bg-teal-400 rounded-full animate-wave-4"></div>
                  <div className="w-1 bg-cyan-300 rounded-full animate-wave-5"></div>
                  <div className="w-1 bg-teal-400 rounded-full animate-wave-2"></div>
                  <div className="w-1 bg-cyan-400 rounded-full animate-wave-1"></div>
                  <span className="text-xs text-rose-400 font-mono font-medium ml-2 flex items-center gap-1">
                    <Radio className="h-3 w-3 animate-spin" /> REC {formatTime(currentTime)}
                  </span>
                </>
              ) : (
                <div className="flex items-center gap-2 text-xs text-slate-400">
                  <div className="flex items-center gap-0.5 opacity-40">
                    <div className="w-1 h-2 bg-slate-500 rounded-full"></div>
                    <div className="w-1 h-3 bg-slate-500 rounded-full"></div>
                    <div className="w-1 h-1.5 bg-slate-500 rounded-full"></div>
                    <div className="w-1 h-4 bg-slate-500 rounded-full"></div>
                    <div className="w-1 h-2 bg-slate-500 rounded-full"></div>
                  </div>
                  <span>Ready to capture multilingual consultation</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Center: Audio Playback Scrubber */}
        <div className="flex-1 max-w-md px-2 lg:px-4">
          <div className="flex items-center justify-between text-[11px] text-slate-400 mb-1">
            <span className="font-mono text-teal-300">{formatTime(currentTime)}</span>
            <span className="font-mono">{formatTime(duration)}</span>
          </div>
          <input
            type="range"
            min={0}
            max={duration}
            value={currentTime}
            onChange={handleScrubberChange}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-teal-400"
          />
          <div className="flex items-center justify-between mt-1.5">
            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="p-1 rounded hover:bg-slate-800 text-slate-300 hover:text-white transition-colors"
                title={isPlaying ? "Pause playback" : "Play consultation audio"}
              >
                {isPlaying ? <Pause className="h-3.5 w-3.5 text-teal-400" /> : <Play className="h-3.5 w-3.5" />}
              </button>
              <button
                onClick={() => { setCurrentTime(0); setIsPlaying(false); }}
                className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
                title="Restart audio"
              >
                <RotateCcw className="h-3 w-3" />
              </button>
              <span className="text-[10px] text-slate-400 font-mono">16kHz IndicConformer</span>
            </div>

            <div className="flex items-center gap-2 text-[10px]">
              <button
                onClick={() => setNoiseFilterEnabled(!noiseFilterEnabled)}
                className={`px-1.5 py-0.5 rounded border transition-colors ${
                  noiseFilterEnabled
                    ? 'bg-teal-500/10 border-teal-500/30 text-teal-300'
                    : 'bg-slate-800 border-slate-700 text-slate-400'
                }`}
                title="Simulates ceiling fan & OPD corridor noise filtering"
              >
                Noise Filter: {noiseFilterEnabled ? 'ON' : 'OFF'}
              </button>
              <button
                onClick={() => setPlaybackSpeed(playbackSpeed === 1 ? 1.5 : 1)}
                className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300 hover:text-white"
              >
                {playbackSpeed}x
              </button>
            </div>
          </div>
        </div>

        {/* Right: Demo Simulation & Processing Action */}
        <div className="flex items-center gap-2.5">
          <button
            onClick={onRunDemoPipeline}
            disabled={isProcessing}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition-all shadow-lg ${
              isProcessing
                ? 'bg-slate-800 text-slate-400 cursor-not-allowed border border-slate-700'
                : 'bg-gradient-to-r from-teal-500 via-teal-400 to-cyan-400 text-slate-950 hover:brightness-110 shadow-teal-500/20 active:scale-95'
            }`}
          >
            <Sparkles className={`h-4 w-4 ${isProcessing ? 'animate-spin' : ''}`} />
            <span>{isProcessing ? 'Processing AI Pipeline...' : 'Run Ambient OPD Demo'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
export default AmbientRecorder;
