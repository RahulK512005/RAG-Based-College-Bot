import React, { useState } from 'react';
import { SourceCitation } from '../../types';
import { FileText, ExternalLink, X, BookOpen, Tag, Percent } from 'lucide-react';

interface SourceCardProps {
  source: SourceCitation;
  index?: number;
}

export const SourceCard: React.FC<SourceCardProps> = ({ source }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="group flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/60 hover:border-emerald-500/40 text-left transition-all duration-150 shadow-sm"
      >
        <div className="w-5 h-5 rounded bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 group-hover:bg-emerald-500/20">
          <FileText className="w-3 h-3" />
        </div>
        <div className="flex flex-col">
          <span className="text-xs font-semibold text-slate-200 group-hover:text-emerald-300 transition-colors line-clamp-1 max-w-[170px]">
            {source.document_title}
          </span>
          <div className="flex items-center gap-1.5 text-[10px] text-slate-400">
            {source.page_number && <span>Page {source.page_number}</span>}
            <span>•</span>
            <span className="text-emerald-400/90 font-medium">
              {(source.similarity_score * 100).toFixed(0)}% match
            </span>
          </div>
        </div>
        <ExternalLink className="w-3 h-3 text-slate-500 group-hover:text-slate-300 ml-1" />
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-150">
          <div className="relative w-full max-w-lg rounded-2xl glass-panel border border-slate-700 bg-slate-900/95 p-6 shadow-2xl">
            <div className="flex items-start justify-between gap-4 pb-4 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                  <BookOpen className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white">{source.document_title}</h3>
                  <div className="flex items-center gap-2 mt-1 text-xs text-slate-400">
                    <span className="flex items-center gap-1">
                      <Tag className="w-3 h-3 text-emerald-400" />
                      {source.category}
                    </span>
                    {source.page_number && (
                      <>
                        <span>•</span>
                        <span>Page {source.page_number}</span>
                      </>
                    )}
                    <span>•</span>
                    <span className="text-emerald-400 font-medium flex items-center gap-0.5">
                      <Percent className="w-3 h-3" />
                      {(source.similarity_score * 100).toFixed(1)}% Relevance
                    </span>
                  </div>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="mt-4">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Retrieved Context Excerpt
              </label>
              <div className="mt-2 p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-sm text-slate-300 leading-relaxed font-mono whitespace-pre-wrap max-h-60 overflow-y-auto">
                {source.excerpt}
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setIsOpen(false)}
                className="px-4 py-2 text-sm font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors"
              >
                Close Preview
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
