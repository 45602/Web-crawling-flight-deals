import os
import lucene
import csv

from java.nio.file import Paths
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField, FloatPoint
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import NIOFSDirectory


class BaseIndexer():
    def __init__(self, indexDirName, analyzer, createNewIndex):
        indexDirPath = f"data/{indexDirName}"
        if not os.path.exists(indexDirPath):
            createNewIndex = True
            os.makedirs(indexDirPath, exist_ok=True)

        indexDir = NIOFSDirectory(Paths.get(indexDirPath))
        config = IndexWriterConfig(analyzer)

        if createNewIndex:
            config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        else:
            config.setOpenMode(IndexWriterConfig.OpenMode.APPEND)

        self.indexer = IndexWriter(indexDir, config)

    def finishIndexing(self):
        self.indexer.close()
        
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.finishIndexing()


class ReviewIndexer(BaseIndexer):
    def __init__(self, createNewIndex=False):
        super().__init__("review_index", StandardAnalyzer(), createNewIndex)

    def indexReview(self, airline, commentId, comment, sentiment):
        doc = Document()

        doc.add(StringField("airline", airline, Field.Store.YES))
        doc.add(StringField("commentId", commentId, Field.Store.YES))
        doc.add(TextField("comment", comment, Field.Store.NO))
        doc.add(StringField("sentiment", sentiment, Field.Store.YES))

        self.indexer.addDocument(doc)


class AirportIndexer(BaseIndexer):
    def __init__(self, createNewIndex=False):
        super().__init__("airport_index", SimpleAnalyzer(), createNewIndex)

    def indexAirport(self, name, code, municipality):
        doc = Document()

        doc.add(TextField("name", name, Field.Store.YES))
        doc.add(TextField("code", code, Field.Store.YES))
        doc.add(TextField("municipality", municipality, Field.Store.YES))

        self.indexer.addDocument(doc)


if __name__ == '__main__':
    lucene.initVM()
    
    data_folder = "../data/review_data"
    with ReviewIndexer(True) as indexer:
        for company in os.listdir(data_folder):
            for commentId in os.listdir(f"{data_folder}/{company}"):
                with open(f"{data_folder}/{company}/{commentId}") as f:
                    comment = f.read()
                commentId = commentId.split(".")[0] # remove extension
                indexer.indexReview(company, commentId, comment, "neutral")

    with open("../data/airports.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        airports = list(reader)
        airports = list(filter(lambda airport: airport["iata_code"] != "", airports)) # keep only airports that have IATA code

    with AirportIndexer(True) as indexer:
        for airport in airports:
            indexer.indexAirport(airport["name"], airport["iata_code"], airport["municipality"])
