import json
import geojson
from functools import partial
import pyproj
import shapely.geometry
import shapely.ops
from pprint import pprint
from geojson import FeatureCollection


def merge_geojson(filename1, filename2, outputfilename):
    # reading into two geojson objects, in a GCS (WGS84)
    with open(filename1) as geojson1:
        poly1_geojson = json.load(geojson1)

    with open(filename2) as geojson2:
        poly2_geojson = json.load(geojson2)

    poly1 = shapely.geometry.asShape(poly1_geojson['features'][0]['geometry'])
    poly1_properties = poly1_geojson['features'][0]['properties']
    poly2 = shapely.geometry.asShape(poly2_geojson['features'][0]['geometry'])
    poly2_properties = poly2_geojson['features'][0]['properties']

    properties = {
        'PROPINSI':
        poly1_properties['PROPINSI'],
        'KECAMATAN':
        '{} - {}'.format(poly1_properties['KECAMATAN'],
                         poly2_properties['KECAMATAN']),
        'KAB_KOTA':
        poly1_properties['KAB_KOTA'],
        'imsi':
        int(poly1_properties['imsi']) + int(poly2_properties['imsi']),
        'msisdn':
        int(poly1_properties['msisdn']) + int(poly2_properties['msisdn']),
        'tipe':
        'kecamatan'
    }
    mergedPolygon = poly1.union(poly2)
    geojson_out = geojson.Feature(
        geometry=mergedPolygon, properties=properties)

    feature_collection = FeatureCollection([geojson_out])

    # outputting the updated geojson file - for mapping/storage in its GCS format
    with open(outputfilename, 'w') as outfile:
        json.dump(feature_collection, outfile, indent=1)


if __name__ == '__main__':
    merge_geojson('geometry/pasarminggu.geojson', 'geometry/jagakarsa.geojson',
                  'geometry/pasarminggu_jagakarsa.geojson')