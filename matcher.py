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
    matched = set(jd_keywords) & set(resume_keywords)
    missing = set(jd_keywords) - set(resume_keywords)
    score = (len(matched) / len(jd_keywords)) * 100 if jd_keywords else 0
    return matched, missing, round(score, 2)

def main():
    with open("job_description.txt", "r", encoding="utf-8") as jd_file:
        jd_text = jd_file.read()

    with open("resume.txt", "r", encoding="utf-8") as resume_file:
        resume_text = resume_file.read()

    jd_keywords = extract_keywords(jd_text)
    resume_keywords = extract_keywords(resume_text)

    matched, missing, score = match_keywords(jd_keywords, resume_keywords)

    print("\nMatch Score:", score, "%")
    print("\nMatched Keywords:", matched)
    print("\nMissing Keywords:", missing)

if __name__ == "__main__":
    main()
