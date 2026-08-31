import React from 'react';
import { DocumentItem } from '../../types';
import { RefreshCw, Trash2, FileText, CheckCircle2, Clock, AlertTriangle, Layers, Tag } from 'lucide-react';

interface DocumentTableProps {
  documents: DocumentItem[];
  isLoading: boolean;
  onReprocess: (id: string) => void;
  onDelete: (id: string, title: string) => void;
}

export const DocumentTable: React.FC<DocumentTableProps> = ({
  documents,
  isLoading,
  onReprocess,
  onDelete,
}) => {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'READY':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <CheckCircle2 className="w-3 h-3" />
            READY
          </span>
        );
      case 'PROCESSING':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20 animate-pulse">
            <Clock className="w-3 h-3" />
            PROCESSING
          </span>
        );
      case 'FAILED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
            <AlertTriangle className="w-3 h-3" />
            FAILED
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-800 text-slate-400">
            {status}
          </span>
        );
    }
  };

  if (isLoading) {
    return (
      <div className="py-16 flex flex-col items-center justify-center gap-3">
        <div className="w-8 h-8 border-3 border-emerald-500 border-t-transparent rounded-full animate-spin" />
        <span className="text-xs text-slate-400">Loading documents...</span>
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="py-16 text-center rounded-2xl glass-panel border border-dashed border-slate-800">
        <FileText className="w-12 h-12 text-slate-700 mx-auto mb-3" />
        <h4 className="text-base font-semibold text-slate-300">No documents found</h4>
        <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
          Upload official college PDFs, DOCX, or TXT documents to index them into the RAG vector database.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-2xl glass-panel border border-white/10 shadow-xl">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-900/80 text-xs font-semibold uppercase tracking-wider text-slate-400 border-b border-slate-800">
          <tr>
            <th className="py-3.5 px-4">Document Title</th>
            <th className="py-3.5 px-4">Category</th>
            <th className="py-3.5 px-4">Department / Year</th>
            <th className="py-3.5 px-4">Chunks</th>
            <th className="py-3.5 px-4">Status</th>
            <th className="py-3.5 px-4">Uploaded</th>
            <th className="py-3.5 px-4 text-right">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800/60 font-sans">
          {documents.map((doc) => {
            const formattedDate = new Date(doc.created_at).toLocaleDateString([], {
              month: 'short',
              day: 'numeric',
              year: 'numeric'
            });

            return (
              <tr key={doc.id} className="hover:bg-slate-800/40 transition-colors group">
                <td className="py-3.5 px-4">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 flex-shrink-0">
                      <FileText className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <div className="font-semibold text-slate-200 group-hover:text-white truncate max-w-xs">
                        {doc.title}
                      </div>
                      <div className="text-xs text-slate-500 truncate max-w-xs">{doc.filename}</div>
                    </div>
                  </div>
                </td>

                <td className="py-3.5 px-4">
                  <span className="inline-flex items-center gap-1 text-xs text-slate-300 bg-slate-800/80 px-2 py-0.5 rounded-md border border-slate-700">
                    <Tag className="w-3 h-3 text-emerald-400" />
                    {doc.category}
                  </span>
                </td>

                <td className="py-3.5 px-4 text-xs text-slate-400">
                  <div>{doc.department || 'All Departments'}</div>
                  {doc.academic_year && <div className="text-slate-500">{doc.academic_year}</div>}
                </td>

                <td className="py-3.5 px-4 text-xs text-slate-300 font-mono">
                  <span className="inline-flex items-center gap-1">
                    <Layers className="w-3.5 h-3.5 text-purple-400" />
                    {doc.chunk_count || 0}
                  </span>
                </td>

                <td className="py-3.5 px-4">
                  <div>
                    {getStatusBadge(doc.processing_status)}
                    {doc.processing_error && (
                      <div className="text-[10px] text-rose-400 mt-1 truncate max-w-[150px]" title={doc.processing_error}>
                        {doc.processing_error}
                      </div>
                    )}
                  </div>
                </td>

                <td className="py-3.5 px-4 text-xs text-slate-500">{formattedDate}</td>

                <td className="py-3.5 px-4 text-right">
                  <div className="flex items-center justify-end gap-1.5">
                    <button
                      onClick={() => onReprocess(doc.id)}
                      title="Reprocess Document"
                      className="p-1.5 text-slate-400 hover:text-cyan-400 hover:bg-cyan-500/10 rounded-lg transition-colors"
                    >
                      <RefreshCw className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onDelete(doc.id, doc.title)}
                      title="Delete Document & Vectors"
                      className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};
