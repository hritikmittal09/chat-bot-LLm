import fitz  # PyMuPDF
import json
import re

pdf_path = "test.pdf"
output_json = "resume.json"

# Step 1: Extract text
doc = fitz.open(pdf_path)
text = "\n".join(page.get_text("text") for page in doc)

# Step 2: Rough section splits (depends on resume format)
sections = {
    "skills": re.findall(r"(Skills|Technical Skills)[\s\S]*?(?=\n[A-Z])", text, re.IGNORECASE),
    "experience": re.findall(r"(Experience|Work Experience)[\s\S]*?(?=\n[A-Z])", text, re.IGNORECASE),
    "projects": re.findall(r"(Projects)[\s\S]*?(?=\n[A-Z])", text, re.IGNORECASE),
    "education": re.findall(r"(Education)[\s\S]*", text, re.IGNORECASE),
}

# Helper to clean text
def clean_section(data):
    if not data:
        return ""
    return re.sub(r"\n+", " ", data[0]).strip()

resume_data = {
    "name": "Hritik Mittal",
    "title": "Full-stack Developer",
    "summary": "Frontend & backend developer with 2 years experience in React, Angular, Node.js, Python and more.",
    "skills": clean_section(sections["skills"]),
    "experience": clean_section(sections["experience"]),
    "projects": clean_section(sections["projects"]),
    "education": clean_section(sections["education"])
}

# Step 3: Save JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(resume_data, f, indent=2)

print(f"✅ Resume data saved in {output_json}")
