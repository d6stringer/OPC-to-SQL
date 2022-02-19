#Adapted from examples found here: https://www.postgresqltutorial.com/postgresql-python/query/

import psycopg2
from decouple import config
import datetime
#make the connection to the RDB


def pSQL_conn():

    pSQL_conn = psycopg2.connect(
        host=config('host', default=''),
        database=config('database', default=''),
        user=config('user', default=''),
        password=config('password', default=''),
        port=config('port', default='')
    )
    return pSQL_conn

def SQL_string_machine(variables, data):
    sql_string =
    "
    """
    """
    "

def send_linescan_to_pSQL(data):
    connection = pSQL_conn()
    cursor = connection.cursor()
    data
    cursor.execute("""
        INSERT INTO machine_run_data (
            traveler_id, 
            part_count, 
            total_part_count, 
            time_stamp, 
            top_heater_SV,
            top_heater_PV,
            top_heater_enable,
            bottom_heater_SV,
            bottom_heater_PV,
            bottom_heater_enable,
            cooling_fans,
            line_speed,
            waste_tension,
            feed_tension,
            roll_diameter,
            start_mode,
            slow_start_mode,
            stop_mode,
            jog_mode,
            safety_ok,
            system_enable
            ) 
        VALUES (
            1, 
            1, 
            %s, 
            default,
            %s, 
            %s, 
            %s, 
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """,
        data)
    # row = cursor.fetchone()
    # while row is not None:
    #     print(row)
    #     row = cursor.fetchone()
    connection.commit()
    connection.close()
    return


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