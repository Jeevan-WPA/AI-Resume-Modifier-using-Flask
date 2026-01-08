# AI Resume Modifier using Flask

A **Flask-based web application** that helps job seekers **modify and optimize their resumes** using AI and job description scraping. The app includes features like **automated resume revisions**, **job description extraction**, and an AI-powered text pipeline to tailor resumes for specific roles.

> ⚡ *This project is ideal for developers and job seekers looking to integrate AI into career tools and save time on tailoring resumes every time.*

---

## 🚀 Features

* 🧠 **AI-assisted Resume Modification** — Suggest improvements based on job descriptions.
* 📄 **Resume & JD Pipeline** — Extracts and processes data from resumes and job postings.
* 🔍 **Job Description Scraping** — Scrapes job listing text for guidance on how to tailor resume content.
* 🗂️ Modular Python/Flask structure — Easy to extend and integrate with AI APIs.
* 📌 Supports HTML templates for interface and routing with Flask.

---

## 🛠️ Tech Stack

| Technology              | Purpose                         |
| ----------------------- | ------------------------------- |
| Python                  | Core logic & scripting          |
| Flask                   | Web server & routing            |
| HTML / CSS              | UI templates                    |
| AI Model (Configurable) | Resume modification suggestions |

---

## 📁 Project Structure

```
AI-Resume-Modifier-using-Flask/
├── resume_template/           # Template files for resume output
├── templates/                 # Jinja2 HTML templates
├── .env.example               # Environment variables example
├── app.py                     # Main Flask application file
├── db.py                      # Database connection & models
├── pipeline.py                # AI & workflow pipeline logic
├── resume_build.py            # Resume building utilities
├── scrape_jd.py               # Job description scraper module
├── requirements.txt           # Project dependencies
└── README.md
```

---

## 🧩 Installation

### 🧪 Prerequisites

* Python 3.8+
* (Optional) Virtual environment tool like `venv` or `conda`

---

### ⚙️ Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Jeevan-WPA/AI-Resume-Modifier-using-Flask.git
   cd AI-Resume-Modifier-using-Flask
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate     # macOS/Linux
   venv\Scripts\activate        # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Rename `.env.example` to `.env` and add your keys/config:

   ```env
   # Example variables
    OPENAI_API_KEY = "your-openai-api-key-here"
   ```

---

## 🏃‍♂️ Running the App

```bash
python app.py 
```

Once the server is running, visit:

👉 `http://127.0.0.1:5000`

---

## 🧠 How It Works

1. **Upload Indeed Link** — Users upload their "Indeed" job application link.
2. **Scrapes Job Description** — Scrapes the target job description text and other details.
3. **AI Processing Pipeline** — The backend uses the job description and existing resume template to generate personalized recommendations or revisions.
4. **Output and Logging** — A modified resume ready for download and is logged in a sql database
---

## 🔮 Future Improvements

You might consider adding:

* ⭐ **Working for multiple Job Sites**
* 📌 **ATS Keyword Scoring**
* 🧑‍💻 **User Authentication**
* 📊 **Visual Analytics (match scores, suggestions breakdown)**

---

## 🤝 Contributing

Contributions are welcome! If you find improvements or bugs, feel free to:

1. Fork this repository
2. Create a branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to your branch (`git push origin feature-name`)
5. Open a pull request
