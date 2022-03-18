#Adapted from examples found here: https://www.postgresqltutorial.com/postgresql-python/query/

import psycopg2
from decouple import config
#make the connection to the RDB


def pSQL_conn():

    pSQL_conn = psycopg2.connect(
        host=config('host', default=''),
        user=config('user', default=''),
        database=config('database', default=''),
        password=config('password', default=''),
        port=config('port', default='')
    )
    return pSQL_conn

def send_data_to_pSQL(data):
    try:
        connection = pSQL_conn()
        cursor = connection.cursor()
        squirrls = """
            INSERT INTO machine_run_data (id, traveler_id, traveler_code, part_count, total_part_count, time_stamp, top_heater_SV, top_heater_PV, top_heater_enable, bottom_heater_SV, bottom_heater_PV, bottom_heater_enable, cooling_fans, line_speed, waste_tension, feed_tension, roll_diameter, start_mode, slow_start_mode, stop_mode, jog_mode, safety_ok, system_enable, waste_tension_enable, feed_tension_enable) 
            VALUES (default, 1,%s, %s, %s,current_timestamp, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        cursor.execute(squirrls, data)
        connection.commit()
        connection.close()
        return
    except IndexError:
        print('This is the index error')
        return
