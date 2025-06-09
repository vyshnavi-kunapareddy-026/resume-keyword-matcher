import spacy
import json
from rapidfuzz import fuzz

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load skills and weights from one JSON file
with open("skills_list.json", "r", encoding="utf-8") as f:
    SKILLS_DICT = json.load(f)
    SKILLS_LIST = set(SKILLS_DICT.keys())

CUSTOM_STOP_WORDS = {"experience", "ability", "development", "work", "project", "team"}

def extract_keywords(text):
    doc = nlp(text.lower())

    noun_chunks = [chunk.text.strip() for chunk in doc.noun_chunks]

    keywords = []
    for chunk in noun_chunks:
        chunk_doc = nlp(chunk)
        lemmatized = " ".join([token.lemma_ for token in chunk_doc if not token.is_stop])
        if lemmatized and lemmatized in SKILLS_LIST:
            keywords.append(lemmatized)

    for token in doc:
        if token.lemma_ in SKILLS_LIST:
            keywords.append(token.lemma_)

    return list(set(keywords))


def match_keywords(jd_keywords, resume_keywords):
    jd_keywords = set([kw.strip().lower() for kw in jd_keywords])
    resume_keywords = set([kw.strip().lower() for kw in resume_keywords])

    matched = set()
    missing = set()
    weighted_score = 0
    max_score = 0
    FUZZY_THRESHOLD = 85

    for jd_kw in jd_keywords:
        weight = SKILLS_DICT.get(jd_kw, 1)
        max_score += weight
        found_match = False

        for resume_kw in resume_keywords:
            if jd_kw == resume_kw or fuzz.token_sort_ratio(jd_kw, resume_kw) >= FUZZY_THRESHOLD:
                matched.add(jd_kw)
                weighted_score += weight
                found_match = True
                break

        if not found_match:
            missing.add(jd_kw)

    score_percent = (weighted_score / max_score * 100) if max_score > 0 else 0

    return {
        "matched": sorted(matched),
        "missing": sorted(missing),
        "match_score": round(score_percent, 2),
        "total_keywords_in_jd": len(jd_keywords),
        "total_matched": len(matched),
        "weighted_score": weighted_score,
        "max_possible_score": max_score
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
