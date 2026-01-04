# Dictionary App (Flask)

A small Python (Flask) dictionary web app that uses the Free Dictionary API and Pexels for images.

Features
- Search English words
- Definitions, part of speech, examples
- Synonyms & antonyms (if available)
- Pronunciation audio (when provided by the API)
- Related images via Pexels
- Simple search history stored in session

Quick start
1. Create a virtualenv and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `PEXELS_API_KEY` and `SECRET_KEY`.

3. Run the app:

```bash
python app.py
```

Open http://127.0.0.1:5000 and try words like `apple`, `aberration`, `serendipity`.

Notes
- Pexels requires an API key (free signup). If no key is set, image section is omitted.
- This scaffold covers Tasks 1 and basic UI for Task 2. Next steps: richer parsing for synonyms/antonyms, better UI/UX, and deployment.

Running tests
1. Install pytest: `pip install pytest`
2. Run tests from project root:

```bash
pytest -q
```

The UI snapshot from the tests is saved to `tests/snapshots/aberration.html` for manual inspection.

Deployment (production-ready)
1. Install a WSGI server, e.g. `gunicorn`:

```bash
pip install gunicorn
```

2. Run with gunicorn (on Linux/WSL or a server):

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

3. (Optional) For Heroku-like deploys, add a `Procfile` with:

```
web: gunicorn app:app
```

Notes on static hosting and environment
- Ensure `PEXELS_API_KEY` is set in environment or `.env`.
- Set `SECRET_KEY` to a secure value for production sessions.
