import requests
from pprint import pprint
import json
import copy


def create_object_from_href(href):
    response = requests.get(href).json()
    for o in response['objekter']:
        response_objekt = requests.get(o['href']).json()
        for egenskap in response_objekt['egenskaper']:
            # checks for properties that are relevant on the road
            # dekkebredde, ant_felt and veglenkeid
            if egenskap['navn'] == 'Dekkebredde':
                egenskaper =	{
                    "dekkebredde": egenskap['verdi'],
                }
            if egenskap['navn'] == 'Antall kjørefelt':
                egenskaper =    {
                    "ant_felt": egenskap['verdi'],
                }
            # if egenskap['navn'] == 'Vegkategori':
            #     egenskaper = {
            #         "vegkategori": egenskap['verdi'],
            #     }
            # if egenskap['navn'] == 'Vegstatus':
            #     egenskaper['vegstatus'] = egenskap['verdi']
            # if egenskap['navn'] == 'Vegnummer':
            #     egenskaper['vegnummer'] = egenskap['verdi']

        egenskaper['veglenkeid'] = response_objekt['lokasjon']['stedfestinger'][0]['veglenkeid']
        vegobjekt[o['id']] = egenskaper


    # if 1000 objects were returned, get the link to the next batch of objects and loop through it
    if response['metadata']['returnert'] == 1000:
        create_object_from_href(response['metadata']['neste']['href'])

def write_href_to_file(link, filename):
    vegobjekt.clear()
    create_object_from_href(link)

    with open(filename, 'w') as writeobject:
        json.dump(vegobjekt, writeobject)

def get_file_as_json(filename):
    with open(filename, 'r') as readobject:
        return json.load(readobject)

def write_dict_to_file(dict, filename):
    with open(filename, 'w') as writeobject:
        json.dump(dict, writeobject)

def create_all_felt():
    oslo = get_file_as_json('files/felt_oslo.json')
    asker = get_file_as_json('files/felt_asker.json')
    lier = get_file_as_json('files/felt_lier.json')
    drammen = get_file_as_json('files/felt_drammen.json')
    bærum = get_file_as_json('files/felt_bærum.json')

    oslo.update(asker)
    oslo.update(lier)
    oslo.update(drammen)
    oslo.update(bærum)

    felt = copy.deepcopy(oslo)
    return felt

def write_all_felt():
    felt_oslo = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/482?fylke=3'
    felt_asker = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/482?kommune=220'
    felt_lier = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/482?kommune=626'
    felt_drammen = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/482?kommune=602'
    felt_bærum = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/482?kommune=219'

    write_href_to_file(felt_oslo, 'files/felt_oslo.json')
    write_href_to_file(felt_asker, 'files/felt_asker.json')
    write_href_to_file(felt_lier, 'files/felt_lier.json')
    write_href_to_file(felt_drammen, 'files/felt_drammen.json')
    write_href_to_file(felt_bærum, 'files/felt_bærum.json')

    felt = create_all_felt()
    write_dict_to_file(felt, 'files/felt_alle.json')

def write_query_vegref():
    query_vegref = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583?egenskap="5555>=0"&vegreferanse=EV18&kommune=301&kommune=220&kommune=219&kommune=602&kommune=626'

    write_href_to_file(query_vegref, 'files/query_vegref_uten_felt.json')

def merge_query_vegref_felt():
    query_vegref = get_file_as_json('files/query_vegref_uten_felt.json')
    felt = get_file_as_json('files/felt_alle.json')

    query_vegref_copy = copy.deepcopy(query_vegref)

    for d in query_vegref:
        felt_liste = []
        for f in felt:
            if query_vegref_copy[d]['veglenkeid'] == felt[f]['veglenkeid']:
                # legg til alle antall felt i en midlertidlig liste per dekkebredde objekt
                felt_liste.append(felt[f]['ant_felt'])

        felt_liste = list(dict.fromkeys(felt_liste))
        query_vegref_copy[d]['ant_felt'] = felt_liste

    test_merge = copy.deepcopy(query_vegref_copy)
    write_dict_to_file(test_merge, 'files/query_vegref_med_felt.json')


if __name__ == '__main__':

    vegobjekt = {}

    write_all_felt()
    write_query_vegref()
    merge_query_vegref_felt()
