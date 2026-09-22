# AI Smart Contacts Manager — Architecture

## 1. Architecture Overview

AI Smart Contacts Manager follows a modular full-stack architecture.

The system is divided into:

- Frontend Layer
- API Layer
- Business Logic Layer
- Data Access Layer
- Database Layer
- AI Layer
- Infrastructure Layer

The architecture is designed so that AI capabilities can be added without
changing the core contact management system.

---

## 2. High-Level Architecture

### Phase 1 — Core Application

User
  ↓
React Frontend
  ↓
REST API
  ↓
Node.js + Express
  ↓
Service Layer
  ↓
PostgreSQL


### Phase 2 — AI Integration

User
  ↓
React Frontend
  ↓
Node.js + Express
  ↓
AI Service
  ↓
OpenAI API
  ↓
Embeddings
  ↓
pgvector
  ↓
Relevant Contact Data
  ↓
RAG
  ↓
AI Response


### Phase 3 — Production

User
  ↓
React
  ↓
Backend API
  ↓
Services
  ├── PostgreSQL
  ├── pgvector
  └── AI Service
          ↓
      OpenAI API

Infrastructure:
- Docker
- AWS
- Logging
- Monitoring


4. API Layer
Technology

Node.js + Express.js

Responsibilities
Receive HTTP requests
Route requests
Authenticate users
Validate requests
Call business services
Return API responses
Handle errors


examples:

POST /api/auth/register
POST /api/auth/login
GET    /api/contacts
POST   /api/contacts
GET    /api/contacts/:id
PUT    /api/contacts/:id
DELETE /api/contacts/:id

6.

backend/
└── src/
    ├── config/
    ├── controllers/
    ├── db/
    ├── middleware/
    ├── routes/
    ├── services/
    ├── utils/
    └── app.js

Routes

Defines API endpoints.

Controllers

Handles HTTP requests and responses.

Services

Contains business logic.

Middleware

Handles:

Authentication
Authorization
Validation
Error handling

DB

Handles database connection and database-related operations.

Config

Handles application configuration and environment variables.

Utils

Contains reusable helper functions.

app.js

Initializes Express and connects the different application components.

6. Database Layer
Technology

PostgreSQL

Main entities:

Users
  |
  | 1:N
  |
Contacts

One user can have multiple contacts.

The database is responsible for:

Data persistence
Relationships
Constraints
Indexes
Data integrity

7. AI Layer

AI functionality will be isolated from the core contact management logic.

Components
OpenAI API
Embedding generation
pgvector
Retrieval
RAG pipeline

Example flow:

User Query
↓
Query Processing
↓
Embedding
↓
Vector Search
↓
Relevant Contacts
↓
Context Construction
↓
OpenAI
↓
Response

8. RAG Architecture

RAG stands for Retrieval-Augmented Generation.

The system will:

Receive a natural-language query.
Convert the query into an embedding.
Search relevant contact information using pgvector.
Retrieve relevant context.
Send the context to the AI model.
Generate the final response.

Example:

"Find my college friends in Bangalore"

        ↓

Query Embedding

        ↓

pgvector Semantic Search

        ↓

Relevant Contacts

        ↓

Context

        ↓

OpenAI

        ↓

Natural Language Response
9. Security Architecture

The application will use:

JWT authentication
Password hashing
Protected routes
Input validation
Authorization checks
Environment variables for secrets
Database constraints

Users must only be able to access their own contacts.

10. Scalability Considerations

The architecture should support future scaling through:

Modular backend services
Database indexing
Pagination
Caching
Docker
AWS deployment
Independent AI service
Logging and monitoring
11. Request Flow

For a normal contact request:

Client
  ↓
React
  ↓
HTTP Request
  ↓
Express Route
  ↓
Authentication Middleware
  ↓
Controller
  ↓
Service
  ↓
PostgreSQL
  ↓
Service
  ↓
Controller
  ↓
HTTP Response
  ↓
React

For an AI request:

Client
  ↓
React
  ↓
Express
  ↓
Authentication
  ↓
AI Controller
  ↓
AI Service
  ↓
Embedding / Retrieval
  ↓
pgvector
  ↓
Context
  ↓
OpenAI
  ↓
AI Response
  ↓
React
12. Architecture Principles

The project will follow:

Separation of concerns
Modular design
Single responsibility
Secure-by-default approach
Reusable services
Clear API boundaries
Testable components
Scalable design
13. Deployment Architecture

Production deployment will eventually use:

User
 ↓
Frontend
 ↓
AWS
 ↓
Backend API
 ↓
PostgreSQL
 ↓
pgvector

Backend
 ↓
OpenAI API

Docker will be used to containerize application components.