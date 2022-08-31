import os
import re
import lucene
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from services.sentiment_prediction import sentiment_predict
from services.indexers import ReviewIndexer


def scrape(airline):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(f"https://www.airlinequality.com/airline-reviews/{airline}/?pagesize=100")

    for i in range(1, 100):
        reviewXPath ='/html/body/div[1]/div/div/div/section[3]/div[1]/article/article[' + str(i) + ']/div[2]/div/div[1]'
        try:
            review = driver.find_element("xpath", reviewXPath).text
        except Exception:
            print("Can't find reviews for", airline)
            break
        review = " ".join(review.split("|")[1:])
        fileName = str(hash(review))
        return saveReview(airline, fileName, review)
        


def fetch_comments(airline):
    airline = prepAirlineName(airline)

    folder = f"app/data/review_data/{airline}"
    if os.path.exists(folder):
        return

    os.mkdir(folder)
    
    sentiment = scrape(airline)
    return sentiment


def saveReview(airline, fileName, text):
    folder = f"app/data/review_data/{airline}"
    with open(f"{folder}/{fileName}.txt", 'w') as f:
        f.write(text)

    sentiment = sentiment_predict(text)

    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    with ReviewIndexer() as indexer:
        indexer.indexReview(airline, fileName, text, sentiment)

    return sentiment


def prepAirlineName(string):
    return re.sub(" \d+", "", string).replace(" ", "-").lower()


