# RAG-Based College Information Assistant

## Product & Technical Specification

**Project Type:** Full-Stack AI Application
**Difficulty:** Medium
**Primary Goal:** Build a production-style college information chatbot using Retrieval-Augmented Generation (RAG).

---

# 1. Project Overview

Build a full-stack AI-powered college information assistant that allows students to ask questions about college-related information such as:

- Admissions
- Departments
- Courses
- Fees
- Examinations
- Academic calendar
- Hostel
- Library
- Clubs
- Placements
- Scholarships
- College policies
- Events
- Notices
- Frequently asked questions

The application MUST use a real RAG pipeline.

The chatbot must NOT simply send user questions directly to an LLM.

The required flow is:

```text
College Documents
       ↓
Text Extraction
       ↓
Text Cleaning
       ↓
Chunking
       ↓
Embedding Generation
       ↓
Vector Database
       ↓
Similarity Search
       ↓
Relevant Context
       ↓
LLM
       ↓
Grounded Answer
       ↓
Sources / References
```

The final answer must be grounded in the retrieved college documents.

---

# 2. Core Objectives

The application must:

1. Allow students to create accounts and log in.
2. Provide a responsive chatbot interface.
3. Allow administrators to upload college documents.
4. Extract text from uploaded documents.
5. Split documents into meaningful chunks.
6. Generate embeddings for document chunks.
7. Store embeddings in a vector database.
8. Perform semantic similarity search for user questions.
9. Retrieve relevant document chunks.
10. Send retrieved context to an LLM.
11. Generate an answer based on retrieved context.
12. Display the sources used for the answer.
13. Refuse to invent information when relevant information is unavailable.
14. Maintain conversation history.
15. Provide an admin interface for document management.
16. Persist application data in a database.
17. Deploy the complete application online.

---

# 3. Recommended Technology Stack

Use a modern and maintainable architecture.

## Frontend

- React
- Vite
- TypeScript
- Tailwind CSS
- React Router
- Axios or Fetch API

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

## AI / RAG

- LLM API such as OpenAI-compatible LLM provider
- Embedding model
- LangChain or lightweight custom RAG implementation where appropriate
- Vector database

## Vector Database

Preferred:

- PostgreSQL + pgvector through Supabase

Alternative:

- Qdrant
- Pinecone
- Chroma for local development only

Prefer **Supabase PostgreSQL + pgvector** for production if practical.

## Database

Supabase PostgreSQL.

Store:

- Users
- User roles
- Documents
- Document chunks
- Chat sessions
- Chat messages
- Feedback
- Document metadata

## File Storage

Use Supabase Storage or another production-compatible object storage service.

Do NOT store large PDF binary files directly inside PostgreSQL.

## Deployment

Frontend:

- Vercel

Backend:

- Render

Database:

- Supabase

Source control:

- GitHub

---

# 4. Repository Structure

The repository MUST follow this structure:

```text
college-rag-chatbot/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── contexts/
│   │   ├── types/
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   └── .env.example
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── rag/
│   │   ├── auth/
│   │   ├── database/
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
│
├── README.md
├── .gitignore
└── spec.md
```

Keep frontend and backend clearly separated.

---

# 5. User Roles

Implement role-based access.

## Student

Students can:

- Sign up
- Log in
- Log out
- Ask questions
- View answers
- View sources
- View chat history
- Create new conversations
- Delete their conversations
- Give feedback on answers

Students MUST NOT be able to:

- Upload documents
- Delete documents
- Update documents
- Access admin dashboard
- Manage users

## Admin

Admins can:

- Log in
- View admin dashboard
- Upload documents
- View uploaded documents
- Delete documents
- Replace/update documents
- View document processing status
- View document metadata
- View basic usage analytics

---

# 6. Authentication

Implement secure authentication.

Required functionality:

```text
Signup
Login
Logout
Protected Routes
Role-Based Authorization
Session Management
```

Password requirements:

- Minimum 8 characters
- Passwords must never be stored in plaintext

Use secure password hashing.

Authentication tokens/session information must be handled securely.

Never expose secrets in frontend source code.

---

# 7. Frontend Requirements

The frontend must be responsive and usable on:

- Desktop
- Tablet
- Mobile

## Main Pages

### 7.1 Landing Page

Include:

- Project name
- Short explanation
- Key features
- "Get Started" button
- Login button
- Signup button

---

### 7.2 Login Page

Fields:

- Email
- Password

Actions:

- Login
- Navigate to signup

Include:

- Validation
- Loading state
- Error messages

---

### 7.3 Signup Page

Fields:

- Full name
- Email
- Password
- Confirm password

Include:

- Validation
- Password mismatch handling
- Loading state
- Error handling

Do NOT allow users to self-register as admin.

---

# 8. Student Chat Interface

Create a professional AI-chat interface.

Layout:

```text
------------------------------------------------
| College AI Assistant                         |
------------------------------------------------
| Sidebar                | Chat                |
|                        |                     |
| New Chat               | User Question      |
| Recent Conversations   |                     |
|                        | AI Answer           |
|                        | Sources             |
|                        |                     |
|                        |---------------------|
|                        | Ask a question...   |
------------------------------------------------
```

Features:

- New conversation
- Conversation list
- Message bubbles
- User/assistant distinction
- Loading indicator
- Error state
- Auto-scroll
- Send button
- Enter-to-send
- Disable send while processing
- Mobile responsive layout

---

# 9. Suggested Questions

Display suggested questions such as:

```text
What are the admission requirements?

What is the fee structure for CSE?

When are the semester examinations?

What scholarships are available?

What are the hostel rules?

What is the academic calendar?

What companies participate in placements?
```

These must be configurable.

---

# 10. Chat Answer Requirements

Every AI answer must be generated using retrieved context.

The LLM prompt must enforce:

```text
You are a college information assistant.

Answer ONLY using the supplied retrieved context.

If the context does not contain enough information to answer the question,
clearly state that the information is not available in the college knowledge base.

Do not invent:
- fees
- dates
- policies
- contact information
- admission requirements
- statistics
- deadlines
- rules

When possible, mention the relevant source.
```

The backend MUST perform retrieval before generating the answer.

---

# 11. Unknown Question Handling

This is mandatory.

If no relevant document chunks are found, return a response such as:

```text
I couldn't find reliable information about that in the college knowledge base.

Please try rephrasing your question or contact the relevant college department.
```

The system MUST NOT hallucinate an answer.

Implement a configurable similarity/relevance threshold.

Example:

```text
SIMILARITY_THRESHOLD=0.70
```

The exact threshold should be configurable through environment variables.

---

# 12. Document Upload

Only admins can upload documents.

Supported formats:

- PDF
- DOCX
- TXT

Optional:

- Images for OCR

Upload form should include:

- Document title
- Category
- Department
- Academic year
- Description
- File

Categories:

```text
Admissions
Academics
Fees
Examinations
Hostel
Library
Placements
Scholarships
Policies
Events
Clubs
General
```

---

# 13. Document Processing Pipeline

When an administrator uploads a document:

```text
Upload File
    ↓
Validate File
    ↓
Store Original File
    ↓
Extract Text
    ↓
Clean Text
    ↓
Split Into Chunks
    ↓
Generate Embeddings
    ↓
Store Chunks + Embeddings
    ↓
Mark Document as READY
```

Processing status:

```text
UPLOADED
PROCESSING
READY
FAILED
```

If processing fails:

- Store failure status
- Store error message
- Do not expose internal stack traces to users

---

# 14. Text Extraction

For PDFs:

Use a reliable PDF text extraction library.

For DOCX:

Use a DOCX extraction library.

For TXT:

Read the text directly.

The extraction layer should be abstracted so additional document types can be added later.

---

# 15. Chunking

Documents must be split into chunks before embedding.

Recommended initial configuration:

```text
Chunk size: 800–1200 tokens
Chunk overlap: 100–200 tokens
```

Make these configurable.

Chunks should preserve useful metadata:

```text
document_id
document_name
page_number
section
category
department
academic_year
chunk_index
```

Avoid arbitrary splitting where possible.

Prefer paragraph/section-aware splitting.

---

# 16. Embedding Generation

Generate embeddings for every chunk.

The embedding service must support:

```text
text → vector
```

Store:

- embedding model
- vector
- chunk ID
- document ID

Do not generate embeddings for the user query using a different embedding model from the document embeddings.

The same embedding model/version must be used consistently for indexing and retrieval.

---

# 17. Vector Database

Use PostgreSQL with pgvector through Supabase where possible.

Create a vector column for document chunks.

Conceptual structure:

```text
document_chunks
----------------
id
document_id
content
embedding
page_number
section
chunk_index
metadata
created_at
```

Create an appropriate vector index if supported by the chosen implementation.

---

# 18. Semantic Search

When a student asks a question:

```text
Question
   ↓
Query Embedding
   ↓
Vector Similarity Search
   ↓
Top K Chunks
```

Initial configuration:

```text
TOP_K=5
```

Make it configurable.

Return:

- Chunk content
- Document title
- Page number
- Similarity/relevance score
- Metadata

Do not return irrelevant chunks simply to fill TOP_K.

---

# 19. Optional Hybrid Search

If implementation time allows, support:

```text
Semantic Search
+
Keyword Search
```

Then combine/re-rank the results.

This is especially useful for queries containing:

- Course codes
- Department names
- Specific policy names
- Dates
- Notice numbers
- Faculty names

Hybrid retrieval is a bonus feature, not a core requirement.

---

# 20. RAG Generation Pipeline

Backend flow:

```text
POST /api/chat

        ↓

Authenticate User

        ↓

Validate Question

        ↓

Create Query Embedding

        ↓

Vector Search

        ↓

Filter Low-Relevance Results

        ↓

Build Context

        ↓

LLM Prompt

        ↓

Generate Grounded Answer

        ↓

Attach Sources

        ↓

Save Chat Message

        ↓

Return Response
```

The LLM must never receive an empty or irrelevant context and then be allowed to answer from general knowledge.

---

# 21. RAG Prompt Structure

Use a structured prompt similar to:

```text
SYSTEM:

You are an AI assistant for a college.

Your job is to answer student questions using ONLY the
provided college knowledge-base context.

Rules:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not supported by the context, say that
   the information is unavailable in the knowledge base.
4. Prefer precise and concise answers.
5. If the context contains conflicting information, mention
   the conflict instead of guessing.
6. Include source references when available.

RETRIEVED CONTEXT:

[Document: Academic Calendar 2026]
[Page: 2]
...

[Document: Student Handbook]
[Page: 14]
...

USER QUESTION:

...
```

---

# 22. Source Display

Every grounded answer should display its sources.

Example:

```text
Answer:
The semester examinations are scheduled to begin on...

Sources:
📄 Academic Calendar 2026
Page 2

📄 Examination Notice
Page 1
```

Sources should be clickable where possible.

The source UI should show:

- Document name
- Page number
- Category
- Relevant excerpt

Do not display raw vector IDs.

---

# 23. Conversation History

Store chat history.

Database structure:

```text
chat_sessions
---------------
id
user_id
title
created_at
updated_at
```

```text
chat_messages
--------------
id
session_id
role
content
sources
created_at
```

Roles:

```text
user
assistant
```

A conversation should preserve enough previous context to support follow-up questions.

Example:

```text
User:
What is the CSE fee?

Assistant:
...

User:
What about hostel?

Assistant:
...
```

The backend should understand the conversation context where appropriate.

Do not blindly send unlimited history to the LLM.

Use a configurable conversation window.

---

# 24. Database Schema

Create the following logical tables.

## users

```text
id
name
email
password_hash / auth_reference
role
created_at
updated_at
```

## documents

```text
id
title
filename
category
department
academic_year
description
storage_path
processing_status
processing_error
uploaded_by
created_at
updated_at
```

## document_chunks

```text
id
document_id
content
embedding
page_number
section
chunk_index
metadata
created_at
```

## chat_sessions

```text
id
user_id
title
created_at
updated_at
```

## chat_messages

```text
id
session_id
role
content
sources
created_at
```

## feedback

```text
id
message_id
user_id
rating
comment
created_at
```

Use proper foreign keys and relationships.

---

# 25. API Design

Use REST APIs.

## Authentication

```text
POST /api/auth/signup
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
```

## Chat

```text
POST /api/chat
GET  /api/chats
POST /api/chats
GET  /api/chats/{id}
DELETE /api/chats/{id}
```

## Messages

```text
GET /api/chats/{id}/messages
POST /api/messages/{id}/feedback
```

## Documents

Admin only:

```text
POST   /api/documents
GET    /api/documents
GET    /api/documents/{id}
DELETE /api/documents/{id}
PUT    /api/documents/{id}
POST   /api/documents/{id}/reprocess
```

## Health

```text
GET /health
```

Return:

```json
{
  "status": "ok"
}
```

---

# 26. Input Validation

Validate all API input.

Examples:

- Email format
- Password length
- Question length
- File type
- File size
- Document title
- Category
- Pagination values
- IDs

Reject malformed requests with appropriate HTTP status codes.

Never trust frontend validation alone.

---

# 27. Error Handling

Implement consistent API errors.

Example:

```json
{
  "error": {
    "code": "DOCUMENT_PROCESSING_FAILED",
    "message": "The document could not be processed."
  }
}
```

Do not expose:

- Stack traces
- API keys
- Database credentials
- Internal paths
- Provider secrets

Frontend must show user-friendly error messages.

---

# 28. Loading States

The UI must clearly show loading states for:

- Login
- Signup
- Chat response
- Document upload
- Document processing
- Delete operations
- Chat history loading

For chat generation, prefer streaming responses as a bonus feature.

---

# 29. Admin Dashboard

Create a separate protected admin dashboard.

Dashboard should display:

```text
Total Documents
Ready Documents
Processing Documents
Failed Documents
Total Users
Total Questions
```

Document table:

```text
Document
Category
Department
Academic Year
Status
Uploaded Date
Actions
```

Actions:

```text
View
Reprocess
Delete
```

---

# 30. Document Management

Deleting a document must also remove its associated vector chunks.

Expected behavior:

```text
Delete Document
      ↓
Delete document chunks
      ↓
Delete stored file
      ↓
Delete document record
```

Handle failures carefully so orphaned vectors/files do not accumulate.

---

# 31. Security Requirements

Mandatory:

- Environment variables for secrets
- No API keys in frontend
- No `.env` committed
- Password hashing
- Authentication middleware
- Authorization checks
- Admin-only document APIs
- File type validation
- File size limits
- Input validation
- CORS configuration
- Rate limiting where practical

Add:

```text
.env
.env.*
!.env.example
```

to `.gitignore`.

---

# 32. Environment Variables

Create:

```text
# Backend
DATABASE_URL=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
LLM_API_KEY=
EMBEDDING_API_KEY=
JWT_SECRET=
CORS_ORIGINS=
TOP_K=5
SIMILARITY_THRESHOLD=0.70
CHUNK_SIZE=1000
CHUNK_OVERLAP=150

# Frontend
VITE_API_BASE_URL=
```

Never commit actual values.

Only `.env.example` files should be committed.

---

# 33. Frontend Environment Security

IMPORTANT:

Only variables explicitly intended for frontend use may use:

```text
VITE_
```

Never expose:

```text
SUPABASE_SERVICE_ROLE_KEY
LLM_API_KEY
JWT_SECRET
DATABASE_URL
```

to the frontend.

---

# 34. UI/UX Design

Design should feel like a modern AI product rather than a basic college CRUD application.

Visual direction:

- Clean
- Professional
- Minimal
- Accessible
- Responsive
- Good typography
- Clear spacing
- Subtle animations
- Proper empty states

Use a consistent design system.

Include:

- Navbar
- Sidebar where appropriate
- Cards
- Buttons
- Forms
- Modals
- Toast notifications
- Skeleton/loading states
- Error states

Do not overuse gradients or unnecessary animations.

---

# 35. Accessibility

Implement:

- Semantic HTML
- Keyboard navigation
- Proper labels
- Focus states
- Accessible buttons
- Sufficient color contrast
- Screen-reader-friendly form errors

---

# 36. Bonus Features

Implement only after ALL core features work.

Priority order:

### Priority 1

- Suggested questions
- Answer feedback
- Streaming responses
- Source highlighting

### Priority 2

- Department-wise collections
- Hybrid search
- Document re-ranking
- Confidence/relevance score

### Priority 3

- OCR
- Multilingual chatbot
- Voice input
- Conversation export
- AI-generated FAQs
- Admin analytics
- Document version management

Do NOT sacrifice the core RAG pipeline to implement bonus features.

---

# 37. RAG Quality Requirements

The system must demonstrate that it actually retrieves information.

For debugging/development, log:

```text
User Query
Query Embedding Generated
Retrieved Chunks
Similarity Scores
Final Context
LLM Response
Sources
```

Do not expose sensitive information in production logs.

The admin/developer should be able to verify:

```text
Question
→ Retrieved document
→ Retrieved chunk
→ Generated answer
```

---

# 38. RAG Evaluation

Create a small evaluation dataset.

Example:

```text
Question:
What is the fee for B.Tech CSE?

Expected Source:
Fee Structure 2026.pdf
```

Include at least 10–20 questions covering different categories.

Evaluate:

- Retrieval relevance
- Source correctness
- Answer grounding
- Unknown question handling

Example evaluation cases:

```text
Known question
Known question with different wording
Specific date question
Specific fee question
Policy question
Multi-step/follow-up question
Unknown question
Ambiguous question
```

---

# 39. Hallucination Prevention

The system should prioritize correctness over answering every question.

If information is unavailable:

```text
I couldn't find this information in the college knowledge base.
```

is a valid and preferred answer.

Never fabricate:

- Dates
- Fees
- Statistics
- Deadlines
- Rules
- Faculty information
- Placement packages
- Scholarship amounts

---

# 40. Deployment Architecture

Use:

```text
                 GitHub
                   |
        -----------------------
        |                     |
      Vercel                Render
        |                     |
    Frontend               FastAPI
                              |
                    ------------------
                    |                |
                 Supabase         LLM API
                    |
             PostgreSQL
              + pgvector
                    |
             Supabase Storage
```

---

# 41. Deployment Requirements

Frontend must be deployed to Vercel.

Backend must be deployed to Render.

Database must be hosted on Supabase.

The deployed application must:

- Load successfully
- Allow signup/login
- Allow authenticated users to chat
- Retrieve document context
- Generate answers
- Display sources
- Persist conversations
- Allow admin document management

Do not submit a deployment that only works locally.

---

# 42. GitHub Requirements

Repository must contain:

```text
frontend/
backend/
README.md
spec.md
.gitignore
```

Do NOT commit:

```text
.env
API keys
Passwords
JWT secrets
Database credentials
OAuth secrets
Private tokens
```

Use environment variables.

---

# 43. README Requirements

README.md MUST contain:

## 1. Project Name

## 2. Problem Statement

Explain the problem and why the application is useful.

## 3. Features

Clearly separate:

```text
Core Features
Bonus Features
```

## 4. Technology Stack

Mention:

- Frontend
- Backend
- Database
- Vector database
- LLM
- Embedding model
- Deployment platforms

## 5. Architecture

Include the RAG architecture.

## 6. RAG Pipeline

Explain:

```text
Document
→ Extraction
→ Chunking
→ Embeddings
→ Vector Search
→ Context
→ LLM
→ Answer
→ Sources
```

## 7. Screenshots

Include screenshots of:

- Landing page
- Login
- Chat
- Sources
- Admin dashboard
- Document upload

## 8. Live Demo

Provide deployed Vercel URL.

## 9. Backend

Provide deployed backend URL.

## 10. Setup Instructions

Explain:

```text
Clone repository
Install dependencies
Configure environment variables
Setup database
Run backend
Run frontend
```

## 11. Environment Variables

List variable names only.

Never expose actual secrets.

## 12. API Documentation

Mention available API endpoints.

---

# 44. Testing Requirements

Create tests for important functionality.

Minimum:

### Backend

- Authentication
- Authorization
- Document upload validation
- Chunking
- Retrieval
- Unknown question handling
- Chat API

### Frontend

- Login form
- Signup form
- Chat interaction
- Protected routes
- Admin route protection

---

# 45. Definition of Done

The project is considered complete ONLY when all of the following work:

### Authentication

- [ ] Signup works
- [ ] Login works
- [ ] Logout works
- [ ] Protected routes work
- [ ] Admin authorization works

### RAG

- [ ] PDF upload works
- [ ] Text extraction works
- [ ] Chunking works
- [ ] Embeddings are generated
- [ ] Embeddings are stored
- [ ] Vector search works
- [ ] Relevant context is retrieved
- [ ] LLM receives retrieved context
- [ ] Answer is grounded
- [ ] Sources are displayed
- [ ] Unknown questions are handled correctly

### Database

- [ ] Users persist
- [ ] Documents persist
- [ ] Chunks persist
- [ ] Conversations persist
- [ ] Messages persist

### Admin

- [ ] Upload documents
- [ ] View documents
- [ ] Delete documents
- [ ] Reprocess documents
- [ ] View processing status

### Frontend

- [ ] Responsive UI
- [ ] Loading states
- [ ] Error states
- [ ] Empty states
- [ ] Navigation
- [ ] Forms
- [ ] Chat interface

### Deployment

- [ ] Frontend deployed
- [ ] Backend deployed
- [ ] Database hosted
- [ ] Production environment variables configured
- [ ] End-to-end functionality verified

### GitHub

- [ ] Clean repository
- [ ] README complete
- [ ] `.gitignore` configured
- [ ] No secrets committed

---

# 46. Development Strategy

Implement the application incrementally.

DO NOT build everything simultaneously.

Recommended phases:

## Phase 1 — Project Setup

- Repository
- Frontend
- Backend
- Database
- Environment configuration

## Phase 2 — Authentication

- Signup
- Login
- Logout
- Protected routes
- Roles

## Phase 3 — Document Management

- Upload
- Storage
- Extraction
- Chunking
- Processing status

## Phase 4 — Vector Search

- Embeddings
- pgvector
- Similarity search
- Retrieval testing

## Phase 5 — RAG

- Prompt construction
- Context injection
- LLM generation
- Source tracking
- Unknown handling

## Phase 6 — Chat

- Chat UI
- Sessions
- History
- Follow-up context

## Phase 7 — Admin

- Dashboard
- Document CRUD
- Processing status
- Analytics

## Phase 8 — Testing

- RAG evaluation
- API testing
- UI testing
- Security testing

## Phase 9 — Deployment

- Vercel
- Render
- Supabase
- Production environment variables

## Phase 10 — Polish

Only now implement bonus features.

---

# 47. Critical Engineering Rules

1. Do not fake the RAG pipeline.
2. Do not hardcode answers.
3. Do not use an LLM without retrieval.
4. Do not store API keys in source code.
5. Do not expose service-role credentials to the frontend.
6. Do not allow students to access admin APIs.
7. Do not blindly trust LLM output.
8. Do not return unrelated retrieved chunks just to fill TOP_K.
9. Do not fabricate answers when retrieval fails.
10. Do not sacrifice backend correctness for UI polish.
11. Do not implement bonus features before the core pipeline works.
12. Every important feature must be testable.
13. The deployed application must work end-to-end.
14. The developer must be able to explain how retrieval works.
15. Keep architecture modular so embedding providers and LLM providers can be replaced.

---

# 48. Final Acceptance Test

A reviewer should be able to perform this sequence:

```text
1. Open deployed application.

2. Create student account.

3. Login.

4. Ask:
   "What are the admission requirements?"

5. Backend generates query embedding.

6. Vector database retrieves relevant chunks.

7. LLM generates grounded response.

8. UI displays answer.

9. UI displays source document and page.

10. Ask a question that is not present in the documents.

11. System responds that the information is unavailable.

12. Login as admin.

13. Upload a new college PDF.

14. Document changes to PROCESSING.

15. Document changes to READY.

16. Ask a question about the newly uploaded document.

17. System retrieves the newly indexed information.

18. Delete the document.

19. Verify its chunks are removed.

20. Verify the deleted document is no longer retrieved.
```

If any major step fails, the project is NOT complete.

---

# 49. Success Criteria

The final project should demonstrate all three layers:

```text
FULL-STACK ENGINEERING
        +
AI / RAG ENGINEERING
        +
DEPLOYMENT
```

The most important technical proof is:

```text
User Question
      ↓
Embedding
      ↓
Vector Search
      ↓
Relevant Document Chunks
      ↓
LLM Context
      ↓
Grounded Answer
      ↓
Source References
```

This pipeline must be real, persistent, testable, and visible through the application's behavior.

---

# 50. Build Philosophy

Prioritize:

```text
Correctness > Features
RAG Quality > UI Effects
Security > Convenience
Maintainability > Quick Hacks
Working Deployment > Local Demo
```

Build the smallest complete working system first.

Then improve it.

Do not claim a feature is implemented unless it actually works end-to-end.
