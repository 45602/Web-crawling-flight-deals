import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from services.fetch_comments import fetch_comments
from services.searchers import ReviewSearcher


def find_flights(destination, source, date, criteria):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(f"https://www.kayak.com/flights/{destination}-{source}/{date}")
    time.sleep(15)

    flights = []

    elem = driver.find_element(By.ID, "searchResultsList")
    elem = elem.find_element(By.CSS_SELECTOR, "div")
    elems = elem.find_elements(By.CLASS_NAME, "Flights-Results-FlightResultItem")
    for elem in elems:
        flight = {}
        flight["time"] = " ".join([elem.find_element(By.CSS_SELECTOR, ".depart-time").text, elem.find_element(By.CSS_SELECTOR, ".depart-time + .meridiem").text, "-", elem.find_element(By.CSS_SELECTOR, ".arrival-time").text, elem.find_element(By.CSS_SELECTOR, ".arrival-time + .meridiem").text])
        flight["price"] = elem.find_element(By.CSS_SELECTOR, ".price span").text
        flight["duration"] = elem.find_element(By.CSS_SELECTOR, ".duration .top").text
        stops_count = elem.find_element(By.CSS_SELECTOR, ".stops .top").text
        stops = elem.find_element(By.CSS_SELECTOR, ".stops .bottom").text
        flight["stops"] = stops_count + (": " + stops if stops_count != "nonstop" else "")
        flight["airlines"] = elem.find_element(By.CSS_SELECTOR, ".times .bottom").text.split(", ")
        flights.append(flight)

    driver.close()

    for airline in [airline for flight in flights for airline in flight["airlines"]]:
        fetch_comments(airline)
        
    flights = sort(flights, criteria, asc=True)

    return flights


sentiment_map = {"positive": 1, "neutral": 0, "negative": -1}


def sort(flights, criteria, asc=False):
    for flight in flights:
        score = 0
        for airline in flight["airlines"]:
            with ReviewSearcher() as searcher:
                comments = searcher.search(airline, criteria)
            if len(comments) == 0:
                score += 0.5
                continue
            sentiments = [sentiment_map[comment["sentiment"]] * comment["score"] for comment in comments]
            avg_sentiment = sum(sentiments) / len(sentiments)
            score += avg_sentiment
        score /= len(flight["airlines"])
        flight["score"] = score
        
    return list(sorted(flights, key=lambda flight: flight["score"], reverse=not asc))

