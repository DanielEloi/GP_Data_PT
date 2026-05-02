import json
import sqlite3

# Prompt for a name file and open it
while True:
    datafile = input('Please insert the name of the data file you wish to import. (Leave empty for the default data file): ')
    if datafile == '': datafile = 'GPappointsdata.json'
    try:
        print('Opening file ' + datafile + '...')
        fhand = open(datafile);
        print('File opened sucessfully.')
        break
    except: print('File not found or impossible to open.')

debug = True

# Ask if user wishes a debug log
while True:
    debFlag = input('\nDo you wish to have the full debug console prints? (y/n):')
    if debFlag == 'y':
        debug = True
        break
    if debFlag == 'n':
        debug = False
        break
    print('Please type only \'y\' or \'n\' for an option.')

# Import the file data to a JSON file
print('\nLoading the file data onto a JSON object...')
try:
    data = json.loads(fhand.read())
    print('JSON object loaded successfully.')

except:
    print('There was an error loading the data file onto the JSON object!')
    exit(1)

# Attempt to create / open the .db file to hold the SQL database
print('\nCreating or opening the database file where the imported data will be stored...')
try:
    conn = sqlite3.connect("GPappointsdata.db")
    cursor = conn.cursor()
    print('Database file created / opened successfully.')

except:
    print('There was an error creating / opening the database file')
    exit(1)

missingRegion = 0
missingSubRegion = 0
missingMonth = 0
missingNormalAppts = 0
missingHouseVisits = 0
missingOtherAppts = 0

for entry in data:
    if(debug): print('NEW ENTRY.')
    try: region = entry['fields']['regiao']
    except:
        if(debug): print('<< Error on acquiring the region value >>')
        region = -1; missingRegion += 1

    try: subRegion = entry['fields']['entidade']
    except:
        if(debug): print('<< Error on acquiring the subRegion value >>')
        subRegion = -1; missingSubRegion += 1

    try: month = entry['fields']['tempo']
    except:
        if(debug): print('<< Error on acquiring the month value >>')
        month = -1; missingMonth += 1

    try: normalAppts = entry['fields']['no_de_consultas_medicas_presencias_qt']
    except:
        if(debug): print('<< Error on acquiring the normalApptsvalue >>')
        normalAppts = -1; missingNormalAppts += 1

    try: houseVisits = entry['fields']['no_de_consultas_medicas_ao_domicilio_qt']
    except:
        if(debug): print('<< Error on acquiring the houseVisits value >>')
        houseVisits = -1; missingHouseVisits += 1

    try: otherAppts = entry['fields']['no_de_consultas_medicas_nao_presenciais_ou_inespecificas_qt']
    except:
        if(debug): print('<< Error on acquiring the otherAppts value >>')
        otherAppts = -1; missingOtherAppts += 1

    # I checked manually; it appears some data is missing in the JSON file, hence the error fetching some field values.

    if(debug): print('At', region, '(specifically', subRegion, '), in', month, 'there where', normalAppts, 'appointments;', houseVisits, 'house visits and', otherAppts, 'other appointments.')


# Final debug report
if(debug):
    print('Final Report:')
    print('Instances of missing data for the region:', missingRegion)
    print('Instances of missing data for the sub region:', missingSubRegion)
    print('Instances of missing data for the month:', missingMonth)
    print('Instances of missing data for the number of appointments:', missingNormalAppts)
    print('Instances of missing data for the number of house visits:', missingHouseVisits)
    print('Instances of missing data for the number of other appointments:', missingOtherAppts)


cursor.close()
