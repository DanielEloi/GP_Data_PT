import sqlite3

# Define the header for the debug log and the function for printing info and/or logging info to the file

debugString = '<< START OF THE DATA QUERY SCRIPT >>>\n'

def debugMsg(msg, printAlso):
    if(printAlso): print(msg)
    global debugString
    debugString += '\n' + msg

def queryForMonths(month1, month2, month3, year, SQLcursor): # Returns a tuple with the sum of face to face appointments, house visits and other appointments in the designated months
    SQLcursor.execute(
        '''
        SELECT
            SUM(faceToFaceAppts) AS totalF2F,
            SUM(houseVisits)     AS totalHouse,
            SUM(otherAppts)      AS totalOther
        FROM SubRegDate
        WHERE date LIKE ?
          AND substr(date, 6, 2) IN (?, ?, ?) 
        ''',
        (f'{year}-%', str(month1), str(month2), str(month3))
    )
    row = SQLcursor.fetchall()
    return row[0]

# Prompt for a name file and open it
while True:
    dbfile = input('Please insert the name of the SQL database file you wish to import. (Leave empty for the default SQL database file): ')
    if dbfile == '': dbfile = 'GPappointsdata.db'
    try:
        debugMsg('Opening file ' + str(dbfile) + '...', True)
        fHand = open(dbfile)
        debugMsg('File opened successfully.', True)
        break
    except: debugMsg('File ' + dbfile + ' not found or impossible to open.', True)

# Attempt to open the SQL .db database file
debugMsg('\nConnecting to the SQL database file...', True)
try:
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    debugMsg('Database file connected successfully.', True)

except:
    debugMsg('There was an error connecting to the database file! Exiting...', True)
    exit(1)

# Now the SQL queries
# Table 1: Each type of appointment total for each year, and percentage of appointments in unspecified area
print('\n<< STARTING WORK ON TABLE 1 - Each type of appointment total for each year, and percentage of appointments in unspecified area. >> ')
totalF2F = dict()
totalHouseVisits = dict()
totalOtherAppts = dict()

unknownF2F = dict()
unknownHouseVisits = dict()
unknownOtherAppts = dict()

# Fetch the id of the subRegion for data with no designated location
cursor.execute('SELECT id FROM SubRegion WHERE subRegion = "Desconhecido | Nacional"')
row = cursor.fetchone()
unknownSubReg_id = row[0]

print('Collecting the total appointments per year and per type. Keeping track of the records with no location assigned.')

# Create and prepare the first row of the buffer string that will be used to write Table1 to the CSV file
table1 = 'Year, F2F appointments, % with unspecified area, House visits, % with unspecified area, Other appointments, % with unspecified area'
for year in range(2018, 2026):
    # House visits and other appointments sometimes have the value "-1" assigned, which flagged an absence of data in the original file. We disregard the entries with subzero values for that reason.
    cursor.execute('SELECT SUM(faceToFaceAppts) FROM SubRegDate WHERE faceToFaceAppts > 0 AND date LIKE ?',(f'{year}%',)) # To match with a regular expression, we use LIKE instead of '=' in SQL. Constructing this regular expression was challenging; I had help from AI.
    row = cursor.fetchone()
    totalF2F[year] = row[0]
    if totalF2F[year] == None: totalF2F[year] = 0 # We will be doing percentage calculations, so we need all data to be a number.

    cursor.execute('SELECT SUM(houseVisits) FROM SubRegDate WHERE houseVisits > 0 AND date LIKE ?',(f'{year}%',))
    row = cursor.fetchone()
    totalHouseVisits[year] = row[0]
    if totalHouseVisits[year] == None: totalHouseVisits[year] = 0

    cursor.execute('SELECT SUM(otherAppts) FROM SubRegDate WHERE otherAppts > 0 AND date LIKE ?', (f'{year}%',))
    row = cursor.fetchone()
    totalOtherAppts[year] = row[0]
    if totalOtherAppts[year] == None: totalOtherAppts[year] = 0

    cursor.execute('SELECT SUM(faceToFaceAppts) FROM SubRegDate WHERE faceToFaceAppts > 0 AND date LIKE ? AND subRegion_id = ?',(f'{year}%', unknownSubReg_id))
    row = cursor.fetchone()
    unknownF2F[year] = row[0]
    if unknownF2F[year] == None: unknownF2F[year] = 0

    cursor.execute('SELECT SUM(houseVisits) FROM SubRegDate WHERE houseVisits > 0 AND date LIKE ? AND subRegion_id = ?', (f'{year}%', unknownSubReg_id))
    row = cursor.fetchone()
    unknownHouseVisits[year] = row[0]
    if unknownHouseVisits[year] == None: unknownHouseVisits[year] = 0

    cursor.execute('SELECT SUM(otherAppts) FROM SubRegDate WHERE otherAppts > 0 AND date LIKE ?  AND subRegion_id = ?', (f'{year}%', unknownSubReg_id))
    row = cursor.fetchone()
    unknownOtherAppts[year] = row[0]
    if unknownOtherAppts[year] == None: unknownOtherAppts[year] = 0

    table1 += ('\n' + str(year) + ', ' +
                str(totalF2F[year]) + ', ' +
                str(unknownF2F[year] / totalF2F[year] * 100) + '% , ' +
                str(totalHouseVisits[year]) + ', ' +
                str(unknownHouseVisits[year] / totalHouseVisits[year] * 100) + '% , ' +
                str(totalOtherAppts[year]) + ', ' +
                str(unknownOtherAppts[year] / totalOtherAppts[year] * 100) + '% '
              )

print('\nTable 1 ready. Preview of the CSV file that will be written now to table1.csv: ' + '\n' + table1)
table1FHand = open('table1.csv', 'w')
table1FHand.write(table1)
print('\nTable1.csv written successfully.')

# Table 2: % of all-time peak for each type of appointment for each year
print('\n<< STARTING WORK ON TABLE 2 -  % of all-time peak for each type of appointment for each year >> ')
maxF2F = 0
maxHouseVisits = 0
maxOtherAppts = 0

# Create and prepare the first row of the buffer string that will be used to write Table2 to the CSV file
table2 = 'Year, F2F appointments percentage of peak year, House visits percentage of peak year, Other appointments percentage of peak year'

print('Collecting the peak values for each type of appointment in the 2018-2025 period. Collecting the data per year to calculate percentages.')
for year in range(2018, 2026): # We need to run through ALL years first to find the maximum value for each appointment type. Only THEN calculate the percentages.
    if totalF2F[year] > maxF2F: maxF2F = totalF2F[year]
    if totalHouseVisits[year] > maxHouseVisits: maxHouseVisits = totalHouseVisits[year]
    if totalOtherAppts[year] > maxOtherAppts: maxOtherAppts = totalOtherAppts[year]

for year in range(2018, 2026): # Now we're ready to calculate the percentages.
    table2 += ('\n' + str(year) + ', ' +
               str(totalF2F[year] / maxF2F * 100) + '% , ' +
               str(totalHouseVisits[year] / maxHouseVisits * 100) + '% , ' +
               str(totalOtherAppts[year] / maxOtherAppts * 100) + '% '
               )

print('\nTable 2 ready. Preview of the CSV file that will be written now to table2.csv: ' + '\n' + table2)
table2FHand = open('table2.csv', 'w')
table2FHand.write(table2)
print('\nTable2.csv written successfully.')

# Table 3: % of total annual activity in each season, per year
print('\n<< STARTING WORK ON TABLE 3 - Percentage of total annual activity in each season, per year >> ')

winterTotal = dict()
springTotal = dict()
summerTotal = dict()
autumnTotal = dict()
yearTotal = dict()

# Create and prepare the first row of the buffer string that will be used to write Table3 to the CSV file
table3 = 'Year, % total activity in winter, % total activity in spring, % total activity in summer, % total activity in autumn'

print('Collecting the number of appointments in each season, per year.')
for year in range(2018, 2026):
    result = queryForMonths("01", "02", "03", year, cursor)
    winterTotal[year] = 0
    for i in result:
        winterTotal[year] += i

    result = queryForMonths("04", "05", "06", year, cursor)
    springTotal[year] = 0
    for i in result:
        springTotal[year] += i

    result = queryForMonths("07", "08", "09", year, cursor)
    summerTotal[year] = 0
    for i in result:
        summerTotal[year] += i

    result = queryForMonths("10", "11", "12", year, cursor)
    autumnTotal[year] = 0
    for i in result:
        autumnTotal[year] += i

    yearTotal[year] = winterTotal[year] + springTotal[year] + summerTotal[year] + autumnTotal[year]

    table3 += ('\n' + str(year) + ', ' +
               str(winterTotal[year] / yearTotal[year] * 100) + '% , ' +
               str(springTotal[year] / yearTotal[year] * 100) + '% , ' +
               str(summerTotal[year] / yearTotal[year] * 100) + '% , ' +
               str(autumnTotal[year] / yearTotal[year] * 100) + '% '
               )

print('\nTable 3 ready. Preview of the CSV file that will be written now to table2.csv: ' + '\n' + table3)
table3FHand = open('table3.csv', 'w')
table3FHand.write(table3)
print('\nTable3.csv written successfully.')
