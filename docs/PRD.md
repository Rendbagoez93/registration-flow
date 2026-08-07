# Product Requirements Document (PRD)
**Product Name:** [App Name] (Centralized Booking & Registration Platform)

## 1. Overview
A centralized SaaS platform that allows various business types (clinics, salons, event organizers) to create custom registration forms and manage bookings. It acts as an enhanced, business-focused alternative to Google Forms by introducing domain-specific features like quota management, automated calendar syncing, and a built-in blogging engine.

## 2. Target Audience
*   **Business Owners (B2B):** Professionals needing to manage appointments, sell tickets, or accept registrations without building a custom website.
*   **End-Users (B2C):** Customers looking for a seamless, centralized way to book services or register for events across different businesses.

## 3. Core Features

### 3.1. Dynamic Registration Forms
*   Business owners can create customized forms with various input types (text, dropdowns, dates, checkboxes).
*   Shareable public links for each form/service.

### 3.2. Quota & Availability Management
*   Set maximum capacities for events (e.g., 50 tickets) or time slots (e.g., 1 patient per 30 mins).
*   Automatic disabling of forms/slots when the quota is reached.

### 3.3. Google Calendar Integration
*   OAuth2 integration for Business Owners to connect their Google accounts.
*   Automatic calendar event creation when a customer registers/books.
*   Two-way sync: If an event is cancelled on the platform, it removes it from Google Calendar.

### 3.4. Export & Download Capabilities
*   **User/Customer Export (PDF):** After a successful registration or booking, customers can export and download their confirmation form, receipt, or ticket as a polished PDF document.
*   **Business Owner Export (Excel):** Business owners can export the list of registered attendees or booked clients for any given event or form into an Excel (.xlsx) file for external processing, offline check-ins, or reporting.

### 3.5. Blogging Engine
*   Business profiles include a blog section.
*   Owners can publish updates, promotional content, or announcements directly to their business page.

### 3.6. Centralized Dashboard
*   **Owner View:** Manage forms, view upcoming bookings, adjust quotas, write blog posts, and export attendee lists.
*   **Customer View:** View past and upcoming appointments/registrations across all businesses, and download PDF confirmations.

## 4. Success Metrics
*   Number of active businesses onboarded.
*   Volume of successful bookings/registrations processed daily.
*   Zero double-bookings (measuring the accuracy of the quota system).
