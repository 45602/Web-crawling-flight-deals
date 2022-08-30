from vectorizer_loader import vectorizer
from ai_model import loaded_model


def sentiment_predict(text):
    vectorized_text = vectorizer.transform([text])
    sentiment_result = loaded_model.predict(vectorized_text)
    return sentiment_result