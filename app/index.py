import json
from flask import Flask, request
from vectorizer_loader import vectorizer
from ai_model import loaded_model
app = Flask(__name__)


@app.route("/")
def hello_world():
  return "Hello, World!"

@app.route("/predict", methods=['POST'])
def predict_senitment():
  print(request.data)
  content_json = json.loads(request.data)
  print(content_json, flush=True)
  text = content_json['text']
  vectorized_text = vectorizer.transform([text])
  sentiment = loaded_model.predict(vectorized_text)
  result = "Sentiment is "  + str(sentiment)
  return result

@app.route("/flights", methods=['POST'])
def find_flight():
  results = 'resultats'#json.dumps('crawl_flights()')
  return results