import requests
from pprint import pprint
import json
import copy


def create_object_from_href(href):
    response = requests.get(href).json()
    for o in response['objekter']:
        response_objekt = requests.get(o['href']).json()
        for egenskap in response_objekt['egenskaper']:
            # checks for properties that are relevant on the road (dekkebredde, ant kjørefelt, veglenkeid)
            if egenskap['navn'] == 'Dekkebredde':
                egenskaper =	{
                    "dekkebredde": egenskap['verdi'],
                }
            if egenskap['navn'] == 'Antall kjørefelt':
                egenskaper =    {
                    "ant_felt": egenskap['verdi'],
                }
            if egenskap['navn'] == 'Vegkategori':
                egenskaper = {
                    "vegkategori": egenskap['verdi'],
                }
            if egenskap['navn'] == 'Vegstatus':
                egenskaper['vegstatus'] = egenskap['verdi']
            if egenskap['navn'] == 'Vegnummer':
                egenskaper['vegnummer'] = egenskap['verdi']

        egenskaper['veglenkeid'] = response_objekt['lokasjon']['stedfestinger'][0]['veglenkeid']
        vegobjekt[o['id']] = egenskaper


    # if 1000 objects were returned, get the link to the next batch of objects and loop through it
    if response['metadata']['returnert'] == 1000:
        response = requests.get(response['metadata']['neste']['href']).json()
        create_object_from_href(response['metadata']['neste']['href'])

def write_href_to_file(link, filename):
    vegobjekt.clear()
    create_object_from_href(link)

    with open(filename, 'w') as writeobject:
        json.dump(vegobjekt, writeobject)

def get_file_as_json(filename):
    with open(filename, 'r') as readobject:
        return json.load(readobject)

def get_bredde(filename1, filename2, veglenkeid):
    file = get_file(filename1)
    veglenke_objekter = get_veglenke_objekter(filename1, filename2)

    for o in veglenke_objekter: #veglenkeid
        breddeobjekter = {}
        for row_number, breddeid in enumerate(file): #bredde
            if veglenkeid == file[breddeid]['veglenkeid']:
                breddeobjekter[breddeid] = file[breddeid]["dekkebredde"]
        return breddeobjekter

def get_felt(filename1, filename2, veglenkeid):
    file = get_file(filename2)
    veglenke_objekter = get_veglenke_objekter(filename1, filename2)

    for o in veglenke_objekter: #veglenkeid
        feltobjekter = {}
        for row_number, breddeid in enumerate(file): #felt
            if veglenkeid == file[breddeid]['veglenkeid']:
                feltobjekter[breddeid] = file[breddeid]["ant_felt"]
        return feltobjekter

def vegref_contains(o):
    file = get_file('vegobjekter_vegref.json')

    for row_number, row_data in enumerate(file):
        if o == file[row_data]['veglenkeid']:
            return True
    return False

def get_veglenke_objekter(filename1, filename2):
    file1 = get_file(filename1)
    file2 = get_file(filename2)

    empty_dict = {}

    for row_number, row_data in enumerate(file1): #bredde
        for row_number2, row_data2 in enumerate(file2): #felt
            if file1[row_data]['veglenkeid'] == file2[row_data2]['veglenkeid']:
                empty_dict.update({file1[row_data]['veglenkeid']: "null"})
    return empty_dict

def create_complete_dict(filename1, filename2):
    veglenke_objekter = get_veglenke_objekter(filename1, filename2)

    for o in veglenke_objekter:
        bredde = get_bredde(filename1, filename2, o)
        felt = get_felt(filename1, filename2, o)

        egenskaper = {
            "breddeobjekter": bredde,
            "feltobjekter": felt
        }

        veglenke_objekter[o] = egenskaper

    veglenke_filtrert = copy.deepcopy(veglenke_objekter)

    for o in veglenke_objekter:
        if vegref_contains(o) == True:
            pass
        else:
            del veglenke_filtrert[o]

    pprint(veglenke_filtrert)
    return veglenke_filtrert

def create_all_dekkebredder():
    oslo = get_file_as_json('files/dekkebredde_oslo.json')
    asker = get_file_as_json('files/dekkebredde_oslo.json')
    lier = get_file_as_json('files/dekkebredde_oslo.json')
    drammen = get_file_as_json('files/dekkebredde_oslo.json')
    bærum = get_file_as_json('files/dekkebredde_oslo.json')

    oslo.update(asker)
    oslo.update(lier)
    oslo.update(drammen)
    oslo.update(bærum)

    dekkebredder = copy.deepcopy(oslo)
    return dekkebredder

def write_dict_to_file(dict, filename):
    with open(filename, 'w') as writeobject:
        json.dump(dict, writeobject)

def write_all_files():
    dekkebredde_oslo = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583?kommune=301'
    dekkebredde_asker = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583?kommune=220'
    dekkebredde_lier = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583?kommune=626'
    dekkebredde_drammen = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583?kommune=602'
    dekkebredde_bærum = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583?kommune=219'

    write_href_to_file(dekkebredde_oslo, 'files/dekkebredde_oslo.json')
    write_href_to_file(dekkebredde_asker, 'files/dekkebredde_asker.json')
    write_href_to_file(dekkebredde_lier, 'files/dekkebredde_lier.json')
    write_href_to_file(dekkebredde_drammen, 'files/dekkebredde_drammen.json')
    write_href_to_file(dekkebredde_bærum, 'files/dekkebredde_bærum.json')

    dekkebredder = create_all_dekkebredder()
    write_dict_to_file(dekkebredder, 'files/dekkebredder.json')

if __name__ == '__main__':

    vegobjekt = {}
    #pprint(len(dekkebredder))

    #get_veglenke_objekter('vegobjekter_dekkebredde.json', 'vegobjekter_felt.json')
    #create_complete_dict('vegobjekter_dekkebredde.json', 'vegobjekter_felt.json')
