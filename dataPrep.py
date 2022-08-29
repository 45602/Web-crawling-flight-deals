import pandas as pd
import os
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

airComp = input("Air company for review ")
def createLink(airComp):
    link = 'https://www.airlinequality.com/airline-reviews/' + airComp + "/" #'/?pagesize=100'
    return link

def launchBrowser(link):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(link)
    for i in range(1,5):
        reviewXPath ='/html/body/div[1]/div/div/div/section[3]/div[1]/article/article[' + str(i) + ']/div[2]/div/div[1]'
        rateXPath = '/html/body/div[1]/div/div/div/section[3]/div[1]/article/article[' + str(i) + ']/div[1]'
        review = driver.find_element("xpath", reviewXPath).text + "\n"
        rate = driver.find_element("xpath", rateXPath).text + "\n"
        data = review + "\n " + rate + "\n"
        fileName = createFileName(data)
        print(fileName)
        createFolderStructure(airComp, fileName, data)
    sleep(5)

def createFolderStructure(airCompany, fileName, data):
    dirPath = os.path.dirname(__file__)
    filePath = os.path.join(dirPath, 'review_data', airCompany)
    if not os.path.exists(filePath):
        print("Creating a folder...")
        os.mkdir(filePath)
        print("Entering data...")
        with open(filePath + '/' + fileName, 'w', encoding="utf-8") as f:
            try:
                f.write(data)
            except IOError:
                print("Problem with making a file")
            finally:
                f.close()
    else:
        with open(filePath + '/' + fileName, 'w', encoding="utf-8") as f:
            try:
                f.write(data)
            except IOError:
                print("Problem with making a file")
            finally:
                f.close()

def createFileName(string):
    return "article" + str(hash(string)) + ".txt"

link = createLink(airComp)
launchBrowser(link)
