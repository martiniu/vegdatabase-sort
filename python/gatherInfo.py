import requests
from pprint import pprint

#https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583.json?egenskap="5555<=16"&kommune=301&kommune=220&kommune=219&kommune=602&kommune=626&overlapp=532(4566=5492%20AND%204568=18%20AND%204570=5506)


response = requests.get('https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583?egenskap="5555<=16"&kommune=301&kommune=220&kommune=219&kommune=602&kommune=626&overlapp=532(4566=5492%20AND%204568=18%20AND%204570=5506)').json()
# for o in response['objekter']:
#     #print(o['id'])
#     response_inside = requests.get(o['href']).json()
#     for dekkebredde in response_inside['egenskaper']:
#         #pprint(dekkebredde)
#         if dekkebredde['navn'] == 'Dekkebredde':
#             print('Dekkebredde: ', dekkebredde['verdi'])
#print(response)
if response['metadata']['returnert'] == 1000:
    response_next = requests.get(response['metadata']['neste']['href']).json()
    print(response_next)
