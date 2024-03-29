import requests
from pprint import pprint
import json
import copy


def create_object_from_href(href):
    """
    Finds every object and each object's properties for each property that we
    are interested in. Saves info to a new object.

    Eg.
    Objectid {
        egenskaper:
            {
            dekkebredde: 22.7
            ant_kjørefelt: 4
            }
    }
    """

    response = requests.get(href).json()    # fetch query search as a .json file
    for o in response['objekter']:
        response_objekt = requests.get(o['href']).json()
        for egenskap in response_objekt['egenskaper']:
            if egenskap['navn'] == 'Dekkebredde':
                egenskaper =	{
                    "dekkebredde": egenskap['verdi'],
                }
            if egenskap['navn'] == 'Antall kjørefelt':
                egenskaper =    {
                    "ant_felt": egenskap['verdi'],
                }

        egenskaper['veglenkeid'] = response_objekt['lokasjon']['stedfestinger'][0]['veglenkeid']
        vegobjekt[o['id']] = egenskaper


    # whenever the query search returns, it caps at 1000 objects and pastes a link
    # to the "rest" of the objects, if 1000 objects were returned, we will continue
    # to read more objects
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

def write_all_felt():
    """
    Creates a superfile that writes every "ant_felt" to a superfile.
    """

    query_felt = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/482?egenskap="5192>=0"&vegreferanse=Ev18hp1-hp49&kommune=301&kommune=220&kommune=219&kommune=602&kommune=626'

    write_href_to_file(query_felt, 'files/query_felt.json')

def write_query_vegref():
    # writes the main "big" query to avoid a million files to sort and compare
    query_vegref = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583?egenskap="5555>=0"&vegreferanse=Ev18hp1-hp49&kommune=301&kommune=220&kommune=219&kommune=602&kommune=626'

    write_href_to_file(query_vegref, 'files/query_vegref_uten_felt.json')

def merge_query_vegref_felt():
    """
    Merges the "big" query and the superfile with "ant_felt" as a common denominator.
    """

    query_vegref = get_file_as_json('files/query_vegref_uten_felt.json')
    felt = get_file_as_json('files/query_felt.json')

    query_vegref_copy = copy.deepcopy(query_vegref)

    # connects each object by "veglenkeid" and adds every valid "ant_felt" to
    # a list to place into yet another custom object file

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
