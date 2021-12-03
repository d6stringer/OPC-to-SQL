import mysql.connector

dbconnector = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'nuSKw2^jS!8Bv$d3',
    port = '3306',
    database = 'python_test'
)

mycursor = dbconnector.cursor()

mycursor.execute('SELECT * FROM training_data')
all_data = mycursor.fetchall()

for data in all_data:
    print(data)