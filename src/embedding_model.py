from sklearn.feature_extraction.text import TfidfVectorizer

class EmbeddingModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")

    def fit(self, texts):
        self.vectorizer.fit(texts)

    def transform(self, texts):
        return self.vectorizer.transform(texts)
