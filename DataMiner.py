import json
import sqlite3

fhand = open("GPappointsdata.json")
data = json.loads(fhand.read())

conn = sqlite3.connect("GPappointsdata.db")
cursor = conn.cursor()

missingRegion = 0
missingSubRegion = 0
missingMonth = 0
missingNormalAppts = 0
missingHouseVisits = 0
missingOtherAppts = 0

for entry in data:
    print('NEW ENTRY.')
    try: region = entry['fields']['regiao']
    except: print('Error on acquiring the region value'); region = -1; missingRegion += 1

    try: subRegion = entry['fields']['entidade']
    except: print('Error on acquiring the subRegion value'); subRegion = -1; missingSubRegion += 1

    try: month = entry['fields']['tempo']
    except: print('Error on acquiring the month value'); month = -1; missingMonth += 1

    try: normalAppts = entry['fields']['no_de_consultas_medicas_presencias_qt']
    except: print('Error on acquiring the normalApptsvalue'); normalAppts = -1; missingNormalAppts += 1

    try: houseVisits = entry['fields']['no_de_consultas_medicas_ao_domicilio_qt']
    except: print('Error on acquiring the houseVisits value'); houseVisits = -1; missingHouseVisits += 1

    try: otherAppts = entry['fields']['no_de_consultas_medicas_nao_presenciais_ou_inespecificas_qt']
    except: print('Error on acquiring the otherAppts value'); otherAppts = -1; missingOtherAppts += 1

    # I checked manually; it appears some data is missing in the JSON file, hence the error fetching some field values.

    print('At', region, '(specifically', subRegion, '), in', month, 'there where', normalAppts, 'appointments;', houseVisits, 'house visits and', otherAppts, 'other appointments.')

print('Final Report:')
print('Instances of missing data for the region:', missingRegion)
print('Instances of missing data for the sub region:', missingSubRegion)
print('Instances of missing data for the month:', missingMonth)
print('Instances of missing data for the number of appointments:', missingNormalAppts)
print('Instances of missing data for the number of house visits:', missingHouseVisits)
print('Instances of missing data for the number of other appointments:', missingOtherAppts)


cursor.close()
