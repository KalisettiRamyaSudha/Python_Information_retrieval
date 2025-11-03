import PyPDF2
import re
import string
from collections import Counter

#--------------LOADING RESUME FILE--------------

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

#-------------CLEAN AND TOKENIZE TEXT -----------

def clean_and_tokenize(text):
    """Remove punctuation, stop words, numbers and converts to lowercase"""
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()

    stopwords = {"the", "and", "a", "to", "of", "in", "for", "on", "with", "at", 
        "by", "from", "is", "an", "as", "it", "be", "this", "that"}
    words = [w for w in words if w not in stopwords and len(w) > 2]

    return words

#-------------COUNT KEYWORD FREQUENCY------------

def extract_keywords(words, top_n=10):
    """Returns the top N most common words."""
    counter = Counter(words)
    return counter.most_common(top_n)

#---------COMPARE RESUME WITH JOB DESCRIPTION ----------

def match_score(resume_words, job_description):
    """Calculate percentage of job keywords found in resume"""
    job_words = clean_and_tokenize(job_description)
    overlap = len(set(job_words) & set(resume_words))
    score = (overlap/ len(set(job_words)))*100
    return round(score, 2)

#--------------MAIN EXECUTION------------------------------

if __name__ == "__main__":
    file_path = input("Enter your resume file name along with the path:").strip()
    text = extract_text_from_pdf(file_path)

    words = clean_and_tokenize(text)
    top_keywords = extract_keywords(words)

    print("\n Top 10 Keywords in your resume:")
    for word, freq in top_keywords:
        print(f"{word}: {freq}")

    selection = input("\n Do you want to compare your resume with job description? (y/n):").lower()
    if selection=="y":
        jd = input("\n Paste the job description and responsibilities:\n")
        score = match_score(words, jd)
        print(f"\n Resume Job match score: {score}%")