# Smriti Car Rental System

A complete, full-stack car rental platform built with Python, Flask, and SQLite, featuring a dual-interface architecture — a premium dark-themed customer portal and a secure admin management system.

---

## Features

### Customer Interface (Port 5000)
- Immersive Homepage — Full-bleed hero section with live car image and live availability stats
- Fleet Browsing — Filter by category (Sedan, SUV, Luxury, Truck, Economy) with animated car cards
- Car Detail View — Specifications, mileage, pricing, and one-click booking
- Secure Booking — Date validation, rental period checks, and integrated mock payment checkout
- My Bookings — Track, view, and cancel pending reservations
- Auto-Generated Payment Info — Random card and expiry assigned on registration

### Admin Interface (Port 5001)
- Dashboard — Real-time overview of pending bookings, fleet status, and revenue
- Fleet Management — Add, edit, delete vehicles; set pricing and rental limits
- Booking Approval — Review, approve (marks car unavailable), or reject reservations with notes
- Payments Overview — View all transactions system-wide
- System Report — Revenue and fleet utilisation analytics

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.x, Flask |
| Database | SQLite with SQLAlchemy ORM |
| Authentication | Werkzeug password hashing |
| Frontend | HTML5, Vanilla CSS (dark theme), Jinja2 |
| Font | Outfit (Google Fonts) |
| Testing | Pytest with pytest-flask |

---

## Quick Start

### Windows

```cmd
run.bat
```

### Linux / macOS

```bash
chmod +x run.sh
./run.sh
```

The startup script will:

1. Activate or create the Python virtual environment
2. Install all requirements from requirements.txt
3. Seed the database with demo data
4. Launch both servers simultaneously

| Interface | URL |
|---|---|
| Customer Portal | http://127.0.0.1:5000 |
| Admin Portal | http://127.0.0.1:5001 |

---

## Demo Credentials

| Role | Email | Password |
|---|---|---|
| Admin | admin@smriticars.com | admin123 |
| Customer | james@example.com | customer123 |
| Customer | aiko@example.com | customer123 |

---

## Running Tests

```cmd
.venv\Scripts\activate
python -m pytest tests/ -v
```

All 17 tests pass across models, services, customer routes, and admin routes.

---

## System Design Diagrams

The project is built directly from three UML diagrams stored in the repository root.

### Class Diagram

Defines all entities: Customer, Admin, Car, Booking, Payment and their relationships.

![Class Diagram](Class%20diagram.drawio.png)

### Use Case Diagram

Maps every user action from browsing and booking (Customer) to approving and reporting (Admin).

![Use Case Diagram](Use%20Case%20Diagram.drawio.png)

### Sequence Diagram

Documents the full 21-step booking and payment approval workflow between all system actors.

![Sequence Diagram](Sequence%20Diagram.drawio.png)

---

## Project Structure

```
CarRentalSystem/
    app/
        admin_app/
            static/css/         Admin dark theme CSS
            templates/          Admin HTML pages
            routes.py           Admin routes
        customer_app/
            static/css/         Customer dark theme CSS
            templates/          Customer HTML pages
            routes.py           Customer routes
        models/                 SQLAlchemy models
        services/               Business logic layer
    config/
        settings.py             App configuration
    scripts/
        seed_data.py            Database initialisation
    tests/                      Pytest test suite
    images/                     Car images
    Class diagram.drawio.png    UML Class Diagram
    Use Case Diagram.drawio.png UML Use Case Diagram
    Sequence Diagram.drawio.png UML Sequence Diagram
    run.bat                     Windows startup script
    run.sh                      Linux/macOS startup script
    requirements.txt
    README.md
```

---

## License

This project was developed as part of an academic system design exercise.
2026 Smriti Bhandari. All rights reserved.
