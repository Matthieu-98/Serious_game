# RIASEC Project

This project is a Django-based web application that lets users explore a playful RIASEC-style personality quiz through themed quests. The experience includes several interactive paths such as elemental, painter, and geometer journeys, with questions stored in the database and results displayed at the end.

## Features

- Interactive personality quiz based on RIASEC categories
- Multiple themed quests: elemental, painter, and geometer
- Session-based gameplay and result tracking
- SQLite database support
- Seed command to populate quiz questions

## Project Structure

- `fate_95/` — main Django app containing models, views, templates, and management commands
- `riasec_project/` — project settings and URL configuration
- `static/` — static assets such as images and CSS
- `db.sqlite3` — local SQLite database

## Requirements

- Python 3.10+
- Django 5.0+

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies

```bash
pip install django
```

## Database Setup

Run migrations:

```bash
python manage.py migrate
```

Seed the quiz questions:

```bash
python manage.py seed_questions
```

## Run the Application

Start the development server:

```bash
python manage.py runserver
```

Then open your browser at:

```text
http://127.0.0.1:8000/
```

## Admin Panel

You can access the Django admin panel at:

```text
http://127.0.0.1:8000/admin/
```

Create a superuser if needed:

```bash
python manage.py createsuperuser
```

## Notes

- The quiz data is seeded through the custom management command `seed_questions`.
- The app uses session storage to track user progress during the quiz.

## License

This project is for educational and personal use.
