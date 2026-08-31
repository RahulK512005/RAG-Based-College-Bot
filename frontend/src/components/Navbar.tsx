import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { GraduationCap, MessageSquare, Shield, LogOut, Sparkles } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, isAdmin, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="glass-panel sticky top-0 z-50 px-4 lg:px-8 py-3.5 flex items-center justify-between border-b border-white/10">
      <Link to="/" className="flex items-center gap-3 group">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform duration-200">
          <GraduationCap className="w-6 h-6 text-slate-950 stroke-[2.5]" />
        </div>
        <div>
          <span className="text-lg font-bold bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
            College RAG AI
          </span>
          <span className="hidden sm:inline-block ml-2 px-2 py-0.5 text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
            Knowledge Engine
          </span>
        </div>
      </Link>

      <div className="flex items-center gap-3 sm:gap-4">
        {isAuthenticated ? (
          <>
            <Link
              to="/chat"
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                location.pathname === '/chat'
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              <span className="hidden sm:inline">Ask AI</span>
            </Link>

            {isAdmin && (
              <Link
                to="/admin"
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                  location.pathname === '/admin'
                    ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                <Shield className="w-4 h-4" />
                <span className="hidden sm:inline">Admin Console</span>
              </Link>
            )}

            <div className="flex items-center gap-2 pl-2 border-l border-slate-700/60">
              <div className="hidden md:flex flex-col items-end">
                <span className="text-xs font-medium text-slate-200">{user?.name}</span>
                <span className={`text-[10px] font-semibold uppercase tracking-wider ${isAdmin ? 'text-indigo-400' : 'text-emerald-400'}`}>
                  {user?.role}
                </span>
              </div>

              <button
                onClick={handleLogout}
                title="Logout"
                className="p-2 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </>
        ) : (
          <div className="flex items-center gap-2.5">
            <Link
              to="/login"
              className="px-4 py-1.5 text-sm font-medium text-slate-200 hover:text-white hover:bg-slate-800/60 rounded-lg transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/signup"
              className="flex items-center gap-1.5 px-4 py-1.5 text-sm font-semibold bg-emerald-500 hover:bg-emerald-400 text-slate-950 rounded-lg shadow-md shadow-emerald-500/20 transition-all hover:shadow-emerald-500/30"
            >
              <Sparkles className="w-4 h-4" />
              Get Started
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};
