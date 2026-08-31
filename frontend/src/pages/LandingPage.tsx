import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Search,
  Layers,
  FileText,
  Database,
  Cpu
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  const { isAuthenticated } = useAuth();

  const features = [
    {
      icon: Search,
      color: 'from-blue-500/20 to-cyan-500/20 text-cyan-400 border-cyan-500/30',
      title: 'Real Vector Retrieval',
      desc: 'Performs cosine similarity searches across thousands of indexed college document chunks.'
    },
    {
      icon: ShieldCheck,
      color: 'from-emerald-500/20 to-teal-500/20 text-emerald-400 border-emerald-500/30',
      title: 'Zero-Hallucination Guarantee',
      desc: 'Strictly refuses to invent dates, fees, or policies when information is not in the knowledge base.'
    },
    {
      icon: FileText,
      color: 'from-purple-500/20 to-indigo-500/20 text-purple-400 border-purple-500/30',
      title: 'Clickable Source Citations',
      desc: 'Every single answer explicitly cites the exact document title, page number, and source excerpt.'
    },
    {
      icon: Layers,
      color: 'from-amber-500/20 to-orange-500/20 text-amber-400 border-amber-500/30',
      title: 'Multi-Format Ingestion',
      desc: 'Extracts, normalizes, and chunks PDFs, Word documents, and text files in background pipelines.'
    },
    {
      icon: Database,
      color: 'from-pink-500/20 to-rose-500/20 text-pink-400 border-pink-500/30',
      title: 'Supabase pgvector',
      desc: 'Full-stack persistence with PostgreSQL, pgvector cosine indexes, and cascading document cleanup.'
    },
    {
      icon: Cpu,
      color: 'from-yellow-500/20 to-amber-500/20 text-yellow-400 border-yellow-500/30',
      title: 'Role-Based Control',
      desc: 'Secure student querying with dedicated administrator consoles for document uploads and audits.'
    }
  ];

  return (
    <div className="min-h-[calc(100vh-65px)] flex flex-col justify-between">
      <section className="relative px-4 sm:px-6 lg:px-8 pt-16 pb-20 max-w-7xl mx-auto text-center flex flex-col items-center">
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold mb-6 shadow-sm">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Production Retrieval-Augmented Generation (RAG) Architecture</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white max-w-4xl leading-[1.15]">
          Verified College Knowledge, Grounded by{' '}
          <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
            AI & Vector Search
          </span>
        </h1>

        <p className="mt-6 text-base sm:text-lg text-slate-400 max-w-2xl leading-relaxed">
          Ask questions about admissions, fees, academic calendars, hostel curfews, and placements.
          Answers are strictly retrieved and verified against official institution documents.
        </p>

        <div className="mt-8 flex flex-col sm:flex-row items-center gap-3.5">
          {isAuthenticated ? (
            <Link
              to="/chat"
              className="flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-xl shadow-emerald-500/20 transition-all hover:scale-105"
            >
              Open AI Chat Assistant
              <ArrowRight className="w-4 h-4" />
            </Link>
          ) : (
            <>
              <Link
                to="/signup"
                className="flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-xl shadow-emerald-500/20 transition-all hover:scale-105"
              >
                Create Student Account
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/login"
                className="px-6 py-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 font-semibold text-sm transition-all"
              >
                Sign In (Demo Accounts)
              </Link>
            </>
          )}
        </div>

        <div className="mt-16 w-full max-w-5xl p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 shadow-2xl">
          <div className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-6">
            End-to-End RAG Verification Pipeline
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2 items-center text-xs">
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex flex-col items-center">
              <span className="text-emerald-400 font-bold">1. Query</span>
              <span className="text-slate-400 text-[10px] mt-0.5">Student Input</span>
            </div>
            <div className="hidden lg:block text-slate-600 font-mono text-center">→</div>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex flex-col items-center">
              <span className="text-cyan-400 font-bold">2. Embed</span>
              <span className="text-slate-400 text-[10px] mt-0.5">Dense Vectors</span>
            </div>
            <div className="hidden lg:block text-slate-600 font-mono text-center">→</div>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex flex-col items-center">
              <span className="text-purple-400 font-bold">3. Vector Search</span>
              <span className="text-slate-400 text-[10px] mt-0.5">Cosine Similarity</span>
            </div>
            <div className="hidden lg:block text-slate-600 font-mono text-center">→</div>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex flex-col items-center">
              <span className="text-amber-400 font-bold">4. Filter</span>
              <span className="text-slate-400 text-[10px] mt-0.5">Threshold Check</span>
            </div>
            <div className="hidden lg:block text-slate-600 font-mono text-center">→</div>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex flex-col items-center">
              <span className="text-pink-400 font-bold">5. Context</span>
              <span className="text-slate-400 text-[10px] mt-0.5">Top-K Chunks</span>
            </div>
            <div className="hidden lg:block text-slate-600 font-mono text-center">→</div>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex flex-col items-center">
              <span className="text-teal-400 font-bold">6. Grounded LLM</span>
              <span className="text-slate-400 text-[10px] mt-0.5">Zero Hallucination</span>
            </div>
            <div className="hidden lg:block text-slate-600 font-mono text-center">→</div>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex flex-col items-center">
              <span className="text-emerald-400 font-bold">7. Answer</span>
              <span className="text-slate-400 text-[10px] mt-0.5">With Sources</span>
            </div>
          </div>
        </div>
      </section>

      <section className="px-4 sm:px-6 lg:px-8 py-16 max-w-7xl mx-auto w-full">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h2 className="text-2xl sm:text-3xl font-bold text-white">Engineered for Academic Accuracy</h2>
          <p className="text-sm text-slate-400 mt-2">
            No generic mockups or hallucinated answers. Full transparency from document chunk to response.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {features.map((feat, i) => {
            const Icon = feat.icon;
            return (
              <div key={i} className="p-6 rounded-2xl glass-card border flex flex-col">
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${feat.color} border flex items-center justify-center mb-4`}>
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-white mb-2">{feat.title}</h3>
                <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">{feat.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      <footer className="border-t border-slate-800/80 py-8 px-4 text-center text-xs text-slate-500">
        <p>© 2026 College RAG AI Assistant. Built with FastAPI, pgvector, and React.</p>
      </footer>
    </div>
  );
};
