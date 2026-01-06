from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def optimize_resume(job_description: str) -> str:
    """Optimize resume based on job description"""
    
    sections= ["summary", "experience", "skills"]
    modified_sections = {}
    for section in sections:
    # Create prompt
        with open(f"./resume_template/src/{section}.tex", 'r') as f:
            base_section = f.read()
        prompt = f"""Modify and return the {section} section to align with this job description.

            Instructions for different sections:
            1. Summary: Rewrite to emphasize relevant experiences to the job description. (3-4 lines)
            2. Experience: Keep titles/companies/dates. Rewrite bullets for relevance. 3-4 bullets per role.
            3. Skills: Use only the most relevant skills from the job description, incorporating applicable skills from the base section. Organize them into four primary categories with 4–6 skills each. Add 1–2 supplementary categories only if significant additional skill areas are present.
            4. Do not change formatting or LaTeX structure for the sections.
            5. Use keywords and terminology from the job posting sparingly to pass ATS.
            VERY IMPORTANT: Return ONLY complete LaTeX code, no explanations or markdown formatting based on the given base_section.

        """
            
        # Call API
        response = client.chat.completions.create(
            model="gpt-4.1-2025-04-14",  # or "gpt-4-turbo" or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are an expert resume optimizer. You modify resumes to match job descriptions while maintaining professional quality. Always return only the LaTeX code without any markdown formatting or explanations."},
                {"role": "user", "content": f" {prompt} \n . This is job description: {job_description} \n This is base section: {base_section}"}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract and clean LaTeX code
        latex_code = response.choices[0].message.content
        latex_code = latex_code.replace("```latex", "").replace("```", "").strip()
        modified_sections[section] = latex_code
        
    return modified_sections

# Usage
# if __name__ == "__main__":
#     job_desc = """
#     BlackStone eIT, a leading computer software company, is looking for a skilled and motivated AI & ML Engineer to join our innovative team. In this role, you will be at the forefront of developing and implementing state-of-the-art artificial intelligence (AI) and machine learning (ML) algorithms to enhance our product offerings and optimize business functions. You will work collaboratively with data scientists, software engineers, and product teams to translate complex data into actionable insights and effective machine learning models. Your expertise will play a pivotal role in driving data-driven decision-making within the organization. This is an exciting opportunity to work on high-impact projects that leverage the latest advancements in AI and ML technologies. Requirements Proven experience as an AI & ML Engineer or in a related field, with at least 3 years of experience. Strong understanding of machine learning algorithms, deep learning, natural language processing, and computer vision techniques. Proficiency in programming languages such as Python, Java, or R. Hands-on experience with ML frameworks and libraries (TensorFlow, Keras, PyTorch, etc.). Experience with data preprocessing, feature extraction, and model evaluation. Background in statistics and mathematics to enhance algorithm performance. Ability to work with large datasets and experience with big data technologies (Hadoop, Spark, etc.) is a plus. Excellent problem-solving skills, attention to detail, and a collaborative attitude. Strong verbal and written communication skills to convey technical concepts to non-technical stakeholders. A degree in Computer Science, Mathematics, Data Science, or a related field is preferred. Benefits Paid Time Off Performance Bonus Training & Development
#     """
    
#     ops = optimize_resume(job_desc)
#     # print("ssss\n",ops)
#     # Save output
#     with open("./output/summary.tex", 'w') as f:
#         f.write(ops["summary"])
#     with open("./output/experience.tex", 'w') as f:
#         f.write(ops["experience"])
#     with open("./output/skills.tex", 'w') as f:
#         f.write(ops["skills"])
    
#     print("✓ Resume optimized and saved to optimized_resume.tex")