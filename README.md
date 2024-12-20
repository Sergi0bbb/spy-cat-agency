# Spy Cat Agency Management System

## Overview

The **Spy Cat Agency Management System** is a Django-based web application designed to manage spy cats, their missions, and targets. It showcases key features such as CRUD operations, relational database integration, and interaction with external APIs.

---

## Features

### Spy Cat Management

- **Create** profiles for spy cats with fields like:
    - Name
    - Breed
    - Years of Experience
    - Salary
- **Retrieve** details of all spy cats or a specific spy cat.
- **Update** attributes, such as the salary of a spy cat.
- **Delete** spy cats.

### Missions Management

- Create missions and assign available spy cats to them.
- Manage targets within missions with fields like:
    - Name
    - Country
    - Notes
    - Completion Status
- Prevent updates to targets once marked as completed.
- Delete missions only if they are not assigned to any spy cats.

### Validations

- Verify cat breeds using the [TheCatAPI](https://api.thecatapi.com/v1/breeds).
- Handle errors gracefully with appropriate status codes and messages.

---

## Project Structure

```plaintext
spy-cat-agency/
├── spy_cat/                 # Services and business logic
├── spy_cat_service/         # Core Django application
├── manage.py                # Main entry point for Django commands
├── db.sqlite3               # SQLite database
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

# Spy Cat Agency Management System

## Installation

### Prerequisites

- Python 3.10 or later
- Virtual environment tool (`venv`)
- SQLite (default) or any supported database
- [TheCatAPI](https://api.thecatapi.com/v1/breeds) key for breed validation

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/spy-cat-agency.git
   cd spy-cat-agency
   ```
2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```
5. **Start the Server**
   ```bash
   python manage.py runserver
   ```