import requests
from pprint import pprint
import json


def loop_site(href):
    response = requests.get(href).json()


    # loops through all objects in json() called objekter
    for o in response['objekter']:

        # gets each href link inside of the object
        response_objekt = requests.get(o['href']).json()

        # loops through all object properties called egenskaper
        for egenskap in response_objekt['egenskaper']:

            # if the object property is called dekkebredde, print this value
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
        #pprint(vegobjekt)


    # if 1000 objects were returned, get the link to the next batch of objects
    if response['metadata']['returnert'] == 1000:
        response = requests.get(response['metadata']['neste']['href']).json()
        loop_site(response['metadata']['neste']['href'])


def write_to_file(link, filename):
    vegobjekt.clear()
    loop_site(link)

    with open(filename, 'w') as writeobject:
        json.dump(vegobjekt, writeobject)

def compare_lenkeid(file1, file2):
    with open(filename, 'r') as readobject:


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
