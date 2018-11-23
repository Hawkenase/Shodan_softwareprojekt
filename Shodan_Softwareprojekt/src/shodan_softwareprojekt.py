import shodan
import argparse
import folium
from colorama import Fore
from folium.plugins import MarkerCluster
from geopy import distance
from geopy.geocoders import Nominatim

coordinates = 0
address = 0
# create Shodan API
SHODAN_API_KEY = "V8kcW56VkPG3xF5modxydH45wPY0W7ft"

api = shodan.Shodan(SHODAN_API_KEY)

# Wrap the request in a try/ except block to catch errors

        #Eingabe User
query = input("Bitte geben Sie ihre Anfrage ein: ")
        # Search Shodan
try:     
    results = api.search(query)
except:
    print('Erro While Searchingr: {}')
   
# If results > 0, show results and put them into .txt file
if len(results['matches']) > 0:
    print('Results found: {}'.format(results['total']))
    print("Daten wurden in Ergebnis.txt abgespeichert.")
    for result in results['matches']:
        file = open("Ergebnis.txt","a")
        #file.write("/n. result")
        file.write('\nIP: {}'.format(result['ip_str']))
        file.write('\nPort: {}'.format(result['port']))
        file.write('\nOrganisation: {}'.format(result['org']))
        file.write('\nBetriebsystem: {}'.format(result['os']))
        file.write('\nLand: {}'.format(result['location']))
        file.write('')
        file.write('\n')
else:
    print ("Nothing was found.")
    sys.exit()   
         
    #zeichne Map mit drei Werten
def draw_map(results, first_coordinates, filename):
    tile = "OpenStreetMap"
    if dark:
        tile = "CartoDB dark_matter"
        
    repeats = []
    
    # erstelle Map mit Location 
    folium_map = folium.Map(location=[first_coordinates[0], first_coordinates[1]],zoom_start=12,tiles=tile)                     
    marker = folium.CircleMarker(location=[first_coordinates[0], first_coordinates[1]])
    marker.add_to(folium_map)
    marker_cluster = MarkerCluster().add_to(folium_map)
    coordinates = []
    first_coordinates_measure = (first_coordinates[0], first_coordinates[1])
    
    # solange es Kameras gibt hol IP, Product, Koordinaten
    for counter, camera in enumerate(results['matches']):
        ip = camera['ip_str']
        product = camera['product']

        coordinates.append(camera['location']['latitude'])
        coordinates.append(camera['location']['longitude'])

        if "200 OK" not in camera['data']:
            color = "red"
        else:
            color = "green"
        
        #gib bei Maker IP und Koordinaten aus
        print ("(IP: ") + Fore.GREEN + ip + Fore.RESET
        print ("Coordinates: ") + Fore.BLUE + str(camera['location']['latitude']) + "," + Fore.BLUE + str(
            camera['location']['longitude']) + Fore.RESET
        print ("-----------------------------------")
        
        #ermittle Distanzen zwischen results
        coordinates_measure = (camera['location']['latitude'], camera['location']['longitude'])
        distance_compare = distance.distance(first_coordinates_measure, coordinates_measure).m
        unit = "m"
        if distance_compare > 1000.0:
            distance_compare = distance_compare / 1000
            unit = "km"

        if coordinates in repeats:
            folium.Marker([camera['location']['latitude'], camera['location']['longitude']], popup=ip + "<br>" + product + "<br>" + str(distance_compare)[0:5] + "" + unit + " from target",icon=folium.Icon(color=color)).add_to(marker_cluster)
        else:
            folium.Marker([camera['location']['latitude'], camera['location']['longitude']], popup=ip + "<br>" + product + "<br>" + str(distance_compare)[0:5] + unit + " from target",icon=folium.Icon(color=color)).add_to(folium_map)

        repeats.append(coordinates)  # make list of lists of coordinates
        coordinates = []

    print ("Saving map as ") + filename + '.html'
    folium_map.save(filename + ".html")


if coordinates:
    geolocator = Nominatim(user_agent="Kamerka")
    try:
        location = geolocator.reverse(coordinates, language='en')
        if location.address is None:
            print ("Nothing was found")
            sys.exit()
    except:
        print ("No address was found")
        sys.exit()

    print (location.address)

    query_cameras = "geo:" + coordinates + "," + radius + " device:webcam"

    split_coordinates = coordinates.split(',')
    converted_coordinates = [float(i) for i in split_coordinates]
    cameras = shodan_query(query_cameras)
    draw_map(cameras, converted_coordinates, coordinates)
    sys.exit()
if address:
    geolocator = Nominatim(user_agent="test")
    location = geolocator.geocode(address)
    try:
        print (location.address)
    except Exception as e:
        print ("Nothing was found, correct your address")
        sys.exit()

    coordinates = [location.latitude, location.longitude]
    query_cameras = "geo:" + str(location.latitude) + "," + str(location.longitude) + "," + radius + " device:webcam"
    cameras = shodan_query(query_cameras)
    draw_map(cameras, coordinates, address)
       
       
        

