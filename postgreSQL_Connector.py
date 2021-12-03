#Adapted from examples found here: https://www.postgresqltutorial.com/postgresql-python/query/

import psycopg2
import datetime
#make the connection to the RDB
def pSQL_conn():
    pSQL_conn = psycopg2.connect(
        host = "bmus-db-sfo3-default-do-user-672237-0.a.db.ondigitalocean.com",
        database = "operations",
        user = "daniel",
        password = "w4vbhlwjqikzuqca",
        port = "25060"
    )
    return pSQL_conn

def send_linescan_to_pSQL(data):
    connection = pSQL_conn()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO linescan_data (id, datetime, part_count, job_number, count_of_blobs, part_width, histogram_avg, histogram_contrast) 
        VALUES (default, default, %s, %s, %s, %s, %s, %s)
        """,
        (data[0], data[1], data[2], data[3], data[4], data[5]))
    # row = cursor.fetchone()
    # while row is not None:
    #     print(row)
    #     row = cursor.fetchone()
    connection.commit()
    connection.close()


# data = [4.0, 18.0, 3.0, 1550.2857666015625, 113.65880584716797, 20.866485595703125]
# pSQL.pSQL_cursor("INSERT INTO linescan_data (part_count, job_number, count_of_blobs, part_width, histogram_avg, histogram_contrast) VALUES (%s, %s, %s, %s, %s, %s)", (data[0], data[1], data[2], data[3], data[4], data[5]))






# #make a cursor
# pSQL_cur = pSQL_conn.cursor()
# #send some SQL
# pSQL_cur.execute("SELECT * FROM manufacturing_products mp")
# #read line by line
# row = pSQL_cur.fetchone()
# while row is not None:
#     print(row)
#     row = pSQL_cur.fetchone()
#
# #close the connection
# pSQL_conn.close()