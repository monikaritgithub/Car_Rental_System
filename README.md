# Car Rental System

A full-stack car rental management platform built with Python, Flask, and SQLite. The application implements an Object-Oriented MVC architecture and uses the Application Factory pattern to serve isolated Customer and Admin portals.

## Technology Stack

- **Backend**: Python 3.10+, Flask 3.0.3, SQLAlchemy 2.0
- **Frontend**: HTML5, Vanilla CSS, Jinja2
- **Testing**: Pytest, pytest-flask

## Architecture

The system is separated into distinct layers to decouple routing, business logic, and data access:

- **Application Factory**: Isolated Flask apps for Customer (Port 5000) and Admin (Port 5001) portals to prevent cross-contamination of sessions and logic.
- **Service Layer**: Core business rules (booking validation, pricing logic, heuristic recommendations) are decoupled from HTTP controllers.
- **Data Access**: SQLAlchemy ORM handles database interactions and schema definitions.

## Getting Started

### Prerequisites

- Python 3.10+

### Local Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Car_Rental_System
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database with seed data:
   ```bash
   python scripts/seed_data.py
   ```

### Running the Application

The system consists of two separate services. Start them in separate terminal sessions:

```bash
# Terminal 1: Customer Portal (http://localhost:5000)
python customer_server.py

# Terminal 2: Admin Portal (http://localhost:5001)
python admin_server.py
```

*Note: For convenience, you can also use `run.sh` (Linux/macOS) or `run.bat` (Windows) to automatically setup the environment and launch both services.*

### Demo Credentials

- **Admin**: `admin@smriticars.com` / `admin123`
- **Customer**: `james@example.com` / `customer123`

## Testing

Run the test suite using pytest. The tests utilize an in-memory SQLite database to ensure isolation.

```bash
python -m pytest tests/ -v
```

## License

MIT License
