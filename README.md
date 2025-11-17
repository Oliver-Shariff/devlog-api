# Devlog API

Devlog API is a backend system designed for managing user generated writing, providing structured organization, AI assisted summarization, and analytics insights. It demonstrates end to end backend architecture including authentication, relational modeling, asynchronous processing, and data aggregation.

## Overview

The system delivers a complete backend for personal writing workflows. It supports secure user management, entry creation, tagging, activity analytics, and asynchronous AI generated summaries. All components are built with production grade patterns including layered architecture, service separation, and strong data modeling.

## Key Capabilities

### Authentication and User Management

* JWT based authentication flow
* Password hashing and secure credential storage
* Protected routes through dependency based access control

### Structured Writing Entries

* Creation, retrieval, editing, and deletion of entries
* Pagination and filtering
* Automatic timestamping and last edit tracking

### Tagging System

* User level tag creation with uniqueness enforcement
* Many to many relationships between tags and entries
* Fast lookup of entries by tag

### AI Assisted Summaries

* Asynchronous background task that generates concise summaries using an external AI model
* Validation layer for length requirements and ownership checks
* Summary storage directly on the entry record

### Analytics and Activity Insights

* Aggregation of total entries and total tags
* Entry distribution per tag
* Entry frequency by day for recent activity
* Efficient SQL queries powered by SQLAlchemy Core and ORM

## Architecture and Design

The application follows a modular design:

* **Routers** define HTTP interfaces
* **CRUD modules** handle database operations
* **Models** use SQLAlchemy ORM with normalized relationships
* **Schemas** validate input and output with Pydantic
* **Security module** manages authentication flow and token validation
* **AI module** integrates with an external API and schedules background tasks
* **Analytics module** executes optimized SQL aggregation queries

This separation supports maintainability, testing, and extension of new features.

## Technologies

* FastAPI
* SQLAlchemy ORM and Core
* PostgreSQL or any SQLAlchemy supported database
* JWT authentication
* Pydantic models
* OpenAI API for summarization
* Background task processing via FastAPI

## Environment Configuration

The service uses environment based configuration through `.env` variables:

```
SQLALCHEMY_DATABASE_URL
JWT_SECRET
JWT_ALG
ACCESS_TOKEN_EXPIRE_MINUTES
OPENAI_SUMMARIZE_KEY
```

## Status at This Stage

The system currently includes:

* Complete authentication flow
* CRUD operations for users, entries, and tags
* Asynchronous summarization pipeline
* Data analytics endpoints
* Fully defined relational models and query patterns
* Modular architecture designed for scale and maintainability

---