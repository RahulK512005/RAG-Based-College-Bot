import React, { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';
import { ChatSession, ChatMessage as ChatMessageType, ChatResponse } from '../types';
import { ChatSidebar } from '../components/Chat/ChatSidebar';
import { ChatMessage } from '../components/Chat/ChatMessage';
import { ChatInput } from '../components/Chat/ChatInput';
import { SuggestedQuestions } from '../components/Chat/SuggestedQuestions';
import { Menu, Sparkles, AlertCircle } from 'lucide-react';

export const ChatPage: React.FC = () => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isSending]);

  const loadSessions = async () => {
    try {
      const res = await api.get<ChatSession[]>('/chats');
      setSessions(res.data);
      if (res.data.length > 0 && !activeSessionId) {
        setActiveSessionId(res.data[0].id);
      }
    } catch (err: any) {
      console.error('Failed to load sessions:', err);
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    if (!activeSessionId) {
      setMessages([]);
      return;
    }

    const loadMessages = async () => {
      setIsLoadingMessages(true);
      setError(null);
      try {
        const res = await api.get<ChatMessageType[]>(`/chats/${activeSessionId}/messages`);
        setMessages(res.data);
      } catch (err: any) {
        setError(err.message || 'Failed to load conversation history.');
      } finally {
        setIsLoadingMessages(false);
      }
    };

    loadMessages();
  }, [activeSessionId]);

  const handleSendMessage = async (questionText: string, categoryFilter?: string) => {
    setError(null);
    setIsSending(true);

    const tempUserMessage: ChatMessageType = {
      id: `temp_${Date.now()}`,
      session_id: activeSessionId || 'pending',
      role: 'user',
      content: questionText,
      sources: [],
      created_at: new Date().toISOString()
    };
    setMessages((prev) => [...prev, tempUserMessage]);

    try {
      const payload = {
        question: questionText,
        session_id: activeSessionId || undefined,
        category_filter: categoryFilter
      };

      const res = await api.post<ChatResponse>('/chat', payload);
      const data = res.data;

      if (!activeSessionId || activeSessionId !== data.session_id) {
        setActiveSessionId(data.session_id);
        await loadSessions();
      }

      const assistantMessage: ChatMessageType = {
        id: data.message_id,
        session_id: data.session_id,
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        created_at: new Date().toISOString()
      };

      setMessages((prev) => [...prev.filter((m) => m.id !== tempUserMessage.id), tempUserMessage, assistantMessage]);
    } catch (err: any) {
      setError(err.message || 'Failed to retrieve information from knowledge base.');
    } finally {
      setIsSending(false);
    }
  };

  const handleNewChat = () => {
    setActiveSessionId(null);
    setMessages([]);
    setError(null);
  };

  const handleDeleteSession = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await api.delete(`/chats/${sessionId}`);
      const updated = sessions.filter((s) => s.id !== sessionId);
      setSessions(updated);
      if (activeSessionId === sessionId) {
        if (updated.length > 0) {
          setActiveSessionId(updated[0].id);
        } else {
          handleNewChat();
        }
      }
    } catch (err: any) {
      console.error('Failed to delete session:', err);
    }
  };

  return (
    <div className="flex h-[calc(100vh-65px)] overflow-hidden bg-[#0b0f17]">
      <ChatSidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={setActiveSessionId}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
        isOpenMobile={isMobileSidebarOpen}
        onCloseMobile={() => setIsMobileSidebarOpen(false)}
      />

      <main className="flex-1 flex flex-col h-full min-w-0 relative">
        <div className="px-4 py-2.5 glass-panel border-b border-white/5 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <button
              onClick={() => setIsMobileSidebarOpen(true)}
              className="p-1.5 text-slate-400 hover:text-white rounded-lg md:hidden"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-emerald-400" />
              <span className="text-sm font-bold text-slate-200 truncate">
                {activeSessionId
                  ? sessions.find((s) => s.id === activeSessionId)?.title || 'Active Conversation'
                  : 'New Conversation'}
              </span>
            </div>
          </div>
          <span className="text-[11px] font-semibold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
            pgvector RAG Active
          </span>
        </div>

        {error && (
          <div className="m-4 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center gap-2.5 text-xs text-rose-400">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <div className="flex-1 overflow-y-auto px-4 sm:px-6 py-4 space-y-4">
          {isLoadingMessages ? (
            <div className="h-full flex flex-col items-center justify-center gap-3 py-16">
              <div className="w-8 h-8 border-3 border-emerald-500 border-t-transparent rounded-full animate-spin" />
              <span className="text-xs text-slate-400 font-medium">Loading knowledge stream...</span>
            </div>
          ) : messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center py-10">
              <div className="w-16 h-16 rounded-3xl bg-gradient-to-tr from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-4 shadow-xl shadow-emerald-500/10 animate-pulse-glow">
                <Sparkles className="w-8 h-8" />
              </div>
              <h2 className="text-xl sm:text-2xl font-bold text-white text-center">
                College AI Knowledge Assistant
              </h2>
              <p className="text-xs sm:text-sm text-slate-400 max-w-md text-center mt-1 mb-4">
                Ask any question about admissions, tuition fees, course curriculum, hostel rules, or placement statistics.
              </p>

              <SuggestedQuestions onSelect={(q) => handleSendMessage(q)} />
            </div>
          ) : (
            <>
              {messages.map((msg) => (
                <ChatMessage key={msg.id} message={msg} />
              ))}

              {isSending && (
                <div className="flex items-center gap-3 my-4">
                  <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center text-slate-950 animate-pulse">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div className="glass-panel border-white/10 rounded-2xl rounded-bl-none px-4 py-3 text-xs text-slate-300 flex items-center gap-2">
                    <div className="w-2 h-2 bg-emerald-400 rounded-full animate-ping" />
                    <span>Searching vector knowledge base and synthesizing grounded response...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        <ChatInput onSendMessage={handleSendMessage} isLoading={isSending} />
      </main>
    </div>
  );
};
