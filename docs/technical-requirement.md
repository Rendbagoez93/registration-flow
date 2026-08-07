# Technical Requirements

## 1. Technology Stack
*   **Backend Framework:** Python 3.11+, Django 5.x
*   **API Layer:** Django REST Framework (DRF)
*   **Database:** PostgreSQL (Ideal for handling concurrent booking transactions and enforcing quota constraints)
*   **Task Queue:** Celery + Redis (Crucial for handling async tasks like sending emails and syncing with Google Calendar without blocking the main thread)
*   **Document & Data Export Stack:**
    *   **PDF Generation:** `WeasyPrint` (Industry standard for rendering clean HTML/CSS templates into high-quality PDFs).
    *   **Excel Generation:** `openpyxl` (Lightweight and modular library for generating native `.xlsx` files without needing heavy dependencies like Pandas).
*   **Third-Party Services:** 
    *   Google Calendar API (`google-api-python-client`, `google-auth-oauthlib`)
    *   Email Provider (e.g., SendGrid or AWS SES)

## 2. Architecture & Modularity
To ensure a clean and scalable codebase, the Django project will be split into isolated, purpose-built apps:
*   `accounts`: Handles Custom User models (Owner vs. Customer), authentication, and profiles.
*   `businesses`: Manages business profiles, staff, and the blogging engine.
*   `forms`: Core logic for dynamic form generation, fields, and validations.
*   `bookings`: Handles registration logic, quota decrements, and scheduling constraints.
*   `exports`: Dedicated module containing utility functions and endpoints strictly for rendering and serving Excel sheets and PDF files.
*   `integrations`: Isolated logic for third-party APIs (Google Calendar Auth, Webhooks).

## 3. Concurrency & Quota Safety
*   **Database Locks:** Use PostgreSQL `select_for_update()` during the booking transaction to prevent race conditions (double-booking when two users submit a form at the exact same millisecond).

## 4. File Export Strategies
*   **PDF Confirmation (Customers):** Endpoints will populate a pre-designed Django HTML template with booking context, style it with CSS, and convert it to a PDF using `WeasyPrint` entirely in-memory. The file is streamed back via `FileResponse`.
*   **Excel Registrant List (Owners):** Generating the file will utilize an in-memory `Workbook` using `openpyxl`. The API will query the database for a specific event's participants, write the headers and rows dynamically, and return it with the `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` content type.

## 5. Security
*   **Authentication:** JWT (JSON Web Tokens) for stateless API authentication.
*   **Permissions:** Strict Role-Based Access Control (RBAC). A business owner can only read/write/export data belonging to their own `Business` instance. Customers can only view and download PDFs of their own confirmed bookings.
*   **OAuth2 Security:** Secure storage of Google refresh tokens in the database (encrypted).