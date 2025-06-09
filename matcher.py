import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text.lower())
    keywords = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop]
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
