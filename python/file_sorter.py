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
            # dekkebredde, ant kjørefelt, veglenkeid
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

def write_dict_to_file(dict, filename):
    with open(filename, 'w') as writeobject:
        json.dump(dict, writeobject)

# def get_bredde(filename1, filename2, veglenkeid):
#     file = get_file(filename1)
#     veglenke_objekter = get_veglenke_objekter(filename1, filename2)
#
#     for o in veglenke_objekter: #veglenkeid
#         breddeobjekter = {}
#         for row_number, breddeid in enumerate(file): #bredde
#             if veglenkeid == file[breddeid]['veglenkeid']:
#                 breddeobjekter[breddeid] = file[breddeid]["dekkebredde"]
#         return breddeobjekter

# def get_felt(filename1, filename2, veglenkeid):
#     file = get_file(filename2)
#     veglenke_objekter = get_veglenke_objekter(filename1, filename2)
#
#     for o in veglenke_objekter: #veglenkeid
#         feltobjekter = {}
#         for row_number, breddeid in enumerate(file): #felt
#             if veglenkeid == file[breddeid]['veglenkeid']:
#                 feltobjekter[breddeid] = file[breddeid]["ant_felt"]
#         return feltobjekter

# def vegref_contains(o):
#     file = get_file('old_files/vegobjekter_vegref.json')
#
#     for row_number, row_data in enumerate(file):
#         if o == file[row_data]['veglenkeid']:
#             return True
#     return False

# def get_veglenke_objekter(filename1, filename2):
#     file1 = get_file(filename1)
#     file2 = get_file(filename2)
#
#     empty_dict = {}
#
#     for row_number, row_data in enumerate(file1): #bredde
#         for row_number2, row_data2 in enumerate(file2): #felt
#             if file1[row_data]['veglenkeid'] == file2[row_data2]['veglenkeid']:
#                 empty_dict.update({file1[row_data]['veglenkeid']: "null"})
#     return empty_dict

# def create_complete_dict(filename1, filename2):
#     veglenke_objekter = get_veglenke_objekter(filename1, filename2)
#
#     for o in veglenke_objekter:
#         bredde = get_bredde(filename1, filename2, o)
#         felt = get_felt(filename1, filename2, o)
#
#         egenskaper = {
#             "breddeobjekter": bredde,
#             "feltobjekter": felt
#         }
#
#         veglenke_objekter[o] = egenskaper
#
#     veglenke_filtrert = copy.deepcopy(veglenke_objekter)
#
#     for o in veglenke_objekter:
#         if vegref_contains(o) == True:
#             pass
#         else:
#             del veglenke_filtrert[o]
#
#     pprint(veglenke_filtrert)
#     return veglenke_filtrert

def create_all_dekkebredder():
    oslo = get_file_as_json('files/dekkebredde_oslo.json')
    asker = get_file_as_json('files/dekkebredde_asker.json')
    lier = get_file_as_json('files/dekkebredde_lier.json')
    drammen = get_file_as_json('files/dekkebredde_drammen.json')
    bærum = get_file_as_json('files/dekkebredde_bærum.json')

    oslo.update(asker)
    oslo.update(lier)
    oslo.update(drammen)
    oslo.update(bærum)

    dekkebredder = copy.deepcopy(oslo)
    return dekkebredder

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


def write_all_dekkebredder():
    dekkebredde_oslo = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583?fylke=3'
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
    write_dict_to_file(felt, 'files/felt.json')

def merge_dekkebredde_felt():
    dekkebredder = get_file_as_json('files/dekkebredder.json')
    felt = get_file_as_json('files/felt.json')

    dekkebredder_med_felt = copy.deepcopy(dekkebredder)

    for d in dekkebredder:
        for f in felt:
            if dekkebredder_med_felt[d]['veglenkeid'] == felt[f]['veglenkeid']:
                dekkebredder_med_felt[d]['ant_felt'] = felt[f]['ant_felt']

    test_merge = copy.deepcopy(dekkebredder_med_felt)
    write_dict_to_file(test_merge, 'files/merge_dekke_felt.json')

def write_all_E18():
    vegref = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/532?egenskap=(4566=5492 AND 4568=18 AND 4570=5506)'

    write_href_to_file(vegref, 'files/vegref.json')


def merge_dekkebredde_felt_vegref():
    merge = get_file_as_json('files/merge_dekke_felt.json')
    vegref = get_file_as_json('files/vegref.json')

    merge_final = copy.deepcopy(merge)

    for m in merge:
        for v in vegref:
            if merge_final[m]['veglenkeid'] == vegref[v]['veglenkeid']:
                merge_final[m]['vegkategori'] = vegref[v]['vegkategori']
                merge_final[m]['vegnummer'] = vegref[v]['vegnummer']
                merge_final[m]['vegstatus'] = vegref[v]['vegstatus']


    final_merge = copy.deepcopy(merge_final)
    write_dict_to_file(final_merge, 'files/final_merge.json')

def filter_out_nonvegref():
    final = get_file_as_json('files/final_merge.json')

    final_copy = copy.deepcopy(final)

    for f in final:
        #pprint(final)
        if 'vegkategori' in final[f]:
            pass
        else:
            del final_copy[f]

    write_dict_to_file(final_copy, 'files/final_filtered.json')

if __name__ == '__main__':

    vegobjekt = {}

    # write_all_dekkebredder()
    # write_all_felt()
    # merge_dekkebredde_felt()
    # write_all_E18()
    # merge_dekkebredde_felt_vegref()
    #filter_out_nonvegref()

    #get_veglenke_objekter('vegobjekter_dekkebredde.json', 'vegobjekter_felt.json')
    #create_complete_dict('vegobjekter_dekkebredde.json', 'vegobjekter_felt.json')
