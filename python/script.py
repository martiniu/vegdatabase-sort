import requests
import json
from pprint import pprint
import webbrowser

# Drammen  -> Oslo
# 86512932 -> 86513964

# for veg_objekt in range(86512932, 86513964):
#   response = requests.get('https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583/'+str(veg_objekt)).json()
#   for egenskap in response['egenskaper']:
#     if egenskap['navn']=='Kjørebanebredde':
#       pprint(egenskap['verdi'])


# 0_0 Grønn
# 2_2 Rødt
# 1_0 Blå 
# 0_1 Blå?@


dekkebredde = input("Dekkebredde større enn: ")

base_url = "https://www.vegvesen.no/vegkart/vegkart/#kartlag:geodata"
edit_url = "/hva:(~(farge:'2_2,filter:(~(operator:'*3d,type_id:4566,verdi:(~5492)),(operator:'*3d,type_id:4568,verdi:(~18))),id:532),(farge:'0_1,filter:(~(operator:'*3e*3d,type_id:5555,verdi:(~"+str(dekkebredde)+"))),id:583))"
constant_url = "/hvor:(kommune:(~301,220,219,602,626))/@250164,6638305,9/vegobjekt:83641744:40a744:583"

webbrowser.open(base_url+edit_url+constant_url)