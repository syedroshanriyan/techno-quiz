# Techno Quiz

A simple Flask-based quiz / buzzer web application used for running quiz sessions.

## Features
- Host/admin interface to manage quizzes
- Player join flow and buzzer interface
- Real-time board display

## Requirements
- Python 3.8+
- See `requirements.txt` for exact dependencies

## Setup
1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate # macOS / Linux
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open your browser at `http://127.0.0.1:5000`.

## Project Structure

- `app.py` — Flask application entrypoint
- `templates/` — HTML templates
- `static/` — CSS, JS, assets
- `requirements.txt` — Python dependencies

## Notes
- This project is intended as a lightweight, local quiz tool. Customize templates and logic in `app.py` for your needs.
