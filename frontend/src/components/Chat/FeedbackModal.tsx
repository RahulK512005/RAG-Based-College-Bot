import React, { useState } from 'react';
import { api } from '../../services/api';
import { ThumbsUp, ThumbsDown, X, Check, MessageSquare } from 'lucide-react';

interface FeedbackModalProps {
  messageId: string;
  initialRating: number; // 1 or -1
  isOpen: boolean;
  onClose: () => void;
  onFeedbackSaved: (rating: number, comment?: string) => void;
}

export const FeedbackModal: React.FC<FeedbackModalProps> = ({
  messageId,
  initialRating,
  isOpen,
  onClose,
  onFeedbackSaved
}) => {
  const [rating, setRating] = useState<number>(initialRating);
  const [comment, setComment] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isSuccess, setIsSuccess] = useState<boolean>(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await api.post(`/messages/${messageId}/feedback`, {
        rating,
        comment: comment.trim() || undefined
      });
      setIsSuccess(true);
      onFeedbackSaved(rating, comment.trim() || undefined);
      setTimeout(() => {
        setIsSuccess(false);
        onClose();
      }, 1200);
    } catch (err) {
      console.error('Failed to submit feedback:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-150">
      <div className="relative w-full max-w-md rounded-2xl glass-panel border border-slate-700 bg-slate-900/95 p-6 shadow-2xl">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
              <MessageSquare className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white">Provide Answer Feedback</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {isSuccess ? (
          <div className="py-8 flex flex-col items-center justify-center text-center">
            <div className="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mb-3">
              <Check className="w-6 h-6 stroke-[3]" />
            </div>
            <p className="text-base font-bold text-white">Thank You for Your Feedback!</p>
            <p className="text-xs text-slate-400 mt-1">Your rating helps us improve RAG retrieval accuracy.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="mt-4 space-y-4">
            <div>
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-2">
                Was this answer grounded and helpful?
              </label>
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => setRating(1)}
                  className={`flex-1 py-2.5 px-3 rounded-xl border flex items-center justify-center gap-2 font-medium text-sm transition-all ${
                    rating === 1
                      ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50 shadow-md shadow-emerald-500/10'
                      : 'bg-slate-800/60 text-slate-400 border-slate-700 hover:text-slate-200'
                  }`}
                >
                  <ThumbsUp className="w-4 h-4" />
                  Helpful & Accurate
                </button>
                <button
                  type="button"
                  onClick={() => setRating(-1)}
                  className={`flex-1 py-2.5 px-3 rounded-xl border flex items-center justify-center gap-2 font-medium text-sm transition-all ${
                    rating === -1
                      ? 'bg-rose-500/20 text-rose-300 border-rose-500/50 shadow-md shadow-rose-500/10'
                      : 'bg-slate-800/60 text-slate-400 border-slate-700 hover:text-slate-200'
                  }`}
                >
                  <ThumbsDown className="w-4 h-4" />
                  Not Grounded
                </button>
              </div>
            </div>

            <div>
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-2">
                Optional comments or suggestions
              </label>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Mention any missing details or inaccuracies..."
                rows={3}
                className="w-full px-3 py-2 bg-slate-950/80 border border-slate-800 rounded-xl text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 resize-none"
              />
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-5 py-2 text-sm font-semibold bg-emerald-500 hover:bg-emerald-400 text-slate-950 rounded-lg shadow-md shadow-emerald-500/20 disabled:opacity-50 transition-all"
              >
                {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
