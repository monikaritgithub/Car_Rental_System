# 🚗 Smriti Car Rental System

> **An automated, full-stack car rental management platform** built with Python, Flask, and SQLite.  
> Developed as a Masters-level Software Engineering assignment demonstrating OOP architecture, design patterns, and software evolution principles.

---

## Table of Contents

1. [Project Background & Introduction](#1-project-background--introduction)  
2. [System Features](#2-system-features)  
3. [Technology Stack](#3-technology-stack)  
4. [Installation & Configuration Guide](#4-installation--configuration-guide)  
   - 4.1 [Prerequisites](#41-prerequisites)  
   - 4.2 [Windows Quick Start](#42-windows-quick-start)  
   - 4.3 [Linux / macOS Quick Start](#43-linux--macos-quick-start)  
   - 4.4 [Manual Step-by-Step Setup](#44-manual-step-by-step-setup)  
5. [Operating the System](#5-operating-the-system)  
   - 5.1 [Demo Credentials](#51-demo-credentials)  
   - 5.2 [Customer Workflow](#52-customer-workflow)  
   - 5.3 [Admin Workflow](#53-admin-workflow)  
6. [Project Structure & File Purposes](#6-project-structure--file-purposes)  
7. [Design and Architecture (Task 1)](#7-design-and-architecture-task-1)  
   - 7.1 [Architectural Overview](#71-architectural-overview)  
   - 7.2 [Design Patterns Used](#72-design-patterns-used)  
   - 7.3 [UML Diagrams](#73-uml-diagrams)  
8. [Innovative Feature: AI Recommendation Engine (Task 2)](#8-innovative-feature-ai-recommendation-engine-task-2)  
9. [Coding Standards & Best Practices](#9-coding-standards--best-practices)  
10. [Running Tests](#10-running-tests)  
11. [Software Evolution Plan (Task 3)](#11-software-evolution-plan-task-3)  
12. [Known Bugs and Issues](#12-known-bugs-and-issues)  
13. [Licensing](#13-licensing)  
14. [Credits](#14-credits)  

---

## 1. Project Background & Introduction

The modern car rental industry often struggles with legacy systems that rely on manual paperwork, leading to inefficiencies, slow processing times, and a high margin for human error. A customer wanting to book a car must phone ahead, fill out paper forms, and wait for staff to manually check availability — all of which are processes prone to mistakes and customer frustration.

The **Smriti Car Rental System** was developed as a software engineering solution to automate and streamline the entire vehicle rental lifecycle. By digitizing user management, fleet tracking, and reservation processing, this system significantly reduces administrative overhead and enhances customer satisfaction.

### Core Objectives

| Objective | How It Is Met |
|---|---|
| Automate the rental process | End-to-end digital booking from search to payment |
| Reduce paperwork errors | Database-driven validation and status tracking |
| Differentiate user roles | Separate Customer and Admin portals with distinct privileges |
| Enforce business rules | Service layer validates dates, availability, and rental periods |
| Provide business insights | Admin report dashboard with revenue and fleet analytics |

Built with a robust **Object-Oriented MVC Architecture** using Python, Flask, and SQLite, the platform provides two distinct, secure interfaces:

1. **Customer Portal (Port 5000):** A sleek, intuitive platform for users to browse the fleet, receive AI-powered vehicle recommendations, and securely book rentals.
2. **Admin Dashboard (Port 5001):** A comprehensive management suite for staff to oversee fleet availability, approve/reject bookings, manage dynamic additional charges, and track revenue.

---

## 2. System Features

### Customer Interface (Port 5000)

| Feature | Description |
|---|---|
| Immersive Homepage | Full-bleed hero section with live availability stats and fleet highlights |
| Fleet Browsing | Filter by category (Sedan, SUV, Luxury, Truck, Economy) with animated car cards |
| Car Detail View | Specifications, mileage, pricing breakdown, and one-click booking |
| Secure Booking | Date validation, rental period constraint checks, and integrated mock payment checkout |
| My Bookings | Track, view, and cancel pending reservations with real-time status |
| AI Car Recommender | Smart heuristic engine that suggests the best car based on budget, purpose, and passenger count |
| Auto-Generated Payment Info | Random mock card and expiry assigned on registration for seamless demo experience |

### Admin Interface (Port 5001)

| Feature | Description |
|---|---|
| Live Dashboard | Real-time KPIs: pending bookings, fleet availability, and total revenue |
| Fleet Management | Full CRUD — add, edit, delete vehicles; set pricing, limits, descriptions, and upload photos |
| Booking Approval | Review all pending bookings; approve (marks car unavailable) or reject (triggers refund) |
| Cancel Approved Bookings | Admin can cancel an approved booking, releasing the car and issuing a refund |
| Additional Charges | Manage per-car extra fees (GPS, Insurance, Airport surcharge) as per-day or one-time charges |
| Payments Overview | View all transactions system-wide with payment status |
| System Report | Revenue totals, fleet utilisation percentages, and booking status breakdown |

---

## 3. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend Framework | Python 3.x, Flask 3.0.3 | Web server and routing |
| ORM / Database | SQLAlchemy 2.0, SQLite | Persistent data storage |
| Authentication | Werkzeug (PBKDF2-SHA256) | Secure password hashing |
| Frontend | HTML5, Vanilla CSS, Jinja2 | Templating and UI rendering |
| Font | Montserrat (Google Fonts) | Typography |
| Forms | Flask-WTF, WTForms | Form handling and CSRF protection |
| Session Management | Flask-Login 0.6.3 | User session management |
| Testing | Pytest 8.3.2, pytest-flask 1.3.0 | Automated unit and route testing |
| Environment Config | python-dotenv 1.0.1 | Environment variable management |

---

## 4. Installation & Configuration Guide

### 4.1 Prerequisites

Before installing, ensure you have the following installed on your system:

- **Python 3.10 or higher** — [Download from python.org](https://www.python.org/downloads/)
- **pip** — Python package manager (bundled with Python 3.4+)
- **Git** — For cloning the repository

Verify your Python installation:
```bash
python --version
# Expected: Python 3.10.x or higher
```

### 4.2 Windows Quick Start

1. Clone or download the repository to your local machine.
2. Open **Command Prompt** or **PowerShell** in the project root directory.
3. Run the startup script:

```cmd
run.bat
```

The script will automatically:
- Create a Python virtual environment (`.venv/`)
- Install all dependencies from `requirements.txt`
- Seed the database with demo cars, customers, and an admin account
- Launch both servers simultaneously

### 4.3 Linux / macOS Quick Start

1. Clone or download the repository.
2. Open a terminal in the project root directory.
3. Make the script executable and run it:

```bash
chmod +x run.sh
./run.sh
```

The startup script performs the same steps as the Windows version automatically.

### 4.4 Manual Step-by-Step Setup

If you prefer to set up manually (for example, for a custom environment or debugging):

**Step 1 — Clone the repository**
```bash
git clone <repository-url>
cd Car_Rental_System
```

**Step 2 — Create and activate a virtual environment**
```bash
# Create the environment
python -m venv .venv

# Activate on Linux/macOS:
source .venv/bin/activate

# Activate on Windows:
.venv\Scripts\activate
```

**Step 3 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4 — Seed the database**
```bash
python scripts/seed_data.py
```

This creates the `car_rental.db` SQLite file and populates it with:
- 1 Admin account
- 3 Demo customer accounts
- 10 Sample vehicles across all categories
- Sample bookings in various states

**Step 5 — Start the Customer Portal**
```bash
python customer_server.py
```

**Step 6 — In a NEW terminal, start the Admin Portal**
```bash
python admin_server.py
```

**Accessing the System:**

| Interface | URL |
|---|---|
| Customer Portal | http://127.0.0.1:5000 |
| Admin Portal | http://127.0.0.1:5001 |

---

## 5. Operating the System

### 5.1 Demo Credentials

| Role | Email | Password | Notes |
|---|---|---|---|
| Admin | admin@smriticars.com | admin123 | Full management access |
| Customer | james@example.com | customer123 | Has existing bookings |
| Customer | aiko@example.com | customer123 | Clean account for testing |

### 5.2 Customer Workflow

The standard customer journey through the system:

1. **Register** — Navigate to `http://127.0.0.1:5000/register`. Fill in your name, email, phone, driver's licence number, and choose a password. A mock payment card is automatically assigned.

2. **Browse the Fleet** — Click **"Browse Cars"** on the homepage. Use the category filter to narrow results. Only cars with `available_now = True` are shown.

3. **View Car Details** — Click any car card to see full specifications, daily rate, and additional charges.

4. **Get AI Recommendation** — Click **"Find My Car"** in the navigation. Enter your passenger count, daily budget, rental purpose (city / family / offroad / eco / luxury), and number of days. The engine scores all available cars and returns the top 3 matches.

5. **Book a Car** — From a car's detail page, click **"Book Now"**. Select start and end dates. The system validates the dates, checks availability, and displays the total fee breakdown (base rate + additional charges).

6. **Checkout** — Enter your card details (any 16-digit number works in demo mode). Click **"Confirm Booking"**. The booking is created with status **PENDING** and payment marked **COMPLETED**.

7. **Track Bookings** — Go to **"My Bookings"** to see all your reservations and their current status (PENDING / APPROVED / REJECTED / CANCELLED).

8. **Cancel a Booking** — A PENDING booking can be cancelled from **"My Bookings"**. The payment is automatically refunded.

### 5.3 Admin Workflow

1. **Login** — Navigate to `http://127.0.0.1:5001` and log in with admin credentials.

2. **Dashboard** — The landing page shows key metrics: pending bookings count, total fleet size, available cars, and recent revenue.

3. **Manage Fleet** — Go to **"Fleet Management"**.
   - **Add Car**: Click "Add New Vehicle", fill in make, model, year, mileage, daily rate, category, rental period limits, and optionally upload a photo.
   - **Edit Car**: Click the edit icon on any car card to modify its details.
   - **Delete Car**: Only possible if the car has no active (PENDING or APPROVED) bookings.

4. **Manage Bookings** — Go to **"Booking Requests"** to see all PENDING bookings.
   - **Approve**: Marks the booking as APPROVED and sets the car's `available_now` flag to `False`.
   - **Reject**: Marks the booking as REJECTED and changes the payment status to REFUNDED.

5. **Additional Charges** — Under Fleet Management, each car has an "Extras" section. Add per-day charges (e.g., GPS at $5/day) or one-time charges (e.g., Airport Pickup at $25). These are automatically included in future booking calculations.

6. **Generate Report** — Go to **"System Report"** for a full business analytics summary.

---

## 6. Project Structure & File Purposes

```
Car_Rental_System/
│
├── app/                            # Main application package
│   ├── __init__.py                 # Package marker
│   │
│   ├── admin_app/                  # Admin portal blueprint
│   │   ├── __init__.py             # Creates the admin Flask app via factory pattern
│   │   ├── routes.py               # Admin HTTP controllers (fleet CRUD, booking approval)
│   │   ├── static/css/             # Admin-specific CSS (corporate light theme)
│   │   └── templates/             # Admin Jinja2 HTML templates
│   │       ├── dashboard.html      # Admin landing page with KPI tiles
│   │       ├── fleet.html          # Car listing and management table
│   │       ├── add_car.html        # Form to add a new vehicle
│   │       ├── edit_car.html       # Form to edit an existing vehicle
│   │       ├── bookings.html       # Pending bookings review table
│   │       ├── booking_detail.html # Single booking detail and approve/reject form
│   │       ├── payments.html       # All payments overview
│   │       └── report.html         # Revenue and analytics report
│   │
│   ├── customer_app/               # Customer portal blueprint
│   │   ├── __init__.py             # Creates the customer Flask app via factory pattern
│   │   ├── routes.py               # Customer HTTP controllers (browse, book, AI recommend)
│   │   ├── static/css/             # Customer-specific CSS (GO Rentals inspired theme)
│   │   └── templates/             # Customer Jinja2 HTML templates
│   │       ├── index.html          # Homepage with hero section and live stats
│   │       ├── cars.html           # Fleet browsing with category filter
│   │       ├── car_detail.html     # Individual car specifications and booking button
│   │       ├── booking.html        # Date selection and fee preview form
│   │       ├── checkout.html       # Payment form (mock card entry)
│   │       ├── my_bookings.html    # Customer's reservation history
│   │       ├── recommend.html      # AI recommendation input form
│   │       ├── login.html          # Customer login form
│   │       └── register.html       # New customer registration form
│   │
│   ├── models/                     # SQLAlchemy ORM entity classes
│   │   ├── __init__.py             # Centralises all model imports for SQLAlchemy
│   │   ├── admin.py                # Admin entity (employeeId, name, email, password)
│   │   ├── customer.py             # Customer entity (licenseId, paymentInfo, etc.)
│   │   ├── car.py                  # Car entity (make, model, year, mileage, rate, etc.)
│   │   ├── booking.py              # Booking entity (dates, status, fee, admin notes)
│   │   ├── payment.py              # Payment entity (amount, card info, status)
│   │   └── additional_charge.py   # Extra fees per car (GPS, insurance, per-day or flat)
│   │
│   └── services/                   # Business logic layer (Service Layer pattern)
│       ├── __init__.py             # Package marker
│       ├── booking_engine.py       # Core logic: validate, calculate, create, approve, reject
│       ├── car_service.py          # Vehicle CRUD operations (add, update, delete, search)
│       ├── customer_service.py     # Registration, login authentication, session management
│       ├── payment_service.py      # Payment processing and refund logic
│       ├── recommendation_service.py # AI heuristic scoring for vehicle recommendations
│       └── report_service.py       # Analytics aggregation for admin reports
│
├── config/
│   ├── __init__.py                 # Package marker
│   └── settings.py                 # Environment configs (Dev / Test / Production classes)
│
├── scripts/
│   └── seed_data.py                # Initialises database with demo vehicles and users
│
├── tests/                          # Pytest test suite
│   ├── __init__.py                 # Package marker
│   ├── conftest.py                 # Pytest fixtures (app, client, sample data)
│   ├── test_models.py              # Unit tests for ORM model methods
│   ├── test_services.py            # Unit tests for booking engine and car service
│   ├── test_customer_routes.py     # Integration tests for customer HTTP routes
│   └── test_admin_routes.py        # Integration tests for admin HTTP routes
│
├── images/                         # Uploaded and seeded car photograph files
│
├── Class diagram.drawio            # Editable draw.io source for Class Diagram
├── Class diagram.drawio.png        # UML Class Diagram (exported PNG)
├── Sequence Diagram.drawio         # Editable draw.io source for Sequence Diagram
├── Sequence Diagram.drawio.png     # UML Sequence Diagram (exported PNG)
├── Use Case Diagram.drawio         # Editable draw.io source for Use Case Diagram
├── Use Case Diagram.drawio.png     # UML Use Case Diagram (exported PNG)
│
├── admin_server.py                 # Entry point to launch the Admin Flask app
├── customer_server.py              # Entry point to launch the Customer Flask app
├── database.py                     # Shared SQLAlchemy db instance (Singleton)
├── requirements.txt                # Python package dependencies
├── run.bat                         # Windows one-click startup script
├── run.sh                          # Linux/macOS one-click startup script
├── state.json                      # Development state tracking metadata
├── replace_emojis.py               # Utility script to sanitise emoji from database text
└── README.md                       # This documentation file
```

---

## 7. Design and Architecture (Task 1)

### 7.1 Architectural Overview

The system is built on a layered **Model-View-Controller (MVC)** architecture implemented within Flask's Application Factory pattern. This separation of concerns ensures that each layer can evolve independently, and business logic remains testable without a running web server.

```
┌─────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                    │
│          Jinja2 Templates (HTML + CSS)                       │
│    Customer Portal (Port 5000) | Admin Portal (Port 5001)    │
└──────────────────────────┬──────────────────────────────────┘
                           │  HTTP Requests / Responses
┌──────────────────────────▼──────────────────────────────────┐
│                       CONTROLLER LAYER                       │
│              Flask Blueprints (routes.py files)              │
│      Handles HTTP routing, session auth, form parsing        │
└──────────────────────────┬──────────────────────────────────┘
                           │  Function calls
┌──────────────────────────▼──────────────────────────────────┐
│                       SERVICE LAYER                          │
│    booking_engine | car_service | customer_service           │
│    payment_service | recommendation_service | report_service │
│      All business rules, validations, and calculations       │
└──────────────────────────┬──────────────────────────────────┘
                           │  ORM queries
┌──────────────────────────▼──────────────────────────────────┐
│                        MODEL LAYER                           │
│     SQLAlchemy ORM Classes: Car, Booking, Customer,          │
│     Admin, Payment, AdditionalCharge                         │
└──────────────────────────┬──────────────────────────────────┘
                           │  SQL queries
┌──────────────────────────▼──────────────────────────────────┐
│                       DATABASE LAYER                         │
│                  SQLite (car_rental.db)                      │
└─────────────────────────────────────────────────────────────┘
```

**Two separate Flask applications** are created by the factory functions, sharing the same database but running on different ports. This ensures that the admin portal is completely isolated from the customer-facing application and prevents any accidental cross-access.

### 7.2 Design Patterns Used

#### Application Factory Pattern
Both `create_customer_app()` and `create_admin_app()` in `app/customer_app/__init__.py` and `app/admin_app/__init__.py` use the Application Factory pattern. Instead of creating a global Flask app instance, a factory function accepts a configuration class and returns a fully configured application. This enables:
- Multiple independent app instances (customer + admin)
- Clean test isolation using `TestingConfig` with in-memory SQLite
- Easy environment switching (Development / Testing / Production)

#### Singleton Pattern — Shared Database Instance
The `database.py` file creates a single `SQLAlchemy` instance (`db`) that is shared across both Flask applications. This ensures all models and services use one consistent ORM session and connection pool.

```python
# database.py — a single shared instance
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```

Both `create_customer_app()` and `create_admin_app()` call `db.init_app(app)`, binding the same `db` object to each application context.

#### Service Layer Pattern (Facade)
Rather than placing business logic inside route handlers, all complex operations are delegated to dedicated service modules under `app/services/`. This is the Service Layer (also known as a Facade over the data layer):

| Service File | Responsibility |
|---|---|
| `booking_engine.py` | Orchestrates the full booking lifecycle (validate → calculate → create → approve/reject) |
| `car_service.py` | Vehicle CRUD operations with business-rule enforcement |
| `customer_service.py` | Customer registration, login authentication |
| `payment_service.py` | Mock payment processing and refund handling |
| `recommendation_service.py` | AI heuristic scoring algorithm |
| `report_service.py` | Business analytics aggregation |

#### Blueprint Pattern (Modular Routing)
Flask Blueprints are used to create modular, reusable route collections. The customer routes and admin routes are registered as separate Blueprints, preventing any namespace collisions and allowing each portal to evolve independently.

#### Repository-like Pattern (ORM Models)
SQLAlchemy models encapsulate not just data structure but also entity-level behaviour:
- `Car.set_availability(status)` — encapsulates the business rule of marking a car available/unavailable
- `Booking.validate_availability()` — encapsulates date validation logic within the Booking entity
- `Customer.set_password() / check_password()` — encapsulates Werkzeug hashing within the model
- `Payment.process_credit_card()` — encapsulates the mock payment transaction

### 7.3 UML Diagrams

#### Class Diagram

Defines all six domain entities and their relationships:
- **Customer** — registers, logs in, makes bookings and payments
- **Admin** — manages fleet, approves/rejects bookings, views reports
- **Car** — the rentable asset; contains availability flag and rental period constraints
- **Booking** — links a Customer to a Car for a date range with a status lifecycle (PENDING → APPROVED / REJECTED / CANCELLED)
- **Payment** — one-to-one record for each booking, tracks payment status and card information
- **AdditionalCharge** — optional or mandatory per-car extra fees (per-day or one-time)

![Class Diagram](Class%20diagram.drawio.png)

#### Use Case Diagram

Maps every user action across two actor groups:

**Customer Actor:**
- Register Account
- Login
- Browse Available Cars
- View Car Details
- Get AI Recommendation
- Book a Car (includes: validate availability, calculate fee, process payment)
- Cancel Reservation
- View My Bookings

**Admin Actor:**
- Login
- View Dashboard
- Add / Edit / Delete Car
- Manage Additional Charges
- Review Booking Requests
- Approve Booking (extends: mark car unavailable)
- Reject Booking (extends: issue refund)
- Cancel Approved Booking (extends: release car + issue refund)
- View Payments
- Generate System Report

![Use Case Diagram](Use%20Case%20Diagram.drawio.png)

#### Sequence Diagram

Documents the complete 21-step booking and payment approval workflow between all system actors:

1. Customer navigates to car listing → UI queries `available_now = True`
2. Customer selects a car
3. Customer submits booking form with dates
4. UI calls Booking Engine: validate availability and rent period
5. Engine queries database for conflicting bookings
6. Engine returns validation result
7. UI displays fee breakdown (Days × Rate + Additional Charges)
8. Customer enters payment details and confirms
9. UI sends mock payment transaction
10. Payment gateway returns approval (always succeeds in demo)
11. Booking record created with `PENDING` status
12. Payment record created with `COMPLETED` status
13. Customer sees "Booking Pending" notice
14. Admin logs in and views pending bookings list
15. Admin clicks "Approve" or "Reject"
16. If Approved: Engine sets `booking_status = APPROVED` and `car.available_now = False`
17. If Rejected: Engine sets `booking_status = REJECTED` and `payment_status = REFUNDED`
18. Customer checks My Bookings and sees final status

![Sequence Diagram](Sequence%20Diagram.drawio.png)

---

## 8. Innovative Feature: AI Recommendation Engine (Task 2)

### Problem Statement

Traditional car rental systems present customers with an undifferentiated list of all available vehicles, forcing them to manually compare specifications, prices, and categories. This leads to **decision fatigue**, longer session times, and lower booking conversion rates.

### Innovation: Heuristic AI Scoring Algorithm

The **Smart AI Car Recommendation Engine** (`app/services/recommendation_service.py`) solves this by translating a customer's *intent* directly into a ranked list of the most suitable vehicles — without requiring any expensive third-party machine learning API.

**How It Works:**

Customers provide four inputs:
1. **Passenger Count** — How many people need to travel
2. **Daily Budget** — Maximum spend per day
3. **Trip Purpose** — `city` / `family` / `offroad` / `luxury` / `eco`
4. **Rental Duration** — Number of days (used to filter by car's min/max rent period)

The engine then scores every available car using a weighted multi-factor algorithm:

| Factor | Points | Logic |
|---|---|---|
| Under budget | +30 | Car's daily rate ≤ customer's budget |
| Slightly over budget | +10 | Within 10% of budget (great fit override) |
| Fits passengers | +20 | Category capacity ≥ passenger count |
| City purpose match | +40 | Economy / Compact / Hatchback category |
| Family purpose match | +40 | SUV / Minivan / Sedan category |
| Luxury purpose match | +40 | Luxury / Premium category |
| Off-road purpose match | +40 | SUV category |
| Eco/Electric match | +50 | Hybrid/EV model name or Electric category |
| Vehicle recency bonus | +(year − 2015) × 2 | Newer cars score slightly higher |

Cars exceeding the budget by more than 10% or violating min/max rental days are **strictly excluded**. The top 3 highest-scoring cars are returned.

**Competitive Advantage:**

- **No API cost** — A lightweight heuristic provides 80% of the benefit of a full ML model at 0% of the cost
- **Addresses decision fatigue** — Customers make faster, more confident booking decisions
- **Transparent reasoning** — The UI displays *why* each car was recommended (e.g., "Under budget", "Spacious and safe for families")
- **Personalised UX** — Each customer sees a different top-3 based on their unique inputs, creating a premium, tailored experience

---

## 9. Coding Standards & Best Practices

The codebase adheres to the following engineering conventions throughout:

### Modularity and Encapsulation
- Each model class encapsulates its own business logic (e.g., `Car.set_availability()`, `Booking.validate_availability()`, `Customer.set_password()`)
- The Service Layer (`app/services/`) separates business logic from HTTP routing
- Flask Blueprints enforce modular route namespacing

### Performance Considerations
- SQLAlchemy ORM queries use targeted filters (`filter_by()`) rather than loading entire tables into memory
- `db.session.flush()` is used before `commit()` when inter-record foreign key IDs are needed within a single transaction (see `booking_engine.py`)
- The `lazy=True` relationship loading strategy avoids N+1 query problems on large result sets

### Commenting and Documentation
- All module-level docstrings explain the file's purpose and UML mapping
- All class-level docstrings explain the entity's role in the system
- All method-level docstrings describe parameters, return values, and sequence diagram step references
- Inline comments explain non-obvious logic (e.g., why `card_last_four` is stored instead of the full number)

### Indentation and Formatting
- All files use 4-space indentation (PEP 8 compliant)
- Lines are kept under 100 characters
- Logical groupings are separated by blank lines with block comments

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `Car`, `Booking`, `BookingEngine`)
- **Functions and variables**: `snake_case` (e.g., `calculate_total_fee`, `daily_rate`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `STATUS_PENDING`, `PAYMENT_COMPLETED`)
- **Private helpers**: prefixed with underscore (e.g., `_generate_booking_id()`)

---

## 10. Running Tests

The project includes a comprehensive Pytest test suite covering models, services, and HTTP routes.

### Run All Tests
```bash
# Activate your virtual environment first
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

python -m pytest tests/ -v
```

### Expected Output
```
tests/test_models.py::test_car_repr PASSED
tests/test_models.py::test_booking_status_update PASSED
tests/test_models.py::test_payment_process_card PASSED
tests/test_models.py::test_additional_charge_per_day PASSED
tests/test_models.py::test_additional_charge_one_time PASSED
tests/test_services.py::test_validate_availability_valid PASSED
tests/test_services.py::test_validate_availability_past_date PASSED
tests/test_services.py::test_validate_availability_car_unavailable PASSED
tests/test_services.py::test_create_and_approve_booking PASSED
tests/test_customer_routes.py::test_homepage_loads PASSED
tests/test_customer_routes.py::test_cars_page_loads PASSED
tests/test_customer_routes.py::test_login_page_loads PASSED
tests/test_customer_routes.py::test_register_page_loads PASSED
tests/test_admin_routes.py::test_admin_login_page_loads PASSED
...

17 passed in X.XXs
```

### Test Coverage Summary

| Test File | Coverage Area |
|---|---|
| `test_models.py` | Unit tests for ORM model methods (`Car`, `Booking`, `Payment`, `AdditionalCharge`) |
| `test_services.py` | Unit tests for `booking_engine` validation, fee calculation, create, approve |
| `test_customer_routes.py` | Integration tests for customer portal HTTP routes (homepage, cars, auth pages) |
| `test_admin_routes.py` | Integration tests for admin portal HTTP routes (login page, dashboard access) |

All tests use an **in-memory SQLite database** (`TestingConfig`) so they run in isolation without affecting the development database.

---

## 11. Software Evolution Plan (Task 3)

### Managing Software Maintenance

The system is architected specifically for long-term maintainability:

**CI/CD Pipeline (GitHub Actions)**
```yaml
# Example workflow trigger
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Pytest
        run: python -m pytest tests/ -v
      - name: Lint with Flake8
        run: flake8 app/ --max-line-length=100
```
- Every pull request automatically runs all 17+ tests and the Flake8 linter
- Merges are blocked if any test fails, preventing regression

**Modular Refactoring Strategy**
- Because all database interactions are mediated by the Service Layer, swapping SQLite for PostgreSQL requires only a one-line change in `config/settings.py` (`SQLALCHEMY_DATABASE_URI`)
- The mock Payment service (`payment_service.py`) can be replaced with a real Stripe SDK without touching any route handler

**Issue Tracking**
- Use GitHub Issues with labels: `bug`, `enhancement`, `documentation`, `regression`
- Triage weekly in Agile sprint planning
- Critical bugs (security, data loss) get same-day hotfix branches

### Versioning

The project will follow **Semantic Versioning (SemVer)** — `MAJOR.MINOR.PATCH`:

| Version Component | Trigger | Example |
|---|---|---|
| `PATCH` (x.x.**1**) | Bug fixes, documentation updates | Fixing image deletion bug |
| `MINOR` (x.**1**.0) | New backward-compatible features | Adding mobile API endpoints |
| `MAJOR` (**2**.0.0) | Breaking changes (schema restructure, API redesign) | Migrating to PostgreSQL with new schema |

**Git Branching Strategy (Git Flow):**

```
main          ← Production-ready releases only (tagged v1.0.0, v1.1.0, etc.)
develop       ← Integration branch, all features merge here first
feature/xxx   ← Individual feature development (e.g., feature/mobile-api)
hotfix/xxx    ← Emergency patches branched from main (e.g., hotfix/xss-fix)
release/x.x.x ← Release preparation branch
```

### Backward Compatibility

**Database Migrations with Alembic (Flask-Migrate)**

Currently, `seed_data.py` drops and recreates the database. In production, this is unacceptable as it destroys customer data. The evolution plan is:

```bash
# Integrate Flask-Migrate
pip install Flask-Migrate

# Generate a migration script for a schema change
flask db migrate -m "add_passenger_capacity_to_car"

# Apply the migration without data loss
flask db upgrade
```

Alembic generates incremental SQL migration scripts that apply changes column-by-column, preserving all existing records.

**API Versioning for Future Mobile Integration**

Future mobile app endpoints will use versioned URL prefixes to ensure older app versions continue to function:

```
/api/v1/cars          ← Original API (maintained for app v1.x)
/api/v2/cars          ← Improved API (for app v2.x+, new response format)
```

**Deprecation Policy**

- Features scheduled for removal are marked with a `@deprecated` comment and a `DeprecationWarning` log for one full `MINOR` release cycle
- Removal only happens in the next `MAJOR` release, giving all integrations time to update

---

## 12. Known Bugs and Issues

| ID | Severity | Area | Description | Planned Fix (Version) |
|---|---|---|---|---|
| BUG-001 | Low | Admin Fleet | When a car is deleted, its associated image file is not removed from the `images/` directory, which may cause disk space accumulation | v1.1.0 (PATCH) |
| BUG-002 | Low | Frontend | Safari on older iOS versions may not fully support `<input type="date">`, falling back to a plain text input and requiring manual date format entry | v1.1.0 (PATCH) |
| BUG-003 | Medium | Booking Engine | In an extremely high-traffic scenario, a theoretical race condition could occur if two customers submit bookings for the same car at the exact same millisecond before the database transaction locks | v1.2.0 (Database-level transaction locking) |

---

## 13. Licensing

This project is released under the **MIT License**.

```
MIT License

Copyright (c) 2026 Smriti Bhandari

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 14. Credits

| Field | Detail |
|---|---|
| **Developer** | Smriti Bhandari |
| **Role** | Lead Software Engineer |
| **Context** | Masters-level Software Engineering Assignment |
| **Institution** | Academic System Design Exercise |
| **System Version** | v1.0.0 |
| **Last Updated** | September 2026 |

### Acknowledgements

- **Flask** — Micro web framework by Pallets Projects
- **SQLAlchemy** — Python SQL toolkit and ORM by Mike Bayer
- **Werkzeug** — WSGI utility library, used for secure password hashing
- **Pytest** — Testing framework by Holger Krekel and contributors
- **draw.io / diagrams.net** — Free UML diagramming tool used for all architectural diagrams
- **Google Fonts (Montserrat)** — Typography used in the UI

---

*For technical questions or bug reports, please open a GitHub Issue on the repository.*
