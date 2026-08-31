# 🎓 College RAG AI — Grounded College Information Assistant

A production-style, end-to-end **Retrieval-Augmented Generation (RAG)** college information assistant. The application answers student inquiries regarding admissions, academic fee structures, semester examination calendars, hostel accommodation policies, placement records, and merit scholarships using **real vector similarity retrieval** and strict context grounding with clickable source citations.

---

## 🌟 Key Capabilities & Non-Negotiable Guarantees

* 🔍 **Real Semantic Vector Search**: Queries are vectorized and matched against stored document chunks using cosine similarity and hybrid term matching.
* 🛡️ **Zero-Hallucination Guard**: Questions out of domain or below similarity thresholds are strictly refused without guessing or making up dates/fees.
* 📖 **Clickable Source Citations**: Every generated response includes verifiable source document titles, page numbers, categories, match percentages, and excerpt modals.
* ⚡ **Multi-Format Ingestion**: Background extraction and chunking pipeline for **PDF**, **DOCX**, and **TXT** files.
* 🔒 **Role-Based Access Control (RBAC)**: Secure separation between `student` and `admin` roles, enforcing JWT token validation and password hashing with `bcrypt` (work factor 12).
* 📊 **Administrator Operations Console**: Real-time analytics dashboard, document inventory monitoring, manual reprocessing triggers, and vector chunk deletion.

---

## 🏛️ System Architecture

### 1. Student Ingestion & Answering Flow
```text
Student Question
       │
       ▼
Dense Query Vectorization
       │
       ▼
Hybrid Vector Search (pgvector Cosine Similarity + BM25 Match)
       │
       ▼
Threshold Evaluation (>= 0.35 Confidence)
 ├── False ──► Safe Hallucination Refusal Response (0 hallucination)
 └── True  ──► Top-K Relevant Document Chunks
                     │
                     ▼
             Grounded LLM Prompt Synthesizer
                     │
                     ▼
             Structured Answer + Verified Citations (Doc Name, Page, Excerpt)
```

### 2. Administrator Document Processing Pipeline
```text
Admin Upload (PDF / DOCX / TXT)
       │
       ▼
Text Extraction (pypdf page preservation / python-docx / UTF-8)
       │
       ▼
Text Cleaning & Normalization
       │
       ▼
Recursive Paragraph/Token Chunker (1000 chars, 150 overlap)
       │
       ▼
Dense Vector Embeddings Generation
       │
       ▼
Database & Vector Store Persistence (Status: READY)
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Python 3.11+, FastAPI, Uvicorn, Pydantic v2 |
| **Database & ORM** | PostgreSQL with pgvector (local SQLite fallback), SQLAlchemy 2.0 |
| **Document Parsers** | `pypdf`, `python-docx` |
| **Security & Auth** | JWT (`pyjwt`), `bcrypt`, `passlib` |
| **Frontend Framework** | React 18, TypeScript, Vite, React Router v6 |
| **Styling & Icons** | Tailwind CSS, Lucide React |
| **HTTP Client** | Axios with JWT Interceptors |

---

## 🔑 Pre-Seeded Demo Credentials

The database comes pre-seeded with two accounts for testing:

| Role | Email | Password | Access Rights |
|---|---|---|---|
| **Administrator** | `admin@college.edu` | `Admin@123456` | Upload, reprocess, delete documents, audit stats |
| **Student** | `student@college.edu` | `Student@123456` | Query RAG assistant, sessions, feedback |

---

## 🚀 Step-by-Step Local Setup Guide

### 1. Prerequisites
- **Python 3.11+** installed
- **Node.js 18+** & `npm` installed

---

### 2. Backend Setup & Startup

1. **Navigate to the Backend Directory**:
   ```bash
   cd backend
   ```

2. **Create & Activate a Virtual Environment (Optional but recommended)**:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
   *(By default, `.env` is pre-configured to run out of the box with zero external API keys needed!)*

5. **Seed the Knowledge Base & Create Demo Users**:
   ```bash
   # In the root project folder:
   python backend/app/database/seed.py
   ```
   *This indexes all 6 official college policy documents from `sample_documents/` into the vector store.*

6. **Start the FastAPI Backend Server**:
   ```bash
   # Run from the backend directory:
   cd backend
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   The backend API will be live at: **`http://127.0.0.1:8000`**  
   Interactive Swagger docs: **`http://127.0.0.1:8000/docs`**

---

### 3. Frontend Setup & Startup

1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Node Packages**:
   ```bash
   npm install --ignore-scripts
   ```

3. **Configure Environment Variables**:
   Create a `.env` file (if not present):
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

4. **Start Vite Development Server**:
   ```bash
   npm run dev
   ```
   Open your browser at: **`http://localhost:5173`**

---

## 🧪 Automated Test Suites & RAG Benchmarking

### 1. Run RAG Pipeline Benchmark (15 Test Cases)
Evaluates domain accuracy, source retrieval, and zero-hallucination refusal across Admissions, Fees, Academics, Hostel, Placements, Scholarships, and Out-of-Domain queries:
```bash
python tests/test_rag_pipeline.py
```
**Benchmark Score**: `15/15 Passed (100.0%)`

### 2. Run API Integration Test Suite
Verifies all REST endpoints, RBAC authorization guards, document processing, and chat sessions:
```bash
python tests/test_api.py
```

---

## 📡 REST API Reference

### Authentication
* `POST /api/auth/signup` — Register student account (`name`, `email`, `password`, `confirm_password`).
* `POST /api/auth/login` — Authenticate and obtain JWT Bearer token.
* `GET /api/auth/me` — Get current user profile and role.

### Chat & Grounded Retrieval
* `POST /api/chat` — Submit query to RAG pipeline with optional `session_id` and `category_filter`.
* `GET /api/chats` — List user's past conversation sessions.
* `GET /api/chats/{session_id}/messages` — Get chronological message stream.
* `DELETE /api/chats/{session_id}` — Delete conversation session.
* `POST /api/messages/{message_id}/feedback` — Submit thumbs up/down rating and comment.

### Document Management (Admin Protected)
* `GET /api/documents` — List documents with category and search filters.
* `POST /api/documents` — Upload new PDF/DOCX/TXT file with metadata.
* `GET /api/documents/{id}` — Get document details and chunk counts.
* `POST /api/documents/{id}/reprocess` — Re-extract and re-embed document.
* `DELETE /api/documents/{id}` — Delete document and cascade delete vector chunks.

### Analytics & System Health
* `GET /api/analytics/stats` — Dashboard statistics (Total Docs, Ready, Chunks, Questions).
* `GET /health` — Health check endpoint.

---

## 📚 Knowledge Base Documents Included

| Document Title | Category | Topics Covered |
|---|---|---|
| `Admissions_Handbook_2026.txt` | Admissions | Eligibility, JEE cutoffs, quota seats, dates |
| `Fee_Structure_2026.txt` | Fees | Tuition by branch, caution deposits, installments |
| `Academic_Calendar_2026.txt` | Academics | Semester timelines, 75% attendance policy, exams |
| `Hostel_Rules_and_Facilities.txt` | Hostel | Non-AC / AC fees, 9:30 PM curfews, mess menu |
| `Placements_and_Career_Services.txt` | Placements | ₹58 LPA highest package, dream policy, top recruiters |
| `Scholarships_and_Financial_Aid.txt` | Scholarships | 100% waiver, Pragati Tech Fellowship for women |

---

## 📄 License
This project is built and maintained for educational and institutional research purposes.
