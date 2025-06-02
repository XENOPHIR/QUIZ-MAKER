# 🧠 Quiz Generator App

This is a lightweight quiz app built with Flask and MySQL. You can upload a file with 300+ questions, take a quiz of 10 random questions, and view your score + review incorrect answers.

---

## 🚀 Local Setup with Docker

> Recommended for fastest start

### 1. Install Docker:  

https://docs.docker.com/get-docker/

### 2. Clone the project and create config files

```bash
cp .env.example .env
Modify .env if needed (MySQL settings, etc.)

3. Run the project
bash
Copy
Edit
docker compose up --build
4. Access the app
Quiz app: http://localhost:5000

Adminer (DB GUI): http://localhost:8080

Server: db, user: quiz_user, password: quiz_pass, DB: quiz_db

🧪 Local Setup without Docker
1. Install Python
Make sure Python 3.10+ is installed.

2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Setup environment variables
Create .env:

env
Copy
Edit
DB_HOST=localhost
DB_PORT=3306
DB_NAME=quiz_db
DB_USER=root
DB_PASSWORD=4444
You need a running MySQL instance manually created (e.g., via XAMPP, MAMP, or system service).

4. Run the app
bash
Copy
Edit
python app.py
Then go to d

📦 File Format for Upload
vbnet
Copy
Edit
Question: What is the capital of France?
A) Berlin
B) Madrid
C) Paris
D) Rome
Answer: C