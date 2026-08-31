import React, { useState } from 'react';
import { ChatMessage as ChatMessageType } from '../../types';
import { SourceCard } from './SourceCard';
import { FeedbackModal } from './FeedbackModal';
import { User, Sparkles, ThumbsUp, ThumbsDown, Clock, ShieldAlert } from 'lucide-react';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const [feedback, setFeedback] = useState(message.feedback);
  const [isFeedbackOpen, setIsFeedbackOpen] = useState(false);
  const [selectedRating, setSelectedRating] = useState<number>(1);

  const isUnknown = message.content.includes("couldn't find reliable information");

  const openFeedback = (rating: number) => {
    setSelectedRating(rating);
    setIsFeedbackOpen(true);
  };

  const handleFeedbackSaved = (rating: number, comment?: string) => {
    setFeedback({ id: 'local', rating, comment });
  };

  const formattedTime = new Date(message.created_at).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className={`flex w-full gap-3.5 my-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex-shrink-0 flex items-center justify-center text-slate-950 shadow-md shadow-emerald-500/20">
          <Sparkles className="w-4 h-4" />
        </div>
      )}

      <div
        className={`max-w-2xl rounded-2xl p-4 sm:p-5 shadow-lg ${
          isUser
            ? 'bg-emerald-600/90 text-white rounded-br-none'
            : isUnknown
            ? 'glass-panel border-amber-500/30 text-slate-100 rounded-bl-none'
            : 'glass-panel border-white/10 text-slate-100 rounded-bl-none'
        }`}
      >
        {!isUser && isUnknown && (
          <div className="flex items-center gap-2 mb-3 px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs font-semibold">
            <ShieldAlert className="w-4 h-4 flex-shrink-0" />
            <span>Zero-Hallucination Guard: Information not found in knowledge base</span>
          </div>
        )}

        <div className="text-sm sm:text-base leading-relaxed whitespace-pre-wrap font-sans">
          {message.content}
        </div>

        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-4 pt-3 border-t border-slate-700/60">
            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
              <span>Verified Sources ({message.sources.length})</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {message.sources.map((source, idx) => (
                <SourceCard key={idx} source={source} index={idx} />
              ))}
            </div>
          </div>
        )}

        <div className="mt-3 flex items-center justify-between gap-4 text-[11px] text-slate-400/80">
          <span className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            {formattedTime}
          </span>

          {!isUser && (
            <div className="flex items-center gap-1.5">
              {feedback ? (
                <span className="text-[10px] font-medium text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                  {feedback.rating === 1 ? '👍 Rated helpful' : '👎 Rated inaccurate'}
                </span>
              ) : (
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => openFeedback(1)}
                    title="Helpful response"
                    className="p-1 text-slate-400 hover:text-emerald-400 hover:bg-slate-800 rounded transition-colors"
                  >
                    <ThumbsUp className="w-3.5 h-3.5" />
                  </button>
                  <button
                    onClick={() => openFeedback(-1)}
                    title="Inaccurate response"
                    className="p-1 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded transition-colors"
                  >
                    <ThumbsDown className="w-3.5 h-3.5" />
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex-shrink-0 flex items-center justify-center text-slate-300">
          <User className="w-4 h-4" />
        </div>
      )}

      {!isUser && (
        <FeedbackModal
          messageId={message.id}
          initialRating={selectedRating}
          isOpen={isFeedbackOpen}
          onClose={() => setIsFeedbackOpen(false)}
          onFeedbackSaved={handleFeedbackSaved}
        />
      )}
    </div>
  );
};
