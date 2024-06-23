# exam group 3

# load packages
from pyqgis_scripting_ext.core import *

# folder paths
folder = 'C:/Users/timo/Documents/GitHub/advanced_geomatics/'
data_folder = folder + 'data/'
output_folder = folder + 'tmp/'

# load data
geopackagePath = data_folder + 'reduced_ne.gpkg'

countriesName = 'ne_50m_admin_0_countries'
countriesLayer = HVectorLayer.open(geopackagePath, countriesName)
countriesLayer.subset_filter("NAME = 'Italy' OR NAME = 'Germany'")

# rempve layers from map
HMap.remove_layers_by_name(['OpenStreetMap', 'ne_50m_admin_0_countries', 'Battles', 'Country borders'])



# import the http requests library to get stuff from the internet
import requests
# import the url parsing library to urlencode the query
import urllib.parse
# define the query to launch
endpointUrl = "https://query.wikidata.org/sparql?query=";
# define the query to launch
query = """
SELECT ?label ?coord
?subj ?year
WHERE
{
  ?subj wdt:P31 wd:Q178561 .
  {?subj wdt:P17 wd:Q38} UNION {?subj wdt:P17 wd:Q183}.
  ?subj wdt:P625 ?coord .
  OPTIONAL {?subj wdt:P580 ?d1}
  OPTIONAL {?subj wdt:P585 ?d2}
  OPTIONAL {?subj wdt:P582 ?d3}
  BIND(IF(!BOUND(?d1),(IF(!BOUND(?d2),?d3,?d2)),?d1) as ?date)
  BIND(YEAR(?date) as ?year)
  ?subj rdfs:label ?label filter (lang(?label) = "en")
}

"""
# URL encode the query string
encoded_query = urllib.parse.quote(query)
# prepare the final url
url = f"{endpointUrl}{encoded_query}&format=json"
# run the query online and get the produced result as a dictionary
r=requests.get(url)
result = r.json()
#print(result)

###########################################################################


# add OSM to map
osm = HMap.get_osm_layer()
HMap.add_layer(osm)

# crs transformation
crsHelper = HCrs()
crsHelper.from_srid(4326)
crsHelper.to_srid(3857)


# add countries to map

countriesStyle = HFill('128, 128, 128, 70') + HStroke('black', 0.5)


nameIndexCountries = countriesLayer.field_index('NAME')
countriesFeatures = countriesLayer.features()

countries = HVectorLayer.new('Country borders', 'MultiPolygon', 'EPSG:3857', {'NAME': 'String'})

for feature in countriesFeatures:
    if feature.attributes[nameIndexCountries]:
        countryName = feature.attributes[nameIndexCountries]
        countryGeometry = feature.geometry
    countries.add_feature(crsHelper.transform(countryGeometry), [countryName])


countries.set_style(countriesStyle)
HMap.add_layer(countries)


# create scheme

fields = {
    'NAME': 'String',
    'YEAR': 'Integer'
}

#battlesLayer = HVectorLayer.new('battles', 'Point', 'EPSG:4326', fields)
battlesLayer = HVectorLayer.new('Battles', 'Point', 'EPSG:3857', fields)

battlesInCountries = {}

counterItaly = 0
counterGermany = 0

for battle in result['results']['bindings']:
    name = battle['label']['value']
    coords = battle['coord']['value'].strip('Point(').strip(')').split(' ')
    #coordsSplit = battle['coord']['value'].strip(')').split('(')
    #coords = coordsSplit[1].split(' ')
    lon = float(coords[0])
    lat = float(coords[1])
    if 'year' in battle:
        year = int(battle['year']['value'])
    else:
        year = None
    
    location = HPoint(lon,lat)
    location3857 = crsHelper.transform(location)
    
    for feature in countriesFeatures:
        countryName = feature.attributes[nameIndexCountries]
        countryGeometry = feature.geometry
        
        
        if location.intersects(countryGeometry):
            
            battlesLayer.add_feature(location3857, [name, year])
            
            if year and 0 <= year <= 1000:
          
                if countryName == 'Italy':
                    counterItaly += 1
                
                else:
                    counterGermany += 1
            

    
path = output_folder + 'battles.gpkg'

error = battlesLayer.dump_to_gpkg(path, overwrite=True)

if error:
    print(error)
    
# styling

field = "if(YEAR >= 0 AND YEAR <=1000, NAME,'')"

labelProperties3 = {
    'font': 'Arial',
    'color': 'black',
    'size': 10,
    'field': field,
    'xoffset': 0,
    'yoffset': -8
}

labelStyle = HLabel(**labelProperties3) + HHalo('white', 2)

ranges = [
    [float('-inf'), 0],
    [1, 1000],
    [1001, 1500],
    [1501, float('inf')]
]


styles = [
    HMarker('circle', 2) + HFill('red') + HStroke('black', 0.1),
    HMarker('circle', 2) + HFill('blue') + HStroke('black', 0.1),
    HMarker('circle', 2) + HFill('green') + HStroke('black', 0.1),
    HMarker('circle', 2) + HFill('orange') + HStroke('black', 0.1)
    
]



#battlesLayer.set_graduated_style('year', ranges, styles, labelStyle)
battlesLayer.set_graduated_style('year', ranges, styles, )
HMap.add_layer(battlesLayer)


printer = HPrinter(iface)

countriesExtent = countries.bbox()
countriesExtent2 = []
for index, coord in enumerate(countriesExtent):
    if index <2:
        countriesExtent2.append(coord-50000)
    else:
        countriesExtent2.append(coord+50000)


mapProperties = {
    "x": 5,
    "y": 5,
    "width": 200,
    "height": 200,
    "extent": countriesExtent2,
    "frame": True
}
    
printer.add_map(**mapProperties)

labelProperties = {
    "x": 215,
    "y": 5,
    "text": "Battles in Italy\nand Germany",
    "font_size": 28,
    "bold": True,
    "font": 'Times New Roman'
}

printer.add_label(**labelProperties)

labelProperties2 = {
    "x": 215,
    "y": 100,
    "text": f"Battles from year 0 to 1000 in:\n- Italy: {counterItaly}\n- Germany: {counterGermany}",
    "font_size": 16,
    "bold": True,
    "font": 'Times New Roman'
}

printer.add_label(**labelProperties2)

legendProperties = {
    "x": 215,
    "y": 147,
    "width": 150,
    "height": 100,
    "max_symbol_size": 3
}

printer.add_legend(**legendProperties)

scalebarProperties = {
    "x": 10,
    "y": 190,
    "segments": 4,
    "unit_per_segment": 250,
    "style": 'Double Box',
    "font": 'Times New Roman'
    
}



printer.add_scalebar(**scalebarProperties)

outputPdf = f"{output_folder}final_map.pdf"
printer.dump_to_pdf(outputPdf)