import json
from flask import Flask, request
from services.find_flights import find_flights
from services.sentiment_prediction import sentiment_predict
from services.autocompletion import autocomplete_location
app = Flask(__name__)


@app.route("/")
def hello_world():
  return "Hello, World!"

@app.route("/predict", methods=['GET'])
def predict_senitment():
  print(request.data)
  content_json = json.loads(request.data)
  print(content_json, flush=True)
  text = content_json['text']
  sentiment = sentiment_predict(text)
  result = "Sentiment is "  + str(sentiment)
  return result

@app.route("/flights", methods=['GET'])
def find_flight():
  content_json = json.loads(request.data)
  destination = content_json['destination']
  source = content_json['source']
  date = content_json['date']
  res = find_flights(destination, source, date)
  results = json.dumps(res)
  return results


@app.route("/autocomplete-location", methods=['GET'])
def autocomplete_loc():
  content_json = json.loads(request.data)
  location_input = content_json['location']
  location_result = autocomplete_location(location_input)
  results = location_result
  return results
