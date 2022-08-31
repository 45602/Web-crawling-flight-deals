import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def find_flights(destination, source, date):
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

    flights = sort(flights,criteria = 'price', asc=True)

    return flights


if __name__ == "__main__":
    print(find_flights("MIL", "LHR", "2022-09-19"))

def sort(flights, criteria, asc=True):
    if asc == True:
        return flights.sort_values(criteria, ascending=True)
    else:
        return flights.sort_values(criteria, ascending=False)