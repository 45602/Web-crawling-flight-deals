import lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import  DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery, TermQuery, BooleanClause, PrefixQuery
from org.apache.lucene.store import NIOFSDirectory


class BaseSearcher():
    def __init__(self, indexDirName, analyzer):
        indexDirPath = f"app/data/{indexDirName}"
        indexDir = NIOFSDirectory(Paths.get(indexDirPath))
        self.reader = DirectoryReader.open(indexDir)
        self.searcher = IndexSearcher(self.reader)
        self.queryAnalyzer = analyzer

    def closeIndex(self):
        self.reader.close()
        
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.closeIndex()


class ReviewSearcher(BaseSearcher):
    def __init__(self):
        super().__init__("review_index", StandardAnalyzer())

    def search(self, airline, phrases):
        builder = BooleanQuery.Builder()
        builder.add(TermQuery(Term("airline", airline)), BooleanClause.Occur.MUST)
        for phrase in phrases:
            builder.add(QueryParser("comment", self.queryAnalyzer).parse(phrase), BooleanClause.Occur.SHOULD)
        builder.setMinimumNumberShouldMatch(1)
        query = builder.build()
        docs = self.searcher.search(query, 100)
        hits = docs.scoreDocs
        
        comments = []
        for hit in hits:
            docId = hit.doc
            score = hit.score
            doc = self.searcher.doc(docId)
            
            comment = {"score": score, **{k: doc.get(k) for k in ["airline", "commentId", "sentiment"]}}
            comments.append(comment)

        return comments


class AirportSearcher(BaseSearcher):
    def __init__(self):
        super().__init__("airport_index", SimpleAnalyzer())

    def search(self, text):
        builder = BooleanQuery.Builder()
        for field in ["name", "code", "municipality"]:
            builder.add(PrefixQuery(Term(field, text.lower())), BooleanClause.Occur.SHOULD)
        builder.setMinimumNumberShouldMatch(1)
        query = builder.build()
        docs = self.searcher.search(query, 3)
        hits = docs.scoreDocs

        airports = []
        for hit in hits:
            docId = hit.doc
            doc = self.searcher.doc(docId)
            airport = {k: doc.get(k) for k in["name", "code", "municipality"]}
            airports.append(airport)

        return airports


if __name__ == '__main__':
    lucene.initVM()
    
    with ReviewSearcher() as searcher:
        print(searcher.search("air-serbia", ["flight"]))

    with AirportSearcher() as searcher:
        print(searcher.search("beg"))