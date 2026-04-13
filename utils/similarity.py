"""
similarity.py
-------------
Computes a similarity score between a resume and a job description
using TF-IDF vectorization and cosine similarity from scikit-learn.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):
    """
    Calculate how similar a resume is to a job description.

    How it works:
        1. Both texts are converted into TF-IDF vectors.
           (TF-IDF = Term Frequency – Inverse Document Frequency;
            it measures how important a word is in a document
            relative to a collection of documents.)
        2. Cosine similarity is computed between the two vectors.
           (A value of 1.0 means identical, 0.0 means completely different.)
        3. The result is returned as a percentage (0 – 100).

    Args:
        resume_text (str):      Text extracted from a resume.
        job_description (str):  The job description provided by the user.

    Returns:
        float: Similarity score as a percentage (0.0 – 100.0).
    """
    if not resume_text or not job_description:
        return 0.0

    # Combine the two texts into a list for the vectorizer
    documents = [resume_text, job_description]

    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Compute cosine similarity between resume (index 0) and JD (index 1)
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    # Convert to percentage and round to 2 decimal places
    return round(score * 100, 2)
