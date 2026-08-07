# API Implementation Strategy

## 1. Overview
The API will follow RESTful principles using Django REST Framework. Responses will be standardized (JSON), utilizing DRF serializers for clean data validation.

## 2. Authentication & Authorization
*   `POST /api/auth/register/` - Register a new user (Customer or Owner).
*   `POST /api/auth/login/` - Returns JWT access and refresh tokens.
*   `GET /api/auth/google/` - Initiates Google Calendar OAuth2 flow.
*   `GET /api/auth/google/callback/` - Handles the OAuth2 callback and stores tokens.

## 3. Core Endpoints

### 3.1. Businesses & Blogs
*   `GET /api/businesses/` - List businesses (public).
*   `POST /api/businesses/` - Create a business profile (Owner only).
*   `GET /api/businesses/{id}/posts/` - List blog posts for a business.
*   `POST /api/businesses/{id}/posts/` - Create a new blog post (Owner only).

### 3.2. Forms & Services
*   `GET /api/forms/` - List available forms/services for a business.
*   `POST /api/forms/` - Create a new form schema with quotas (Owner only).
    *   *Payload Example:* Includes form title, field definitions (JSON), and quota limits.
*   `GET /api/forms/{id}/` - Retrieve form details and available slots/quota.

### 3.3. Bookings & Registrations
*   `POST /api/bookings/` - Submit a registration.
    *   *Logic:* Validates form data against form schema -> Checks quota with DB lock -> Creates booking -> Triggers Celery task for Google Calendar sync -> Sends confirmation email.
*   `GET /api/bookings/` - List user's bookings (Customer) or business's bookings (Owner).
*   `PATCH /api/bookings/{id}/` - Cancel or update a booking. (Triggers Calendar delete event).

## 4. Async Task Implementation (Celery)
*   `sync_to_google_calendar(booking_id)`: Fetches booking details, formats into a Google Event payload, retrieves the Owner's refresh token, and pushes to the Google API.
*   `send_booking_confirmation(booking_id)`: Generates and sends a transactional email to the user.