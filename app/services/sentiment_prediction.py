from services.vectorizer_loader import vectorizer
from services.ai_model import loaded_model


def sentiment_predict(text):
    vectorized_text = vectorizer.transform([text])
    sentiment_result = loaded_model.predict(vectorized_text)
    return sentiment_result[0]