import json
import lucene
from flask import Flask, request, render_template
from services.find_flights import find_flights
from services.sentiment_prediction import sentiment_predict
from services.autocompletion import autocomplete_location
app = Flask(__name__, template_folder='templates')


@app.before_first_request
def load_index():
    lucene.initVM()


@app.route("/")
def hello_world():
  # return "Hello, World!"
  return render_template('index.html')


@app.route("/predict", methods=['GET'])
def predict_senitment():
  text = request.args['text']
  sentiment = sentiment_predict(text)
  result = "Sentiment is " + str(sentiment)
  return result

@app.route("/flights", methods=['GET'])
def find_flight():
  destination = request.args['dest']
  source = request.args['source']
  date = request.args['date']
  criteria = [request.args[f"option{i}"] for i in range(1, 5) if request.args.get(f"option{i}")]
  res = find_flights(destination, source, date, criteria)
  results = res
  return render_template('results.html', content=results)


@app.route("/autocomplete-location", methods=['GET'])
def autocomplete_loc():
  location_input = request.args["location"]
  location_result = autocomplete_location(location_input)
  results = json.dumps(location_result)
  return results
