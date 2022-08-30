import json
from flask import Flask, request
from services.find_flights import find_flights
from services.sentiment_prediction import sentiment_predict
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
  sentiment = sentiment_predict(text)
  result = "Sentiment is "  + str(sentiment)
  return result

@app.route("/flights", methods=['POST'])
def find_flight():
  content_json = json.loads(request.data)
  destination = content_json['destination']
  source = content_json['source']
  date = content_json['date']
  res = find_flights(destination, source, date)
  results = json.dumps(res)
  return results