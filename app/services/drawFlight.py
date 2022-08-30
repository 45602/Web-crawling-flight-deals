from geopy.geocoders import Nominatim
import plotly.express as px
import plotly.graph_objects as go

geolocator = Nominatim(user_agent="geoapiExercises")

def plotDots(coordinateOne, coordinateTwo):
    fig = px.scatter_mapbox(
        lon = [coordinateOne[1], coordinateTwo[1]],
        lat = [coordinateOne[0], coordinateTwo[0]],
        center = {"lat": abs(coordinateOne[0]+coordinateTwo[0])/2 , "lon": abs(coordinateOne[1]+coordinateTwo[1])/2},
        width = 2000,
        height = 1200, 
        zoom = 7
    )  
    return fig
def drawEdges(figure, coordinateOne, coordinateTwo):
            
    lons = [coordinateOne[1], coordinateTwo[1]]
    lats = [coordinateOne[0], coordinateTwo[0]]
    figure.add_trace(
        go.Scattermapbox(
            mode = "markers+lines",
            marker=dict(size=10, color='black'),
            lon = lons,
            lat = lats))      
        
def drawMap(airportOne, airportTwo):

    addressOne = geolocator.geocode(airportOne)
    addressTwo = geolocator.geocode(airportTwo)
    coordinatesOne = [addressOne.latitude, addressOne.longitude]
    coordinatesTwo = [addressTwo.latitude, addressTwo.longitude]

    figure = plotDots(coordinatesOne, coordinatesTwo)
    figure.update_layout(mapbox_style="open-street-map")
    drawEdges(figure, coordinatesOne, coordinatesTwo)  
    figure.update_layout(mapbox_style="open-street-map")
    figure.write_html('figura.html', auto_open=True) 

drawMap("Novi Sad, Serbia", "Zagreb, Hrvatska")