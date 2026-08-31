import React from 'react';
import { ChatSession } from '../../types';
import { MessageSquarePlus, Trash2, MessageSquare, Sparkles } from 'lucide-react';

interface ChatSidebarProps {
  sessions: ChatSession[];
  activeSessionId: string | null;
  onSelectSession: (id: string) => void;
  onNewChat: () => void;
  onDeleteSession: (id: string, e: React.MouseEvent) => void;
  isOpenMobile: boolean;
  onCloseMobile: () => void;
}

export const ChatSidebar: React.FC<ChatSidebarProps> = ({
  sessions,
  activeSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
  isOpenMobile,
  onCloseMobile,
}) => {
  return (
    <>
      {isOpenMobile && (
        <div
          onClick={onCloseMobile}
          className="fixed inset-0 z-40 bg-black/70 backdrop-blur-sm md:hidden"
        />
      )}

      <aside
        className={`fixed md:static inset-y-0 left-0 z-40 w-72 flex-shrink-0 flex flex-col glass-panel border-r border-white/10 bg-slate-950/90 transform transition-transform duration-200 ease-in-out md:translate-x-0 ${
          isOpenMobile ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="p-4 border-b border-slate-800">
          <button
            onClick={() => {
              onNewChat();
              onCloseMobile();
            }}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/15 transition-all hover:scale-[1.01] active:scale-[0.99]"
          >
            <MessageSquarePlus className="w-4 h-4 stroke-[2.5]" />
            New Conversation
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-1.5">
          <div className="px-2 py-1 text-[11px] font-bold uppercase tracking-wider text-slate-500">
            Recent Conversations ({sessions.length})
          </div>

          {sessions.length === 0 ? (
            <div className="py-8 text-center px-4">
              <MessageSquare className="w-8 h-8 text-slate-700 mx-auto mb-2" />
              <p className="text-xs text-slate-500">No previous conversations yet.</p>
            </div>
          ) : (
            sessions.map((session) => {
              const isActive = session.id === activeSessionId;
              const formattedDate = new Date(session.updated_at).toLocaleDateString([], {
                month: 'short',
                day: 'numeric'
              });

              return (
                <div
                  key={session.id}
                  onClick={() => {
                    onSelectSession(session.id);
                    onCloseMobile();
                  }}
                  className={`group relative flex items-center justify-between p-2.5 rounded-xl cursor-pointer transition-all ${
                    isActive
                      ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30'
                      : 'hover:bg-slate-800/60 text-slate-300 hover:text-white'
                  }`}
                >
                  <div className="flex items-center gap-2.5 min-w-0 pr-2">
                    <MessageSquare
                      className={`w-4 h-4 flex-shrink-0 ${
                        isActive ? 'text-emerald-400' : 'text-slate-500 group-hover:text-slate-400'
                      }`}
                    />
                    <div className="flex flex-col min-w-0">
                      <span className="text-xs font-medium truncate">{session.title}</span>
                      <span className="text-[10px] text-slate-500">{formattedDate}</span>
                    </div>
                  </div>

                  <button
                    onClick={(e) => onDeleteSession(session.id, e)}
                    title="Delete conversation"
                    className="opacity-0 group-hover:opacity-100 p-1 text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 rounded transition-all"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              );
            })
          )}
        </div>

        <div className="p-3 border-t border-slate-800/80 bg-slate-900/40 text-[11px] text-slate-400 flex items-center gap-2">
          <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
          <span>Grounded RAG Pipeline</span>
        </div>
      </aside>
    </>
  );
};
