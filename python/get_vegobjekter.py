import requests
from pprint import pprint
import json


def loop_site(href):
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
        loop_site(response['metadata']['neste']['href'])


def write_to_file(link, filename):
    vegobjekt.clear()
    loop_site(link)

    with open(filename, 'w') as writeobject:
        json.dump(vegobjekt, writeobject)


def get_file(filename):
    with open(filename, 'r') as readobject:
        return json.load(readobject)


def get_veglenke_objekter(filename1, filename2):
    file1 = get_file(filename1)
    file2 = get_file(filename2)

    duplicate_free = {}

    for row_number, row_data in enumerate(file1): #bredde
        for row_number2, row_data2 in enumerate(file2): #felt
            if file1[row_data]['veglenkeid'] == file2[row_data2]['veglenkeid']:
                duplicate_free.update({file1[row_data]['veglenkeid']: "null"})
    return duplicate_free

def create_complete_dict(filename1, filename2):
    veglenke_objekter = get_veglenke_objekter(filename1, filename2)
    # ID = breddeobjekt && feltobjekt
    # 2345613 = {
    #   breddeobjekt{
    #       23984771 = 20.7 meter
    #       23984772 = 20.9 meter
    #   }
    #   feltobjekt{
    #       23451 = 3 felt
    #       23452 = 4 felt
    #   }
    # }
    file1 = get_file(filename1)
    file2 = get_file(filename2)

    breddeobjekter = {} # temporary breddeobjekt list
    #feltobjekter = {}   # temporary feltobjekt list
    #breddeobjekt = {}   # key: "breddeobjekt", value: (all temporary items in breddeobjekter)
    #feltobjekt = {}   # key: "feltobjekt", value: (all temporary items in feltobjekter)

    #veglenkeobjekt = []

    # for every new veglenkeid, empty a temporary list, then add all the
    # matches(dictionary style) found for that particular veglenkeid
    for o in veglenke_objekter: #veglenkeid
        breddeobjekter.clear()
        #breddeobjekt.clear()
        for row_number2, row_data2 in enumerate(file1): #bredde
            if o == file1[row_data2]['veglenkeid']:
                breddeobjekter[row_data2] = file1[row_data2]['dekkebredde']
                #print(breddeobjekter)

        # adds all breddeobjekter into a dictionary with the key breddeobjekt
        #breddeobjekt['breddeobjekt'] = breddeobjekter
        print(o, breddeobjekter)
        veglenke_objekter[o] = breddeobjekter
        #temp = {o: breddeobjekt}
        #veglenke_objekter.update(temp)
        #veglenke_objekter.update(breddeobjekt)

    #pprint(veglenke_objekter)

    for o in veglenke_objekter: #veglenkeid
        #feltobjekter.clear()
        # new veglenkeid
        for row_number2, row_data2 in enumerate(file2): #felt
            if o == file2[row_data2]['veglenkeid']:
                pass
                #feltobjekter[row_data2] = file2[row_data2]['ant_felt']
                # new feltobjekt
        #feltobjekt['feltobjekt'] = feltobjekter
        #print(feltobjekt)
        #print(o, " HAR VERDIENE: ", feltobjekter)
        #print()
    #print(veglenke_objekter)

    # for o in veglenke_objekter:
    #     print(o, veglenke_objekter[o])
    #     print()


if __name__ == '__main__':
    #feil_link = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583.json?egenskap="5555>=0"&overlapp=532(4566=5492 AND 4568=18 AND 4570=5506)&kommune=301&kommune=220&kommune=219&kommune=602&kommune=626'
    felt_link = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/482.json?kommune=301&kommune=220&kommune=219&kommune=602&kommune=626'
    dekkebredde_link = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583?kommune=301&kommune=220&kommune=219&kommune=602&kommune=626'
    vegref_link = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/532?egenskap="4566=5492 AND 4568=18 AND 4570=5506"&kommune=301&kommune=220&kommune=219&kommune=602&kommune=626'

    #vegobjekt = {}

    #write_to_file(feil_link, 'vegobjekter_feil.json')
    #write_to_file(felt_link, 'vegobjekter_felt.json')
    #write_to_file(dekkebredde_link, 'vegobjekter_dekkebredde.json')
    #write_to_file(vegref_link, 'vegobjekter_vegref.json')

    get_veglenke_objekter('vegobjekter_dekkebredde.json', 'vegobjekter_felt.json')
    create_complete_dict('vegobjekter_dekkebredde.json', 'vegobjekter_felt.json')
