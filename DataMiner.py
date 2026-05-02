import json
import sqlite3
import datetime

# Define the header for the debug log and the function for printing info and/or logging info to the file
timeInfo = datetime.datetime.now()
debugString = '<< NEW ENTRY ON THE DEBUG LOG >>>\n' + ' Date and Time of current run: ' + str(timeInfo) + '\n ------- \n'

def debugMsg(msg, printAlso):
    if(printAlso): print(msg)
    global debugString
    debugString += '\n' + msg

# Prompt for a name file and open it
while True:
    datafile = input('Please insert the name of the data file you wish to import. (Leave empty for the default data file): ')
    if datafile == '': datafile = 'GPappointsdata.json'
    try:
        debugMsg('Opening file ' + str(datafile) + '...', True)
        fHand = open(datafile)
        debugMsg('File opened sucessfully.', True)
        break
    except: debugMsg('File ' + datafile + ' not found or impossible to open.', True)

# Import the file data to a JSON file
debugMsg('\nLoading the file data onto a JSON object...', True)
try:
    data = json.loads(fHand.read())
    debugMsg('JSON object loaded successfully.', True)

except:
    debugMsg('There was an error loading the data file onto the JSON object! Exiting...', True)
    exit(1)

# Attempt to create / open the .db file to hold the SQL database
debugMsg('\nCreating or opening the database file where the imported data will be stored...', True)
try:
    conn = sqlite3.connect("GPappointsdata.db")
    cursor = conn.cursor()
    debugMsg('Database file created / opened successfully.', True)

except:
    debugMsg('There was an error creating / opening the database file! Exiting...', True)
    exit(1)

missingRegion = 0
missingSubRegion = 0
missingMonth = 0
missingNormalAppts = 0
missingHouseVisits = 0
missingOtherAppts = 0

for entry in data:
    debugMsg('NEW ENTRY.', False)
    try: region = entry['fields']['regiao']
    except:
        debugMsg('<< Error on acquiring the region value >>', False)
        region = -1; missingRegion += 1

    try: subRegion = entry['fields']['entidade']
    except:
        debugMsg('<< Error on acquiring the subRegion value >>', False)
        subRegion = -1; missingSubRegion += 1

    try: month = entry['fields']['tempo']
    except:
        debugMsg('<< Error on acquiring the month value >>', False)
        month = -1; missingMonth += 1

    try: normalAppts = entry['fields']['no_de_consultas_medicas_presencias_qt']
    except:
        debugMsg('<< Error on acquiring the normalApptsvalue >>', False)
        normalAppts = -1; missingNormalAppts += 1

    try: houseVisits = entry['fields']['no_de_consultas_medicas_ao_domicilio_qt']
    except:
        debugMsg('<< Error on acquiring the houseVisits value >>', False)
        houseVisits = -1; missingHouseVisits += 1

    try: otherAppts = entry['fields']['no_de_consultas_medicas_nao_presenciais_ou_inespecificas_qt']
    except:
        debugMsg('<< Error on acquiring the otherAppts value >>', False)
        otherAppts = -1; missingOtherAppts += 1

    # I checked manually; it appears some data is missing in the JSON file, hence the error fetching some field values.

    debugMsg('At ' + region +
    ' (specifically ' + str(subRegion) +
    '), in ' + str(month) +
    ' there where ' + str(normalAppts) + ' appointments; ' +
    str(houseVisits) + ' house visits and ' +
    str(otherAppts) + ' other appointments.', False)


# Final debug report
debugMsg('\nFinal Report:' +
    '\nInstances of missing data for the region:' + str(missingRegion) +
    '\nInstances of missing data for the sub region:'+ str(missingSubRegion) +
    '\nInstances of missing data for the month:' + str(missingMonth) +
    '\nInstances of missing data for the number of appointments:' + str(missingNormalAppts) +
    '\nInstances of missing data for the number of house visits:' + str(missingHouseVisits) +
    '\nInstances of missing data for the number of other appointments:' + str(missingOtherAppts), True)

debugMsg('\n ------- \n <<< END OF DEBUG LOG FOR CURRENT RUN >>> \n', False)

# Save the debug log in DataMiner_log.txt
debugFHand = open('DataMiner_log.txt', 'a')
debugFHand.write(debugString)
debugFHand.close()

cursor.close()
