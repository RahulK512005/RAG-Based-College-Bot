import React from 'react';
import { DashboardStats } from '../../types';
import { FileText, CheckCircle2, Clock, AlertTriangle, Layers, MessageSquare } from 'lucide-react';

interface StatsGridProps {
  stats: DashboardStats | null;
  isLoading: boolean;
}

export const StatsGrid: React.FC<StatsGridProps> = ({ stats, isLoading }) => {
  const cards = [
    {
      title: 'Total Documents',
      value: stats?.total_documents ?? 0,
      icon: FileText,
      color: 'from-blue-500/20 to-cyan-500/20 text-cyan-400 border-cyan-500/30'
    },
    {
      title: 'Ready / Indexed',
      value: stats?.ready_documents ?? 0,
      icon: CheckCircle2,
      color: 'from-emerald-500/20 to-teal-500/20 text-emerald-400 border-emerald-500/30'
    },
    {
      title: 'Processing',
      value: stats?.processing_documents ?? 0,
      icon: Clock,
      color: 'from-amber-500/20 to-yellow-500/20 text-amber-400 border-amber-500/30'
    },
    {
      title: 'Failed',
      value: stats?.failed_documents ?? 0,
      icon: AlertTriangle,
      color: 'from-rose-500/20 to-red-500/20 text-rose-400 border-rose-500/30'
    },
    {
      title: 'Vector Chunks',
      value: stats?.total_chunks ?? 0,
      icon: Layers,
      color: 'from-purple-500/20 to-indigo-500/20 text-purple-400 border-purple-500/30'
    },
    {
      title: 'Total Questions',
      value: stats?.total_questions ?? 0,
      icon: MessageSquare,
      color: 'from-pink-500/20 to-rose-500/20 text-pink-400 border-pink-500/30'
    }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5 mb-8">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className="p-4 rounded-2xl glass-card border flex flex-col justify-between"
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-medium text-slate-400">{card.title}</span>
              <div className={`p-1.5 rounded-lg bg-gradient-to-br ${card.color} border`}>
                <Icon className="w-3.5 h-3.5" />
              </div>
            </div>
            <div className="text-2xl font-black text-white font-mono">
              {isLoading ? (
                <div className="h-7 w-12 bg-slate-800 rounded animate-pulse" />
              ) : (
                card.value
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
