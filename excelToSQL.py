import xlrd
import sqlite3
import re
from datetime import datetime

# Open the workbook and define the worksheet
book = xlrd.open_workbook("2015 2016 attacks.xlsx")
sheet = book.sheet_by_name("Sheet1")

# Establish a sqlite3 connection
conn = sqlite3.connect('attacks.db')

# Get the cursor, which is used to traverse the database, line by line
c = conn.cursor()

# c.execute("CREATE TABLE attacks (attack_id INT PRIMARY KEY NOT NULL, start_date DATE NOT NULL, end_date DATE NOT NULL, type TEXT, victim_death_count INT NOT NULL, perpetrator_death_count INT, victim_injury_count INT, perpetrator_injury_count INT, primary_location text, secondary_location text, perpetrator text, reason text)")
# Create the INSERT INTO sql query
query = "INSERT INTO attacks (attack_id, start_date, end_date, type, victim_death_count, perpetrator_death_count, victim_injury_count, perpetrator_injury_count, primary_location, secondary_location, perpetrator, reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

def my_int(value):
    if isinstance(value, basestring) and value == 'unknown':
        return None
    return int(value) if value else 0

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet.nrows):
    attack_id               = r;
    year                    = my_int(sheet.cell(r,0).value)
    month                   = sheet.cell(r,1).value
    start_day               = my_int(sheet.cell(r,2).value)
    end_day                 = my_int(sheet.cell(r,3).value)
    type                    = sheet.cell(r,4).value
    victim_death_count      = my_int(sheet.cell(r,5).value)
    perpetrator_death_count = my_int(sheet.cell(r,6).value)
    victim_injury_count     = my_int(sheet.cell(r,7).value)
    perpetrator_injury_count= my_int(sheet.cell(r,8).value)
    location                = sheet.cell(r,9).value
    perpetrator             = sheet.cell(r,10).value
    reason                  = sheet.cell(r,11).value


    start_date = datetime.strptime(month+' '+str(start_day)+' '+str(year), '%B %d %Y')
    end_date = datetime.strptime(month+' '+str(end_day)+' '+str(year), '%B %d %Y')
    m = re.match(r'(.*,)*\s*\xc2*\xa0*(.*),\s*\xc2*\xa0*(.*)', location)
    if m:
        primary_location = m.group(3)
        secondary_location = m.group(2)
    else:
        primary_location = None
        secondary_location = None

    # Assign values from each row
    values = (attack_id, start_date, end_date, type, victim_death_count, perpetrator_death_count, victim_injury_count, perpetrator_injury_count, primary_location, secondary_location, perpetrator, reason)

    # Execute sql Query
    c.execute(query, values)


# Commit the transaction
conn.commit()

# Close the database connection
conn.close()

# Print results
print ""
print "All Done! Bye, for now."
print ""
columns = str(sheet.ncols)
rows = str(sheet.nrows)
print "I just imported " + columns + " columns and " + rows + " rows to MySQL!"
