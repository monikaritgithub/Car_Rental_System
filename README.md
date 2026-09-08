# Smriti Car Rental System

An automated, full-stack car rental management platform built with Python, Flask, and SQLite. This project demonstrates object-oriented architecture, design patterns, and software evolution principles.

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Features](#2-system-features)
3. [Technology Stack](#3-technology-stack)
4. [Installation & Configuration Guide](#4-installation--configuration-guide)
5. [Operating the System](#5-operating-the-system)
6. [Project Structure](#6-project-structure)
7. [Design and Architecture](#7-design-and-architecture)
8. [Recommendation Engine](#8-recommendation-engine)
9. [Coding Standards](#9-coding-standards)
10. [Testing](#10-testing)
11. [Software Evolution](#11-software-evolution)
12. [Known Issues](#12-known-issues)
13. [License](#13-license)
14. [Credits](#14-credits)

---

## 1. Introduction

Legacy car rental systems often rely on manual processes, leading to inefficiencies and errors. The Smriti Car Rental System addresses this by automating the vehicle rental lifecycle. The application digitizes user management, fleet tracking, and reservation processing to reduce administrative overhead and improve reliability.

### Core Objectives

| Objective | Implementation |
|---|---|
| Automate the rental process | End-to-end digital booking from search to payment |
| Reduce paperwork errors | Database-driven validation and status tracking |
| Differentiate user roles | Separate Customer and Admin portals with distinct privileges |
| Enforce business rules | Service layer validates dates, availability, and rental periods |
| Provide business insights | Admin report dashboard with revenue and fleet analytics |

Built using an Object-Oriented MVC Architecture with Python, Flask, and SQLite, the platform provides two separate interfaces:

1. **Customer Portal (Port 5000):** A platform for users to browse the fleet, receive vehicle recommendations, and book rentals.
2. **Admin Dashboard (Port 5001):** A management suite for staff to oversee fleet availability, approve or reject bookings, manage additional charges, and track revenue.

---

## 2. System Features

### Customer Interface (Port 5000)

| Feature | Description |
|---|---|
| Homepage | Displays live availability statistics and fleet highlights. |
| Fleet Browsing | Filter options by category (Sedan, SUV, Luxury, Truck, Economy). |
| Car Details | Specifications, mileage, pricing breakdown, and one-click booking access. |
| Secure Booking | Date validation, rental period constraint checks, and mock payment checkout. |
| My Bookings | Interface to track, view, and cancel pending reservations. |
| Recommendation Engine | Suggests vehicles based on budget, purpose, and passenger count. |
| Mock Payment Profiles | Random mock card and expiry assigned on registration for testing. |

### Admin Interface (Port 5001)

| Feature | Description |
|---|---|
| Dashboard | Real-time KPIs: pending bookings, fleet availability, and total revenue. |
| Fleet Management | Full CRUD operations for vehicles, including pricing, limits, and photos. |
| Booking Approval | Review pending bookings, approve (marks car unavailable) or reject (issues refund). |
| Booking Cancellation | Allows cancellation of approved bookings, releasing the car and issuing a refund. |
| Additional Charges | Manage per-car extra fees (e.g., GPS, Insurance) as per-day or one-time charges. |
| Payments Overview | View system-wide transactions and payment statuses. |
| Reporting | Revenue totals, fleet utilization percentages, and booking status breakdowns. |

---

## 3. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend Framework | Python 3.x, Flask 3.0.3 | Web server and routing |
| ORM / Database | SQLAlchemy 2.0, SQLite | Persistent data storage |
| Authentication | Werkzeug (PBKDF2-SHA256) | Secure password hashing |
| Frontend | HTML5, Vanilla CSS, Jinja2 | Templating and UI rendering |
| Typography | Montserrat (Google Fonts) | Primary application font |
| Forms | Flask-WTF, WTForms | Form handling and CSRF protection |
| Session Management | Flask-Login 0.6.3 | User session management |
| Testing | Pytest 8.3.2, pytest-flask 1.3.0 | Automated unit and route testing |
| Environment Config | python-dotenv 1.0.1 | Environment variable management |

---

## 4. Installation & Configuration Guide

### 4.1 Prerequisites

Ensure you have the following installed:
- Python 3.10 or higher
- pip
- Git

Verify your Python installation:
```bash
python --version
```

### 4.2 Windows Setup

1. Clone the repository.
2. Open Command Prompt or PowerShell in the project root directory.
3. Run the startup script:

```cmd
run.bat
```

The script will automatically:
- Create a Python virtual environment (`.venv/`)
- Install dependencies from `requirements.txt`
- Seed the database with demo cars, customers, and an admin account
- Launch both servers

### 4.3 Linux / macOS Setup

1. Clone the repository.
2. Open a terminal in the project root directory.
3. Make the script executable and run it:

```bash
chmod +x run.sh
./run.sh
```

### 4.4 Manual Setup

If you prefer to configure the environment manually:

**Step 1: Clone the repository**
```bash
git clone <repository-url>
cd Car_Rental_System
```

**Step 2: Create and activate a virtual environment**
```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Seed the database**
```bash
python scripts/seed_data.py
```
This populates the `car_rental.db` SQLite file with initial testing data.

**Step 5: Start the applications**
In terminal 1:
```bash
python customer_server.py
```
In terminal 2:
```bash
python admin_server.py
```

Access the Customer Portal at `http://127.0.0.1:5000` and the Admin Portal at `http://127.0.0.1:5001`.

---

## 5. Operating the System

### 5.1 Demo Credentials

| Role | Email | Password | Notes |
|---|---|---|---|
| Admin | admin@smriticars.com | admin123 | Full management access |
| Customer | james@example.com | customer123 | Contains existing bookings |
| Customer | aiko@example.com | customer123 | Clean account for testing |

### 5.2 Customer Workflow

1. **Register:** Navigate to `http://127.0.0.1:5000/register`. Complete the form to create an account. A mock payment card is automatically assigned.
2. **Browse the Fleet:** Click "Browse Cars" on the homepage. Filter results by category. Only cars marked as available are displayed.
3. **View Car Details:** Select any car to review specifications, daily rates, and additional charges.
4. **Get Recommendation:** Use the "Find My Car" feature. Enter passenger count, budget, purpose, and rental duration to receive algorithmically matched vehicles.
5. **Book a Car:** Click "Book Now" from a car's detail page. Select start and end dates to calculate the total fee.
6. **Checkout:** Enter payment details (any 16-digit number works in demo mode). Confirming the booking sets its status to PENDING.
7. **Track Bookings:** View the status of all reservations under "My Bookings".
8. **Cancel a Booking:** PENDING bookings can be cancelled, which automatically issues a refund.

### 5.3 Admin Workflow

1. **Login:** Access `http://127.0.0.1:5001` and log in with admin credentials.
2. **Dashboard:** View key metrics including pending bookings, fleet size, availability, and revenue.
3. **Manage Fleet:** Use "Fleet Management" to add, edit, or delete vehicles. Cars with active bookings cannot be deleted.
4. **Manage Bookings:** Navigate to "Booking Requests" to review PENDING bookings. Approving a booking marks the car as unavailable. Rejecting a booking triggers a refund.
5. **Additional Charges:** Manage per-day or one-time fees for individual cars from the "Extras" section.
6. **Generate Report:** Access the "System Report" for business analytics summaries.

---

## 6. Project Structure

```text
Car_Rental_System/
├── app/
│   ├── admin_app/             # Admin portal blueprint and templates
│   ├── customer_app/          # Customer portal blueprint and templates
│   ├── models/                # SQLAlchemy ORM entity classes
│   └── services/              # Business logic layer
├── config/                    # Environment configurations
├── scripts/                   # Database seeding utilities
├── tests/                     # Pytest test suite
├── images/                    # Vehicle photograph files
├── admin_server.py            # Admin app entry point
├── customer_server.py         # Customer app entry point
├── database.py                # Shared SQLAlchemy instance
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 7. Design and Architecture

### 7.1 Architectural Overview

The system uses a layered Model-View-Controller (MVC) architecture implemented with Flask's Application Factory pattern. This isolates the admin portal from the customer-facing application.

```text
┌─────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                   │
│          Jinja2 Templates (HTML + CSS)                      │
│    Customer Portal (Port 5000) | Admin Portal (Port 5001)   │
└──────────────────────────┬──────────────────────────────────┘
                           │  HTTP Requests / Responses
┌──────────────────────────▼──────────────────────────────────┐
│                       CONTROLLER LAYER                      │
│              Flask Blueprints (routes.py files)             │
└──────────────────────────┬──────────────────────────────────┘
                           │  Function calls
┌──────────────────────────▼──────────────────────────────────┐
│                       SERVICE LAYER                         │
│    booking_engine | car_service | customer_service          │
│    payment_service | recommendation_service | report_service│
└──────────────────────────┬──────────────────────────────────┘
                           │  ORM queries
┌──────────────────────────▼──────────────────────────────────┐
│                        MODEL LAYER                          │
│     SQLAlchemy ORM Classes: Car, Booking, Customer,         │
│     Admin, Payment, AdditionalCharge                        │
└──────────────────────────┬──────────────────────────────────┘
                           │  SQL queries
┌──────────────────────────▼──────────────────────────────────┐
│                       DATABASE LAYER                        │
│                  SQLite (car_rental.db)                     │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Core Design Patterns

- **Application Factory Pattern:** `create_customer_app()` and `create_admin_app()` are independent factories that accept a configuration class and return a configured application instance.
- **Singleton Pattern:** A single SQLAlchemy instance (`db`) in `database.py` is shared across both Flask applications.
- **Service Layer Pattern:** Complex operations are delegated to dedicated service modules under `app/services/` to keep controllers thin.
- **Blueprint Pattern:** Modular routing is implemented via Flask Blueprints to separate customer and admin routes.

### 7.3 UML Documentation

UML diagrams mapping the domain entities (Class Diagram), user actions (Use Case Diagram), and the booking workflow (Sequence Diagram) are available in the root directory as `.png` files.

---

## 8. Recommendation Engine

The recommendation engine (`app/services/recommendation_service.py`) translates customer intent into a ranked list of suitable vehicles using a heuristic scoring algorithm. 

**Inputs:**
1. Passenger Count
2. Daily Budget
3. Trip Purpose (city, family, offroad, luxury, eco)
4. Rental Duration

**Scoring Logic:**
Cars are evaluated against these inputs and awarded points based on how well they match the criteria (e.g., budget alignment, capacity, vehicle category match). Cars exceeding the budget by more than 10% or violating rental duration constraints are excluded. The top 3 highest-scoring vehicles are returned. This approach provides tailored suggestions without the overhead of machine learning models.

---

## 9. Coding Standards

- **Encapsulation:** Model classes contain their own state-mutation logic. The Service Layer isolates business logic from HTTP routing.
- **Performance:** SQLAlchemy ORM queries utilize targeted filters (`filter_by()`) and relationship loading strategies (`lazy=True`) to minimize database load.
- **Style:** Code adheres to PEP 8 standards with 4-space indentation and line lengths under 100 characters. Naming conventions follow standard Python practices (PascalCase for classes, snake_case for functions and variables).

---

## 10. Testing

The project includes a comprehensive Pytest test suite covering models, services, and HTTP routes. Tests run against an in-memory SQLite database (`TestingConfig`) to ensure complete isolation.

To run the suite:
```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

---

## 11. Software Evolution

The application is structured for future scalability and maintainability:

- **CI/CD Integration:** Automated tests and linters (Flake8) can be run on every pull request to prevent regressions.
- **Database Migrations:** While `seed_data.py` drops and recreates the database for testing, production environments should utilize Flask-Migrate (Alembic) for incremental schema updates without data loss.
- **API Versioning:** Future API expansions should use versioned URL prefixes (e.g., `/api/v1/cars`) to maintain backward compatibility.

---

## 12. Known Issues

- Deleted vehicles currently do not automatically remove their associated image files from the `images/` directory.
- Safari on older iOS versions may require manual date format entry due to partial `<input type="date">` support.
- A theoretical race condition could occur if multiple customers submit bookings for the identical vehicle simultaneously before the database transaction locks.

---

## 13. License

This project is released under the MIT License.

---

## 14. Credits

Developed by Smriti Bhandari as a system design and architecture project.

*For technical questions or bug reports, please open a GitHub Issue on the repository.*
