export type UserRole = 'student' | 'admin';

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface SourceCitation {
  document_id: string;
  document_title: string;
  filename: string;
  page_number?: number;
  category: string;
  department?: string;
  similarity_score: number;
  excerpt: string;
}

export interface FeedbackInfo {
  id: string;
  rating: number; // 1 or -1
  comment?: string;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceCitation[];
  created_at: string;
  feedback?: FeedbackInfo;
}

export interface ChatSession {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ChatSessionDetail extends ChatSession {
  messages: ChatMessage[];
}

export interface ChatResponse {
  answer: string;
  session_id: string;
  sources: SourceCitation[];
  message_id: string;
  is_unknown: boolean;
}

export type ProcessingStatus = 'UPLOADED' | 'PROCESSING' | 'READY' | 'FAILED';

export interface DocumentItem {
  id: string;
  title: string;
  filename: string;
  category: string;
  department?: string;
  academic_year?: string;
  description?: string;
  processing_status: ProcessingStatus;
  processing_error?: string;
  uploaded_by: string;
  created_at: string;
  updated_at: string;
  chunk_count?: number;
}

export interface DocumentListResponse {
  documents: DocumentItem[];
  total: number;
}

export interface DashboardStats {
  total_documents: number;
  ready_documents: number;
  processing_documents: number;
  failed_documents: number;
  total_chunks: number;
  total_users: number;
  total_questions: number;
}
