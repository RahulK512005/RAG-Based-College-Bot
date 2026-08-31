import React, { useState, useRef } from 'react';
import { Send, Filter } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (question: string, categoryFilter?: string) => void;
  isLoading: boolean;
}

const CATEGORIES = [
  'All Categories',
  'Admissions',
  'Academics',
  'Fees',
  'Examinations',
  'Hostel',
  'Placements',
  'Scholarships',
  'Policies',
  'Events',
  'General'
];

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [question, setQuestion] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All Categories');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (!question.trim() || isLoading) return;
    const cat = selectedCategory === 'All Categories' ? undefined : selectedCategory;
    onSendMessage(question.trim(), cat);
    setQuestion('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setQuestion(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto px-4 pb-4">
      <div className="flex items-center gap-2 mb-2 px-1">
        <Filter className="w-3.5 h-3.5 text-slate-400" />
        <span className="text-xs text-slate-400">Filter Scope:</span>
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="bg-slate-900 border border-slate-800 text-xs text-emerald-400 rounded-lg px-2 py-1 focus:outline-none focus:border-emerald-500/50"
        >
          {CATEGORIES.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      <div className="relative flex items-end gap-2 p-2 rounded-2xl glass-panel border border-white/10 bg-slate-900/90 shadow-2xl focus-within:border-emerald-500/50 transition-all duration-200">
        <textarea
          ref={textareaRef}
          value={question}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about admissions, fees, syllabus, hostel, or placements..."
          disabled={isLoading}
          rows={1}
          className="w-full max-h-32 p-2.5 bg-transparent text-sm text-slate-100 placeholder-slate-500 focus:outline-none resize-none leading-relaxed"
        />

        <button
          onClick={handleSend}
          disabled={!question.trim() || isLoading}
          className="flex-shrink-0 p-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 disabled:bg-slate-800 text-slate-950 disabled:text-slate-600 shadow-md shadow-emerald-500/20 disabled:shadow-none transition-all duration-150 active:scale-95 flex items-center justify-center"
        >
          {isLoading ? (
            <div className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
          ) : (
            <Send className="w-4 h-4" />
          )}
        </button>
      </div>
      <p className="text-[11px] text-slate-500 text-center mt-2">
        College RAG AI answers using verified institution knowledge base context only.
      </p>
    </div>
  );
};
