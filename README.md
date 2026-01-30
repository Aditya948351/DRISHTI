# Drishti Platform

**AI-Driven Government Complaint & Case Management System**

> [!IMPORTANT]
> **[👉 Click here for Instructions on How to Run the Project](How_to_Run.md)**

## Overview
Drishti is a comprehensive platform designed to bridge the gap between citizens and administration. It leverages AI to categorize, track, and resolve public grievances efficiently.

## Problem Statement
Traditional grievance systems (like CPGRAMS) often struggle with manual processing bottlenecks, lack of real-time updates, and inefficient complaint routing. **DRISHTI** solves these issues by integrating **Artificial Intelligence** to automate classification and prioritization, ensuring faster resolution times, complete transparency for citizens, and enhanced accountability for government officers.

## Features
- **AI-Powered Categorization**: Automatically routes complaints to the right department.
- **Real-time Tracking**: Citizens can track the status of their complaints.
- **Multi-Role Dashboards**: Dedicated interfaces for Citizens, Officers, and Admins.
- **Analytics**: Insightful reports for administration to improve service delivery.

## 🧠 System Architecture: How It Works

### 1️⃣ For Non-Technical Users (The "What" & "Why")
Think of **Drishti** as a smart digital assistant for the government.
- **The "Brain" (Backend):** Just like a helpful receptionist, our system takes your complaint, understands what it's about, and immediately sends it to the correct department. You don't need to know *who* to talk to; the system knows.
- **The "Digital Vault" (Database):** We replaced dusty physical files with a secure, cloud-based filing cabinet. Every complaint is saved instantly, cannot be lost, and can be pulled up by an officer on their phone or laptop in seconds.
- **The "Smart Reader" (AI):** Instead of a human reading thousands of letters, our AI reads your complaint instantly. If you write "broken street light," it knows that belongs to the "Electricity Department" and routes it there automatically.

### 2️⃣ For Technical Users (The "How")
Drishti is built on a robust, scalable architecture focusing on security and automation.
- **Backend Kernel:** Powered by **Django 5.0+**, utilizing the **MVT (Model-View-Template)** architecture for rapid development and clean separation of concerns.
    - **Authentication:** Custom User Model extending `AbstractUser` to handle multiple roles (Citizen, Admin, Officer) securely.
    - **API Integration:** Connects with **OpenRouter/Gemini LLMs** for NLP tasks (complaint summarization and categorization).
- **Database Layer:**
    - **Primary DB:** Relational database management using **MySQL** (release) or **SQLite** (dev default) for structured storage. Utilizes **dj-database-url** for environment-based configuration and seamless deployments (e.g., Railway/Render).
    - **ORM Security:** Django ORM abstracts SQL queries, preventing typical injection vulnerabilities.
- **Media Management:** Deep integration with **Cloudinary** for scalable, optimized storage of image/video evidence.
- **Security**: Implements Django's built-in session security, CSRF protection, and environment variable management via `python-dotenv`.

## 🔐 Backend Workflows & Role Management

Drishti controls access using a sophisticated Role-Based Access Control (RBAC) system.

### 1. Authentication & Routing Logic
When a user logs in, the backend (`accounts/views.py`) dynamically routes them to their specific dashboard based on their assigned role.
- **Login Process**:
  1. User submits credentials.
  2. `CustomLoginView` authenticates the user.
  3. The `get_success_url()` method checks `user.role` (e.g., `'citizen'`, `'officer'`, `'dept_admin'`).
  4. User is redirected to their dedicated workspace (e.g., `/dashboard/citizen/` or `/dashboard/officer/`).

### 2. User Roles Explained
- **👤 Citizen (`citizen`)**:
  - **Capabilities**: Can file new complaints, view valid schemes, and track the status of their reported issues.
  - **Backend Logic**: Restricted to viewing only their own data.
- **👮 Local Officer (`officer`)**:
  - **Capabilities**: Field officers who update the status of assigned complaints (e.g., "In Progress", "Resolved") and upload proof of work.
  - **Backend Logic**: Filtered view showing only complaints assigned to their specific department and district.
- **🏢 Department Admin (`dept_admin`)**:
  - **Capabilities**: Oversees all officers within a specific department (e.g., Health, Police). Can re-assign complaints and view department-wide analytics.
- **🏛️ Higher Authorities (`city_admin` / `super_admin`)**:
  - **Capabilities**: Top-level view of the entire city or state. Access to global analytics, AI usage stats, and critical alerts.

## Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Vanilla), JavaScript
- **Database**: SQLite (Development)
