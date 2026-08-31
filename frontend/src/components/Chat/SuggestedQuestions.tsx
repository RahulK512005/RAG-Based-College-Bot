import React from 'react';
import { HelpCircle, DollarSign, Calendar, Home, Briefcase, Award } from 'lucide-react';

interface SuggestedQuestionsProps {
  onSelect: (question: string) => void;
}

const SUGGESTIONS = [
  {
    icon: HelpCircle,
    color: 'from-blue-500/20 to-cyan-500/20 text-cyan-400 border-cyan-500/30',
    title: 'Admissions Criteria',
    prompt: 'What are the eligibility criteria and cutoffs for B.Tech admissions 2026?'
  },
  {
    icon: DollarSign,
    color: 'from-emerald-500/20 to-teal-500/20 text-emerald-400 border-emerald-500/30',
    title: 'CSE Fee Structure',
    prompt: 'What is the annual tuition fee for B.Tech in Computer Science and Engineering (CSE)?'
  },
  {
    icon: Calendar,
    color: 'from-amber-500/20 to-orange-500/20 text-amber-400 border-amber-500/30',
    title: 'Semester Exams & Attendance',
    prompt: 'What is the minimum attendance percentage required to sit for semester examinations?'
  },
  {
    icon: Home,
    color: 'from-purple-500/20 to-indigo-500/20 text-purple-400 border-purple-500/30',
    title: 'Hostel Curfew & Fees',
    prompt: 'What are the hostel room options, annual fees, and gate curfew timings?'
  },
  {
    icon: Briefcase,
    color: 'from-rose-500/20 to-pink-500/20 text-rose-400 border-rose-500/30',
    title: 'Placement Statistics',
    prompt: 'What was the highest international package offered and top recruiting companies?'
  },
  {
    icon: Award,
    color: 'from-yellow-500/20 to-amber-500/20 text-yellow-400 border-yellow-500/30',
    title: 'Scholarship Schemes',
    prompt: 'Who is eligible for the 100% tuition fee waiver scholarship and Pragati fellowship?'
  }
];

export const SuggestedQuestions: React.FC<SuggestedQuestionsProps> = ({ onSelect }) => {
  return (
    <div className="w-full max-w-3xl mx-auto my-6 px-4">
      <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 text-center sm:text-left">
        Suggested Inquiries
      </h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {SUGGESTIONS.map((item, i) => {
          const Icon = item.icon;
          return (
            <button
              key={i}
              onClick={() => onSelect(item.prompt)}
              className="group p-3.5 rounded-xl glass-card text-left flex flex-col justify-between hover:scale-[1.02] active:scale-[0.98] transition-all duration-150"
            >
              <div className="flex items-center gap-2.5 mb-2">
                <div className={`p-2 rounded-lg bg-gradient-to-br ${item.color} border`}>
                  <Icon className="w-4 h-4" />
                </div>
                <span className="text-xs font-bold text-slate-200 group-hover:text-white transition-colors">
                  {item.title}
                </span>
              </div>
              <p className="text-xs text-slate-400 group-hover:text-slate-300 transition-colors line-clamp-2">
                {item.prompt}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
};
