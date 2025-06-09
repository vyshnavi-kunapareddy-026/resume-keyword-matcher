import spacy
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load skills list from JSON
with open("skills_list.json", "r", encoding="utf-8") as f:
    SKILLS_LIST = set(json.load(f))

CUSTOM_STOP_WORDS = {"experience", "ability", "development", "work", "project", "team"}

def extract_keywords(text):
    doc = nlp(text.lower())

    noun_chunks = [chunk.text.strip() for chunk in doc.noun_chunks]

    keywords = []
    for chunk in noun_chunks:
        chunk_doc = nlp(chunk)
        lemmatized = " ".join([token.lemma_ for token in chunk_doc if not token.is_stop])
        if lemmatized and lemmatized in SKILLS_LIST and lemmatized not in CUSTOM_STOP_WORDS:
            keywords.append(lemmatized)

    for token in doc:
        if token.lemma_ in SKILLS_LIST and token.lemma_ not in CUSTOM_STOP_WORDS:
            keywords.append(token.lemma_)

    return list(set(keywords))

def match_keywords(jd_keywords, resume_keywords):
    jd_keywords = set([kw.strip().lower() for kw in jd_keywords])
    resume_keywords = set([kw.strip().lower() for kw in resume_keywords])

    matched = jd_keywords & resume_keywords
    missing = jd_keywords - resume_keywords

    score = (len(matched) / len(jd_keywords)) * 100 if jd_keywords else 0

    return {
        "matched": sorted(matched),
        "missing": sorted(missing),
        "match_score": round(score, 2),
        "total_keywords_in_jd": len(jd_keywords),
        "total_matched": len(matched)
    }

def main():
    with open("job_description.txt", "r", encoding="utf-8") as jd_file:
        jd_text = jd_file.read()

    with open("resume.txt", "r", encoding="utf-8") as resume_file:
        resume_text = resume_file.read()

    jd_keywords = extract_keywords(jd_text)
    resume_keywords = extract_keywords(resume_text)

    matched_result = match_keywords(jd_keywords, resume_keywords)
    matched = matched_result["matched"]
    missing = matched_result["missing"]
    score = matched_result["match_score"]

    print("\nMatch Score:", score, "%")
    print("\nMatched Keywords:", matched)
    print("\nMissing Keywords:", missing)
    print(f"\nMatched keywords in job description {matched_result['total_matched']} out of {matched_result['total_keywords_in_jd']} total keywords.")
    print("\nTotal Keywords in Job Description:", matched_result['total_keywords_in_jd'])

if __name__ == "__main__":
    main()
