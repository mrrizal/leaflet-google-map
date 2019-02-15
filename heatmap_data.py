from pprint import pprint
import json
import os


def create_json():
    with open('DATA_IMSI_DAN_MSISDN/REKAP_LAPANGAN.csv', 'r') as f:
        list_data = [data.split(',') for data in f.read().split('\n')]
        result = {}
        for data in list_data:
            temp = {
                'kecamatan': data[6].replace(' ', '').lower(),
                'imsi': data[3],
                'msisdn': data[4]
            }

            try:
                temp['imsi'] = int(temp['imsi'])
            except ValueError:
                temp['imsi'] = 0

            try:
                temp['msisdn'] = int(temp['msisdn'])
            except ValueError:
                temp['msisdn'] = 0

            if temp['kecamatan'] not in result:
                result[temp['kecamatan']] = {
                    'imsi': temp['imsi'],
                    'msisdn': temp['msisdn']
                }
            else:
                result[temp['kecamatan']]['imsi'] += temp['imsi']
                result[temp['kecamatan']]['msisdn'] += temp['msisdn']

        pprint(result)
        print('jumlah data {}'.format(len(list_data)))

    with open('data_rekap.json', 'w') as f:
        json.dump(result, f, indent=True)


def open_geojson(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def save_geojson(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=True)


def update_geojson():
    # get data rekap
    with open('data_rekap.json', 'r') as f:
        data = json.load(f)

    list_geojson = os.listdir('geometry')

    for filename in list_geojson:
        kecamatan = filename.replace('.geojson', '')
        filename = 'geometry/{}'.format(filename)

        data_geojson = open_geojson(filename)

        if kecamatan in data:
            data_geojson['features'][0]['properties']['imsi'] = data[
                kecamatan]['imsi']
            data_geojson['features'][0]['properties']['msisdn'] = data[
                kecamatan]['msisdn']
        else:
            data_geojson['features'][0]['properties']['imsi'] = 0
            data_geojson['features'][0]['properties']['msisdn'] = 0

        save_geojson(filename, data_geojson)


if __name__ == '__main__':
    create_json()
    update_geojson()
