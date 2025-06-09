# Resume Keyword Matcher

This tool compares a job description with a resume and gives:
- A match score (how closely the resume matches the job)
- Keywords that match
- Keywords that are missing

## Tech Used
- Python
- spaCy for NLP

## How to Run
1. Install requirements:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
