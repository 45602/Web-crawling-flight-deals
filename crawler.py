import scrapy 
from dataPrep import *

#link = inputData()
class Crawler(scrapy.Spider):
    name = "scrapy"
    start_urls = [link]
    print(start_urls)