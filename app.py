from flask import Flask, render_template
from flask import request, send_file
import os
from pipeline import run_pipeline
from db import init_db, get_jobs
import sqlite3

app = Flask(__name__)
OUTPUT_DIR = "./Website/output"
init_db()  # Create DB tables if not exists

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        job_url = request.form.get("url")
        if not job_url:
            return render_template("error.html", message="No URL provided")
        try:
            pdf_path = run_pipeline(job_url)
            return render_template("success.html", pdf_path=pdf_path)
        except Exception as e:
            return render_template("error.html", message=str(e))
    return render_template("index.html")

@app.route("/history")
def history():
    jobs = get_jobs()
    return render_template("history.html", jobs=jobs)

@app.route("/download_pdf/<path:pdf_path>")
def download_pdf(pdf_path):
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return render_template("error.html", message="PDF not found")

@app.route("/view_pdf/<path:pdf_path>")
def view_pdf(pdf_path):
    if os.path.exists(pdf_path):
        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=False  # THIS is the key
        )
    return "PDF not found", 404

@app.route("/view_resume/<int:job_id>")
def view_resume(job_id):
    conn = sqlite3.connect("./jobs.db")
    c = conn.cursor()
    c.execute("SELECT pdf_path FROM jobs WHERE id = ?", (job_id,))
    row = c.fetchone()
    conn.close()

    if not row or not row[0]:
        return "Resume not found", 404

    return send_file(
        row[0],
        mimetype="application/pdf",
        as_attachment=False
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
