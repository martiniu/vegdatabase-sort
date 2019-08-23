import requests
from pprint import pprint
import json

#https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583.json?egenskap="5555<=16"&kommune=301&kommune=220&kommune=219&kommune=602&kommune=626&overlapp=532(4566=5492%20AND%204568=18%20AND%204570=5506)

vegbredde_objekt = {}


def loop_site(href):
    # gets internet site as .json()
    response = requests.get(href).json()

    # loops through all objects in json() called objekter
    for o in response['objekter']:

        # gets each href link inside of the object
        response_inside = requests.get(o['href']).json()

        # loops through all object properties called egenskaper
        for dekkebredde in response_inside['egenskaper']:
            egenskaper_objekt = {}

            # if the object property is called dekkebredde, print this value
            if dekkebredde['navn'] == 'Dekkebredde':
                dekkebredde_objekt = {}
                egenskaper_objekt.update({'Dekkebredde': dekkebredde['verdi']})
                #egenskaper_objekt.append(dekkebredde_objekt)

                #egenskaper_objekt[o['id']] = dekkebredde_objekt

            veglenke_objekt = {}
            egenskaper_objekt.update({'Veglenkeid': response_inside['lokasjon']['stedfestinger'][0]['veglenkeid']})
            #egenskaper_objekt.append(veglenke_objekt)

            vegbredde_objekt.update({o['id'] : egenskaper_objekt})



    # if 1000 objects were returned, get the link to the next batch of objects
    if response['metadata']['returnert'] == 1000:
        response = requests.get(response['metadata']['neste']['href']).json()
        #print("NEXT:", response['metadata']['neste']['href'])
        #print("------- Next page ------>")
        loop_site(response['metadata']['neste']['href'])
    else:
        #print("Returned: ", response['metadata']['returnert'])
        pass

if __name__ == '__main__':
    start_href = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583?egenskap="5555>=23"&kommune=301&kommune=220&kommune=219&kommune=602&kommune=626&overlapp=532(4566=5492%20AND%204568=18%20AND%204570=5506)'
    loop_site(start_href)
    #pprint(vegbredde_objekt)
    pprint(vegbredde_objekt)


    # with open('vegobjekter.json', 'w') as writeobject:
    #     json.dump(vegbredde_objekt, writeobject)
    # #asd = json.dumps(vegbredde_objekt)
    #
    #
    # with open('vegobjekter.json','r') as readobject:
    #     output = readobject.read()
    #     for o in output['dekkebredde']:
    #         pass
