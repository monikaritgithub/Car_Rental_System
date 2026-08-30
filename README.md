# Smriti Car Rental System

A complete car rental platform built with Python, Flask, and SQLite. This system features a dual-interface architecture: a customer-facing portal for browsing and booking vehicles, and a secure admin interface for fleet and reservation management.

## Features

### Customer Interface
- **Fleet Browsing:** View available cars with dynamic category filtering.
- **Reservations:** Book vehicles with built-in date validation and fee calculation.
- **Mock Payments:** Integrated checkout flow simulating a payment gateway.
- **Booking History:** Track current and past reservations, and cancel pending bookings.

### Admin Interface
- **Dashboard:** Real-time overview of fleet status, pending approvals, and recent bookings.
- **Fleet Management:** Add, edit, and remove vehicles. Set pricing and rental limits.
- **Booking Management:** Review incoming reservations, approve (marks car unavailable), or reject.
- **Financial Reports:** Generate system-wide summary reports covering utilization and revenue.

## Technology Stack

- **Backend:** Python 3.x, Flask
- **Database:** SQLite with SQLAlchemy ORM
- **Security:** Werkzeug password hashing
- **Frontend:** HTML5, Vanilla CSS, Jinja2 Templates
- **Testing:** Pytest

## Quick Start (Windows)

The project includes a startup script that handles database initialization and launches both servers simultaneously.

1. Ensure Python 3 is installed.
2. Run the startup script:
   ```cmd
   run.bat
   ```
3. The script will:
   - Run the database seed (creates tables, admin, customers, and cars).
   - Start the Customer Interface at [http://127.0.0.1:5000](http://127.0.0.1:5000)
   - Start the Admin Interface at [http://127.0.0.1:5001](http://127.0.0.1:5001)

### Demo Credentials

**Admin Account:**
- Email: `admin@smriticars.com`
- Password: `admin123`

**Customer Accounts:**
- Email: `james@example.com`
- Password: `customer123`
- Email: `aiko@example.com`
- Password: `customer123`

## Development

To run tests:
```cmd
.venv\Scripts\activate
python -m pytest tests/ -v
```

## Architecture

This project maps directly to the system design specification:
- **Class Diagram:** Implemented strictly through SQLAlchemy models.
- **Use Case Diagram:** Implemented through dedicated Flask routes and service layers.
- **Sequence Diagram:** The 21-step booking and payment flow is fully implemented in `app/services/booking_engine.py`.
