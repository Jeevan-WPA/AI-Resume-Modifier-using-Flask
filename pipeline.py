import asyncio
import os
import shutil
from pathlib import Path
import scrape_jd
import resume_build
from playwright.async_api import async_playwright
from db import save_job

SRC = "./resume_template"
OUTPUT_DIR = "./output"

async def run_job_pipeline(url: str):
    async with async_playwright() as p:
        chrome = scrape_jd.open_chrome_with_debugging()
        await asyncio.sleep(3)
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()
        await asyncio.sleep(3)

        job_details = await scrape_jd.scrape_jd(page, url)
        save_job(job_details)  # Save to SQLite

        optimized_sections = resume_build.optimize_resume(job_details.get("JD", ""))
        company = job_details.get("company", "UnknownCompany").replace("/", "_").replace(" ", "_")
        dst = Path(OUTPUT_DIR) / f"{company}_resume"
        dst_src = dst / "src"
        if not dst.exists():
            shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("summary.tex","experience.tex","skills.tex"))
        dst_src.mkdir(exist_ok=True)

        for name in ("summary", "experience", "skills"):
            with open(dst_src / f"{name}.tex", "w", encoding="utf-8") as f:
                f.write(optimized_sections[name])

        pdf_path = scrape_jd.save_as_pdf(dst / "resume.tex", output_dir=dst)

        await browser.close()
        chrome.terminate()
        return pdf_path

def run_pipeline(url: str):
    return asyncio.run(run_job_pipeline(url))
