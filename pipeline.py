import asyncio
import os
import shutil
import time
from pathlib import Path
import scrape_jd
import resume_build
from playwright.async_api import async_playwright
from db import save_job

SRC = "./resume_template"
OUTPUT_DIR = "./output"

async def run_job_pipeline(url: str = None, raw_text: str = None):
    # Case 1: Raw Text Provided (Skip Scraper)
    if raw_text:
        job_details = {
            "job_description": raw_text,
            "company": "Manual_Input",
            "job_title": "Custom Role",
            "location": "Remote/Unspecified",
            "url": "Manual Text Entry",
            "status": "applied",
            "date_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        # Only run optimization steps, skip browser logic
        optimized_sections = resume_build.optimize_resume(job_details.get("job_description", ""))
        
        # Use a consistent naming for manual entries
        company_safe = "Manual_Job_" + str(int(time.time()))
        dst = Path(OUTPUT_DIR) / company_safe
        
        return await process_and_save_resume(dst, optimized_sections, job_details)

    # Case 2: URL Provided (Run Scraper)
    elif url:
        async with async_playwright() as p:
            # Launch browser (headless=True is generally better for server apps, but keeping existing logic)
            # Checking if we can use standard launch instead of connecting to existing chrome for stability
            # But aggressively keeping existing behavior for now as user didn't ask to change scraping logic
            try:
                chrome = scrape_jd.open_chrome_with_debugging()
                await asyncio.sleep(3)
                browser = await p.chromium.connect_over_cdp("http://localhost:9222")
                context = browser.contexts[0]
                page = await context.new_page()
                
                # Scrape
                job_details = await scrape_jd.scrape_jd(page, url)
                await browser.close()
                chrome.terminate()
            except Exception as e:
                # Fallback if browser fails? For now just raise
                raise e

            optimized_sections = resume_build.optimize_resume(job_details.get("job_description", ""))
            
            # Prepare destination
            company = job_details.get("company", "UnknownCompany")
            if not company: company = "UnknownCompany"
            company_safe = company.replace("/", "_").replace(" ", "_").replace(",", "_")
            dst = Path(OUTPUT_DIR) / f"{company_safe}_resume"
            
            return await process_and_save_resume(dst, optimized_sections, job_details)
    
    else:
        raise ValueError("Either URL or Raw Text must be provided")

async def process_and_save_resume(dst: Path, optimized_sections: dict, job_details: dict):
    """Helper to generate PDF and save to DB, shared by both methods"""
    
    # 1. Prepare Directory
    if not dst.exists():
        # Copy template but ignore the dynamic sections we are about to overwrite
        shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("summary.tex", "experience.tex", "skills.tex"))
    
    dst_src = dst / "src"
    dst_src.mkdir(exist_ok=True, parents=True)

    # 2. Write New Sections
    for name in ("summary", "experience", "skills"):
        # Ensure we have content for each section
        content = optimized_sections.get(name, "")
        with open(dst_src / f"{name}.tex", "w", encoding="utf-8") as f:
            f.write(content)

    # 3. Compile PDF
    # Assuming the main tex file is named 'resume.tex' at the root of the copied template
    pdf_path = scrape_jd.save_as_pdf(dst / "resume.tex", output_dir=dst)
    
    # 4. Save to DB
    job_details["pdf_path"] = str(pdf_path)
    # Ensure job_details has all keys expected by save_job
    # (Checking db.py might be good, but assuming job_details matches schema)
    save_job(job_details)
    
    return pdf_path

def run_pipeline(url: str = None, raw_text: str = None):
    return asyncio.run(run_job_pipeline(url, raw_text))
