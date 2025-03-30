# 🦆 Quack - Project Technical Report

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Backend Architecture](#backend-architecture)
   - [Technology Stack](#backend-technology-stack)
   - [Application Structure](#backend-application-structure)
   - [Database Design](#database-design)
   - [API Endpoints](#api-endpoints)
   - [Authentication](#authentication)
4. [Frontend Architecture](#frontend-architecture)
   - [Technology Stack](#frontend-technology-stack)
   - [Application Structure](#frontend-application-structure)
   - [State Management](#state-management)
   - [Routing](#routing)
   - [User Interface](#user-interface)
5. [Integration Points](#integration-points)
6. [Deployment Architecture](#deployment-architecture)
7. [Security Considerations](#security-considerations)

## Project Overview

Quack is a comprehensive platform for home servicing and solutions that connects customers with professional service providers. The application facilitates the entire service lifecycle, from customer request submission to service completion and review. The platform includes role-based access for customers, service professionals, and administrators, with appropriate workflows for each user type.

## System Architecture

The Quack application follows a modern client-server architecture with distinct separation between:

1. **Frontend**: A Vue.js-based single-page application
2. **Backend**: A Flask-based RESTful API service
3. **Database**: SQLite (development) / PostgreSQL (production)
4. **Background Tasks**: Celery with Redis for asynchronous operations

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│                 │     │                  │     │                 │
│    Frontend     │━━━━▶│ Backend API      │━━━━▶│    Database     │
│    (Vue.js)     │◀━━━━│ (Flask/Flask-RESTx)  │◀━━━━│  (PostgreSQL)  │
│                 │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │   ▲
                               ▼   │
                        ┌─────────────────┐     ┌─────────────────┐
                        │                 │     │                 │
                        │  Celery Worker  │━━━━▶│  Redis/RabbitMQ │
                        │                 │◀━━━━│                 │
                        └─────────────────┘     └─────────────────┘
```

The system employs a microservices-inspired architecture, with the frontend and backend as separate services that communicate via RESTful APIs.

## Backend Architecture

### Backend Technology Stack

- **Language**: Python 3.10+
- **Web Framework**: Flask, Flask-RESTx
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Database Migrations**: Flask-Migrate (Alembic)
- **Authentication**: JWT with Flask-JWT-Extended
- **API Documentation**: Swagger UI via Flask-RESTx
- **Background Tasks**: Celery
- **Message Broker**: Redis
- **Email Service**: Flask-Mail

### Backend Application Structure

The backend follows a modular structure with clear separation of concerns:

```
backend/
├── app/                    # Main application package
│   ├── __init__.py         # App initialization and factory pattern
│   ├── config.py           # Configuration classes
│   ├── database.py         # Database setup and connections
│   ├── models.py           # SQLAlchemy data models
│   ├── celery_utils.py     # Celery configuration
│   ├── api/                # API package (nested resources)
│   ├── routes/             # Route definitions by role
│   │   ├── admin.py        # Admin-specific endpoints
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── customer.py     # Customer-specific endpoints
│   │   ├── professional.py # Professional-specific endpoints
│   │   └── service.py      # Service-related endpoints
│   ├── tasks/              # Background task definitions
│   │   └── email_tasks.py  # Email sending tasks
│   ├── utils/              # Utility functions
│   │   └── email.py        # Email helpers
│   └── static/             # Static files (uploads, etc.)
│       └── uploads/        # User uploaded content
│           ├── profiles/   # Profile images
│           └── documents/  # Document uploads
├── migrations/             # Database migration files
├── instance/               # Instance-specific data (database files)
├── manage.py               # Management script
├── seed_data.py            # Database seeding script
└── requirements.txt        # Python dependencies
```

The backend follows the Flask factory pattern, which allows for different configurations for development, testing, and production environments.

### Database Design

The database schema consists of the following key entities:

#### User
- Core entity that represents either a customer, professional, or admin
- Contains authentication details, profile information, and role associations
- Fields include username, password (hashed), status, contact details, and more

#### Role
- Defines user roles (admin, customer, professional)
- Many-to-many relationship with User via UserRoles

#### Service
- Represents a service offering available on the platform
- Contains name, price, time required, and description

#### ServiceRequest
- Tracks a service request from creation to completion
- Links customers, professionals, and services
- Contains status information, dates, location data, and request details

#### Document
- Stores verification documents for professional users
- Contains document type, file path, and verification status

**Entity Relationship Diagram**:

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│      User       │       │    UserRoles    │       │      Role       │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id              │◀─────▶│ user_id         │◀─────▶│ id              │
│ username        │       │ role_id         │       │ name            │
│ password        │       └─────────────────┘       └─────────────────┘
│ name            │
│ email           │
│ status          │
│ blocked         │
│ ...             │
└─────────────────┘
       ▲  ▲
       │  │
       │  │
┌──────┘  └────────┐
│                  │
│                  │
▼                  ▼
┌─────────────────┐       ┌─────────────────┐
│  ServiceRequest │       │    Document     │
├─────────────────┤       ├─────────────────┤
│ id              │       │ id              │
│ service_id      │       │ user_id         │
│ customer_id     │       │ document_type   │
│ professional_id │       │ file_path       │
│ service_status  │       │ verified        │
│ ...             │       │ ...             │
└─────────────────┘       └─────────────────┘
        │
        │
        ▼
┌─────────────────┐
│     Service     │
├─────────────────┤
│ id              │
│ name            │
│ price           │
│ time_required   │
│ description     │
└─────────────────┘
```

### API Endpoints

The backend exposes several RESTful API endpoints organized by user role:

#### Authentication Endpoints
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Authenticate user and return tokens
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Log out user (client-side token removal)
- `GET /auth/me` - Get current user information

#### Admin Endpoints
- `GET /admin/professionals` - List all professionals
- `GET /admin/customers` - List all customers
- `PATCH /admin/professionals/{id}/approve` - Approve a professional
- `PATCH /admin/professionals/{id}/reject` - Reject a professional
- `GET /admin/services` - List all services
- `POST /admin/services` - Create a new service
- `PUT /admin/services/{id}` - Update a service
- `DELETE /admin/services/{id}` - Delete a service
- `GET /admin/documents` - List all verification documents
- `PATCH /admin/documents/{id}/verify` - Verify a document
- `PATCH /admin/documents/{id}/reject` - Reject a document

#### Customer Endpoints
- `GET /customer/services` - List available services
- `POST /customer/requests` - Create a service request
- `GET /customer/requests` - List customer's service requests
- `GET /customer/requests/{id}` - Get details of a service request
- `PUT /customer/profile` - Update customer profile

#### Professional Endpoints
- `GET /professional/requests` - List service requests assigned to professional
- `PATCH /professional/requests/{id}/accept` - Accept a service request
- `PATCH /professional/requests/{id}/complete` - Mark a service request as complete
- `PATCH /professional/requests/{id}/reject` - Reject a service request
- `PUT /professional/profile` - Update professional profile
- `POST /professional/documents` - Upload verification documents

### Authentication

The system uses JSON Web Tokens (JWT) for authentication with the following components:

- **Access Tokens**: Short-lived tokens (1 hour) for API access
- **Refresh Tokens**: Long-lived tokens (7 days) to obtain new access tokens
- **Role-Based Access Control**: Routes are protected based on user roles
- **Token Storage**: Client-side storage in localStorage
- **Custom Decorators**: `admin_required()`, `professional_required()`, and `customer_required()` for route protection

## Frontend Architecture

### Frontend Technology Stack

- **Framework**: Vue.js 3 with Composition API
- **Build Tool**: Vite
- **Router**: Vue Router 4
- **State Management**: Pinia
- **HTTP Client**: Axios
- **CSS Framework**: Bootstrap 5 with custom neo-brutalist styling
- **Icons**: Custom icon components

### Frontend Application Structure

The frontend follows a component-based architecture with a clear organization:

```
frontend/
├── public/                # Static files
├── src/                   # Source code
│   ├── assets/            # Images, fonts, etc.
│   ├── components/        # Reusable components
│   │   ├── ui/            # UI components (buttons, icons, etc.)
│   │   ├── forms/         # Form components
│   │   └── ...            # Feature-specific components
│   ├── router/            # Vue Router configuration
│   │   └── index.js       # Route definitions
│   ├── stores/            # Pinia state stores
│   │   ├── auth.js        # Authentication state
│   │   └── ...            # Other state modules
│   ├── services/          # API and utility services
│   │   ├── api/           # API clients
│   │   └── toastService.js # Notification service
│   ├── views/             # Page components
│   │   ├── admin/         # Admin views
│   │   ├── auth/          # Authentication views
│   │   ├── customer/      # Customer views
│   │   ├── professional/  # Professional views
│   │   └── HomeView.vue   # Home page
│   ├── App.vue            # Root component
│   └── main.js            # Application entry point
├── index.html             # HTML entry point
└── package.json           # Dependencies and scripts
```

### State Management

The application uses Pinia for state management with the following main stores:

1. **AuthStore**: Manages authentication state
   - User information
   - JWT tokens
   - Login/logout logic
   - Role checking

2. **Other Domain Stores**:
   - ServiceStore: Manages services data
   - RequestStore: Manages service requests
   - ProfileStore: Manages user profile data

The stores implement persistence with localStorage for maintaining session state across page refreshes.

### Routing

Vue Router handles navigation with role-based access control:

1. **Public Routes**:
   - Home
   - Login
   - Register
   - Blocked/Pending/Disapproved notification screens

2. **Protected Routes**:
   - Admin dashboard and sub-routes
   - Professional dashboard and sub-routes
   - Customer dashboard and sub-routes

The router implements navigation guards to:
- Redirect unauthenticated users to login
- Redirect users without proper roles to the home page
- Handle special cases like blocked users or pending professionals

### User Interface

The UI follows a neo-brutalist design approach with:

- Bold colors and contrasts
- Strong borders and shadows
- Playful typography
- Clean, functional layouts

Key UI components include:
- NeoButton: Customized button component
- NeoIcon: Icon system with consistent styling
- Form components with validation
- Responsive layouts using Bootstrap 5 grid

## Integration Points

The frontend and backend communicate primarily through RESTful API calls:

1. **Authentication Flow**:
   - Login/registration requests return JWT tokens
   - Frontend stores tokens in localStorage
   - Tokens are sent with subsequent requests in Authorization header

2. **API Communication**:
   - Axios interceptors handle token inclusion in requests
   - Error handling for common response codes (401, 403, etc.)
   - Automatic refresh of expired tokens

3. **File Uploads**:
   - Multipart form data for document and profile image uploads
   - Direct file serving for images and documents

## Deployment Architecture

The application is designed for modern deployment pipelines:

**Development Environment**:
- Frontend: Vite dev server on port 5173
- Backend: Flask development server on port 5000
- Database: SQLite file-based database
- CORS configured for cross-domain communication

**Production Environment**:
- Frontend: Static files served by Nginx or CDN
- Backend: Gunicorn/uWSGI with Flask behind Nginx
- Database: PostgreSQL
- Background workers: Celery workers with Redis
- Object storage: For user-uploaded files

## Security Considerations

The application implements several security measures:

1. **Authentication**:
   - Password hashing with Werkzeug's generate_password_hash
   - JWT with appropriate expiration times
   - Protected routes on both frontend and backend

2. **File Security**:
   - Secure filename generation
   - Path traversal prevention
   - Filetype validation
   - Size limitations

3. **API Security**:
   - CORS configuration
   - Rate limiting capabilities
   - Input validation

4. **User Data Protection**:
   - Professional approval workflow
   - Document verification process
   - User blocking capabilities

5. **Error Handling**:
   - Structured error responses
   - Minimal information leakage
   - Consistent error format across API

This architecture provides a secure, scalable, and maintainable foundation for the Quack home services platform. 