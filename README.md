📘 Dictionary App (Flask)

A lightweight Python Flask dictionary web application that fetches word meanings from the Free Dictionary API and displays related images using the Pexels API.

🚀 Features

🔍 Search English words

📖 Definitions, part of speech & usage examples

🔁 Synonyms & antonyms (if available)

🔊 Pronunciation audio (when provided)

🖼️ Related images via Pexels API

🕘 Simple search history using Flask sessions

🛠️ Tech Stack

Backend: Python, Flask

APIs: Free Dictionary API, Pexels API

Deployment: Docker, Gunicorn

Environment: WSL 2 (Windows)

⚡ Quick Start (Local – Without Docker)
1️⃣ Clone the repository
git clone https://github.com/MahithaSagiraju/dictionary-python-app.git
cd dictionary-python-app

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Environment variables

Copy .env.example to .env and set:

PEXELS_API_KEY=your_pexels_api_key
SECRET_KEY=your_secret_key

5️⃣ Run the app
python app.py


📍 Open: http://127.0.0.1:5000

Try words like: apple, aberration, serendipity

🐳 Docker Deployment (Recommended)
1️⃣ Build Docker image
docker build -t dictionary-app .

2️⃣ Run Docker container
docker run --env-file .env -p 5000:5000 dictionary-app


📍 App will be available at:
http://localhost:5000

✔ Runs using Gunicorn (production WSGI server)

🧪 Running Tests

Install pytest:

pip install pytest


Run tests:

pytest -q


📄 UI snapshot is saved at:

tests/snapshots/aberration.html

🌐 Production Notes

Pexels API key is required for images

If no key is provided, image section is skipped

Set a strong SECRET_KEY for session security

Gunicorn is used for production-ready deployment

📌 Future Enhancements

Advanced synonym/antonym parsing

Improved UI/UX

Cloud deployment (AWS / Render / Railway)

User authentication

👩‍💻 Author

Mahitha Sagiraju
GitHub: https://github.com/MahithaSagiraju
