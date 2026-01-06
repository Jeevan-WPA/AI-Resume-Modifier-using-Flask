import asyncio
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup
import time
import os
import csv

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
selectors = {
                "job_description":r"#jobDescriptionText",
                "job_title":r"#viewJobSSRRoot > div > div.fastviewjob.jobsearch-ViewJobLayout--standalone.css-81tydb.eu4oa1w0.hydrated > div.css-1yuy2sm.eu4oa1w0 > div > div > div.jobsearch-JobComponent.css-rndth6.eu4oa1w0 > div.jobsearch-InfoHeaderContainer.jobsearch-DesktopStickyContainer.css-rbjs5z.eu4oa1w0 > div:nth-child(1) > div.jobsearch-JobInfoHeader-title-container.css-1u3gzh9.eu4oa1w0",
                "company":r"#viewJobSSRRoot > div > div.fastviewjob.jobsearch-ViewJobLayout--standalone.css-81tydb.eu4oa1w0.hydrated > div.css-1yuy2sm.eu4oa1w0 > div > div > div.jobsearch-JobComponent.css-rndth6.eu4oa1w0 > div.jobsearch-InfoHeaderContainer.jobsearch-DesktopStickyContainer.css-rbjs5z.eu4oa1w0 > div:nth-child(1) > div.css-1xky5b5.eu4oa1w0 > div > div > div > div.css-oy1dfc.eu4oa1w0 > div.css-19qk8gi.eu4oa1w0",
                "location":r"#viewJobSSRRoot > div > div.fastviewjob.jobsearch-ViewJobLayout--standalone.css-81tydb.eu4oa1w0.hydrated > div.css-1yuy2sm.eu4oa1w0 > div > div > div.jobsearch-JobComponent.css-rndth6.eu4oa1w0 > div.jobsearch-InfoHeaderContainer.jobsearch-DesktopStickyContainer.css-rbjs5z.eu4oa1w0 > div:nth-child(1) > div.css-1xky5b5.eu4oa1w0 > div > div > div > div.css-89aoy7.eu4oa1w0"
            }

async def scrape_jd(page, url):
    await page.goto(url)
    await asyncio.sleep(3)  # allow content to load fully
    html =await page.content()
    soup = BeautifulSoup(html, "html.parser")
    results = {}
    for key, selector in selectors.items():
        el = soup.select_one(selector)
        results[key] = el.get_text(separator=" ",strip=True) if el else None
    results["url"] = url
    results["status"] = "applied"
    results["date_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return results

def open_chrome_with_debugging():
    chrome_proc=subprocess.Popen([
        chrome_path,
        "--remote-debugging-port=9222",
        r'--user-data-dir=C:\playwright\ChromeProfile'
    ])
    return chrome_proc

def update_csv(csv_path,job):
    """Update CSV file with new job details if needed."""
    fieldnames = [
    "date_time",
    "company",
    "job_title",
    "location",
    "job_description",
    "url",
    "status"
]

    file_exists = os.path.exists(csv_path)

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        writer.writerow(job)
        
def save_as_pdf(latex_path, output_dir=None):
    """
    Convert a LaTeX file to PDF using pdflatex safely.

    Args:
        latex_path (str or Path): Path to the .tex file.
        output_dir (str or Path, optional): Where to save the PDF. 
            Defaults to the same directory as the .tex file.

    Returns:
        Path: Path to the generated PDF.
    """
    latex_path = Path(latex_path).resolve()
    if output_dir is None:
        output_dir = latex_path.parent
    else:
        output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={output_dir}",
        str(latex_path)
    ]

    # Run twice for references, TOC, etc.
    for _ in range(2):
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print("LaTeX compilation failed!")
            print(result.stdout)
            print(result.stderr)
            raise RuntimeError("PDF compilation failed.")

    pdf_path = output_dir / latex_path.with_suffix(".pdf").name
    return pdf_path