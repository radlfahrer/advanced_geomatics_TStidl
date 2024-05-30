# creating new gpkg from natural_earth_vector.gpkg with only used layers

from pyqgis_scripting_ext.core import *

nat_earth_folder = 'C:/Users/timo/Documents/GitHub/advanced_geomatics/data/natural_earth_vector.gpkg/packages/'
geopackagePath = nat_earth_folder + 'natural_earth_vector.gpkg'
folder = 'C:/Users/timo/Documents/GitHub/advanced_geomatics/data/'
layers = ['ne_10m_admin_1_states_provinces', 'ne_50m_admin_0_countries', 'ne_50m_populated_places', 'ne_10m_rivers_lake_centerlines_scale_rank']

layer1 = 'ne_10m_admin_1_states_provinces'
layer2 = 'ne_50m_admin_0_countries'
layer3 = 'ne_50m_populated_places'
layer4 = 'ne_10m_rivers_lake_centerlines_scale_rank'

path = folder + 'reduced_ne.gpkg'

for i, layer in enumerate(layers):
    ne_layer = HVectorLayer.open(geopackagePath, layer)
    if i == 0:
        error = ne_layer.dump_to_gpkg(path, overwrite=True)
    else:
        error = ne_layer.dump_to_gpkg(path, overwrite=False)
    if error:
        print(error)