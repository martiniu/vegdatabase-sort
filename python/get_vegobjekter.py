import requests
from pprint import pprint
import json

# dictionary to store objectid and it's properties:
#       - dekkebredde
#       - veglenkeid

def loop_site(href):
    # gets internet site as .json()
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
                    "veglenkeid": response_objekt['lokasjon']['stedfestinger'][0]['veglenkeid']
                }
            if egenskap['navn'] == 'Antall kjørefelt':
                egenskaper =    {
                    "ant_felt": egenskap['verdi'],
                    "veglenkeid": response_objekt['lokasjon']['stedfestinger'][0]['veglenkeid']
                }
        vegobjekt[o['id']] = egenskaper
        #pprint(vegobjekt)


    # if 1000 objects were returned, get the link to the next batch of objects
    if response['metadata']['returnert'] == 1000:
        response = requests.get(response['metadata']['neste']['href']).json()
        loop_site(response['metadata']['neste']['href'])

if __name__ == '__main__':
    vegbredde = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583.json?egenskap="5555>=0"&kommune=301&kommune=220&kommune=219&kommune=602&kommune=626&overlapp=532(4566=5492 AND 4568=18 AND 4570=5506)'
    felt = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/482.json?egenskap="5192>=0"&kommune=301&kommune=220&kommune=219&kommune=602&kommune=626&overlapp=532(4566=5492 AND 4568=18 AND 4570=5506)'

    #vegobjekt = {}
    #loop_site(vegbredde)

    #with open('vegobjekter_vegbredde.json', 'w') as writeobject:
    #    json.dump(vegobjekt, writeobject)

    vegobjekt = {}
    loop_site(felt)

    with open('vegobjekter_felt.json', 'w') as writeobject:
        json.dump(vegobjekt, writeobject)
