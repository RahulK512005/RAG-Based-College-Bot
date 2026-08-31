import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { DocumentItem, DocumentListResponse, DashboardStats } from '../types';
import { StatsGrid } from '../components/Admin/StatsGrid';
import { DocumentTable } from '../components/Admin/DocumentTable';
import { UploadModal } from '../components/Admin/UploadModal';
import { Shield, Upload, Search, Filter, RefreshCw, AlertCircle } from 'lucide-react';

const CATEGORIES = [
  'All',
  'Admissions',
  'Academics',
  'Fees',
  'Examinations',
  'Hostel',
  'Library',
  'Placements',
  'Scholarships',
  'Policies',
  'Events',
  'Clubs',
  'General'
];

export const AdminPage: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [isLoadingStats, setIsLoadingStats] = useState(true);
  const [isLoadingDocs, setIsLoadingDocs] = useState(true);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);

  // 1. Fetch dashboard metrics
  const loadStats = async () => {
    setIsLoadingStats(true);
    try {
      const res = await api.get<DashboardStats>('/analytics/stats');
      setStats(res.data);
    } catch (err: any) {
      console.error('Failed to load stats:', err);
    } finally {
      setIsLoadingStats(false);
    }
  };

  // 2. Fetch document list
  const loadDocuments = async () => {
    setIsLoadingDocs(true);
    setError(null);
    try {
      const params: any = {};
      if (selectedCategory !== 'All') params.category = selectedCategory;
      if (searchQuery.trim()) params.search = searchQuery.trim();

      const res = await api.get<DocumentListResponse>('/documents', { params });
      setDocuments(res.data.documents);
    } catch (err: any) {
      setError(err.message || 'Failed to load documents.');
    } finally {
      setIsLoadingDocs(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  useEffect(() => {
    loadDocuments();
  }, [selectedCategory, searchQuery]);

  // 3. Handle document deletion
  const handleDeleteDocument = async (id: string, title: string) => {
    if (!window.confirm(`Are you sure you want to delete "${title}" and remove all its vector chunks?`)) {
      return;
    }

    try {
      await api.delete(`/documents/${id}`);
      setActionSuccess(`Deleted "${title}" and associated vector embeddings.`);
      await loadDocuments();
      await loadStats();
      setTimeout(() => setActionSuccess(null), 3000);
    } catch (err: any) {
      setError(err.message || 'Failed to delete document.');
    }
  };

  // 4. Handle document reprocessing
  const handleReprocessDocument = async (id: string) => {
    try {
      await api.post(`/documents/${id}/reprocess`);
      setActionSuccess('Triggered document re-extraction and vector embedding.');
      await loadDocuments();
      await loadStats();
      setTimeout(() => setActionSuccess(null), 3000);
    } catch (err: any) {
      setError(err.message || 'Failed to reprocess document.');
    }
  };

  return (
    <div className="min-h-[calc(100vh-65px)] p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              <Shield className="w-5 h-5" />
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Administrator Console</h1>
          </div>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Manage college knowledge base documents, monitor vector chunk index, and audit RAG pipeline metrics.
          </p>
        </div>

        <button
          onClick={() => setIsUploadModalOpen(true)}
          className="flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/20 transition-all hover:scale-105"
        >
          <Upload className="w-4 h-4 stroke-[2.5]" />
          Upload Document
        </button>
      </div>

      {/* Success / Error Banners */}
      {actionSuccess && (
        <div className="mb-6 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-semibold">
          {actionSuccess}
        </div>
      )}

      {error && (
        <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center gap-2.5 text-xs text-rose-400">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Stats Metric Cards */}
      <StatsGrid stats={stats} isLoading={isLoadingStats} />

      {/* Filter and Search Controls */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between mb-4">
        {/* Search */}
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search documents..."
            className="w-full pl-10 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500/50"
          />
        </div>

        {/* Category filter */}
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-slate-400" />
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="bg-slate-900 border border-slate-800 text-xs text-slate-200 rounded-xl px-3 py-2 focus:outline-none focus:border-emerald-500/50 w-full sm:w-auto"
          >
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>
                {cat === 'All' ? 'All Categories' : cat}
              </option>
            ))}
          </select>

          <button
            onClick={() => {
              loadDocuments();
              loadStats();
            }}
            title="Refresh Table"
            className="p-2 text-slate-400 hover:text-white bg-slate-900 border border-slate-800 rounded-xl hover:bg-slate-800 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Documents Table */}
      <DocumentTable
        documents={documents}
        isLoading={isLoadingDocs}
        onReprocess={handleReprocessDocument}
        onDelete={handleDeleteDocument}
      />

      {/* Upload Modal */}
      <UploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onUploadSuccess={() => {
          setActionSuccess('Document uploaded and indexed successfully into vector database.');
          loadDocuments();
          loadStats();
          setTimeout(() => setActionSuccess(null), 3000);
        }}
      />
    </div>
  );
};
