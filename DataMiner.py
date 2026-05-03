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
        debugMsg('File opened successfully.', True)
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
missingDate = 0
missingNormalAppts = 0
missingHouseVisits = 0
missingOtherAppts = 0

# Prepare the SQL tables
cursor.execute('DROP TABLE IF EXISTS SubRegion')
cursor.execute('''
                CREATE TABLE SubRegion(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                subRegion TEXT, 
                region_id INTEGER 
                )''')

cursor.execute('DROP TABLE IF EXISTS Region')
cursor.execute('''
                CREATE TABLE Region (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                region TEXT
                )''')

cursor.execute('DROP TABLE IF EXISTS SubRegDate') # The many-to-many relationship table that will match a subregion with a date of data
cursor.execute('''
                CREATE TABLE SubRegDate (
                subRegion_id INTEGER,
                date DATE,
                faceToFaceAppts INTEGER, 
                houseVisits INTEGER, 
                otherAppts INTEGER,
                PRIMARY KEY (subRegion_id, date)
                )''')

entryCount = 0 # To count the number of entries processed and time the write-to-file function

for entry in data:
    # Read and check the data from the JSON entry, and feed it to python variables, for use later. Assign illogical values to signal a read error.

    debugMsg('NEW ENTRY.', False)
    try: region = entry['fields']['regiao']
    except:
        debugMsg('<< Error on acquiring the region value >>', False)
        region = str(-1); missingRegion += 1

    try: subRegion = entry['fields']['entidade']
    except:
        debugMsg('<< Error on acquiring the subRegion value >>', False)
        subRegion = str(-1); missingSubRegion += 1

    try: date = entry['fields']['tempo']
    except:
        debugMsg('<< Error on acquiring the date value >>', False)
        date = datetime.date.fromisoformat('1500-01-01'); missingDate += 1

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
    '), in ' + str(date) +
    ' there where ' + str(normalAppts) + ' appointments; ' +
    str(houseVisits) + ' house visits and ' +
    str(otherAppts) + ' other appointments.', False)

    # Now we import the entry data to the SQL database!

    # Find out if this region is already on the Region table. Fetch its id if applicable.
    cursor.execute('SELECT * FROM Region WHERE region = ? ', (region,))
    row = cursor.fetchone()
    if row is None:  # Create an entry for that Region and fetch it id
        cursor.execute('INSERT INTO Region (region) VALUES (?)', (region,))
        cursor.execute('SELECT id FROM Region WHERE region = ? ', (region,))
        row = cursor.fetchone()
    region_id = row[0]

    # Find out if this subRegion is already on the SubRegion table. Fetch its id if applicable.
    cursor.execute('SELECT id FROM SubRegion WHERE subRegion = ? ', (subRegion,))
    row = cursor.fetchone()
    if row is None:  # Create a row for that subRegion and fetch it id
        cursor.execute('INSERT INTO SubRegion (subRegion, region_id) VALUES (?, ?)', (subRegion, region_id))
        cursor.execute('SELECT id FROM SubRegion WHERE subRegion = ? ', (subRegion,))
        row = cursor.fetchone()
    subRegion_id = row[0]

    # Convert the date into a SQL-friendly DATE variable. The JSON data holds the date variable in a string like "2026-04-29T12:11:39.530+02:00"
    date = date[:9]
    if len(date) < 9: date = date + '-01' # In case only the month is provided in this entry, I chose to place the data in the first day of the month.
    date = datetime.date.fromisoformat(date)

    # Now insert the data into the subRegDate table. Check if there is already a row with this subRegion and this date.
    cursor.execute('SELECT * FROM SubRegDate WHERE subRegion_id = ? AND date = ?', (subRegion_id, date))
    row = cursor.fetchone()
    if row is None:
        cursor.execute('INSERT INTO SubRegDate (subRegion_id, date, faceToFaceAppts, houseVisits, otherAppts) VALUES (?, ?, ?, ?, ?)', (subRegion_id, date, normalAppts, houseVisits, otherAppts))
    else:
        debugMsg('There was already an entry for the subregion named ' + subRegion + 'and the date ' + str(date) + '!!! Ignoring this entry.', True)

    # Write the cached data to the database file at every 1000th entry.
    entryCount += 1
    if entryCount % 1000 == 0:
        debugMsg('Saving cached data to the database file at entry number ' + str(entryCount), True)
        conn.commit()


debugMsg('Saving the final entries to the database file...', True)
conn.commit()
# Final debug report
debugMsg('\nFinal Report:' +
    '\nInstances of missing data for the region:' + str(missingRegion) +
    '\nInstances of missing data for the sub region:'+ str(missingSubRegion) +
    '\nInstances of missing data for the date:' + str(missingDate) +
    '\nInstances of missing data for the number of appointments:' + str(missingNormalAppts) +
    '\nInstances of missing data for the number of house visits:' + str(missingHouseVisits) +
    '\nInstances of missing data for the number of other appointments:' + str(missingOtherAppts), True)

debugMsg('\n ------- \n <<< END OF DEBUG LOG FOR CURRENT RUN >>> \n', False)

# Save the debug log in DataMiner_log.txt
debugFHand = open('DataMiner_log.txt', 'a')
debugFHand.write(debugString)

debugFHand.close()
cursor.close()
conn.close()