import lucene
from services.searchers import AirportSearcher

def autocomplete_location(location_input):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    with AirportSearcher() as searcher:
        return searcher.search(location_input)