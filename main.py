#Bay Materials
#Author: Daniel Woodson
#Started on: 8/25/2021
#Purpose: To create a bridge between the OPC server(s) of the custom BM equipment to the postgreSQL relational database

import postgreSQL_Connector as pSQL
import time
import OPC_Connector
import utilities

yams = utilities.yaml_loader('opc_config.yml')

def get_and_send():
    data = OPC_Connector.get_node_values(opc_data)
    job_status = 1  # not really using right now but might implement in the future
    if job_status:
        print(data)
        pSQL.send_data_to_pSQL(data)
        # OPC_Connector.int_change(yams['nodes']['write_ok'],1) #this writes back to the PLC that the connection is OK
    else:
        # OPC_Connector.int_change(yams['nodes']['write_ok'],0) #this writes back to the PLC that the connection is NOT OK
        pass


if __name__ == '__main__':

    # opc_data = list(yams['nodes'].values()) #while this does work, it may not be advised since it may not come in the same order every time
    opc_data = [yams['nodes']['traveler_id'],
                yams['nodes']['part_count'],
                yams['nodes']['total_part_count'],
                yams['nodes']['top_heater_SV'],
                yams['nodes']['top_heater_PV'],
                yams['nodes']['top_heater_enable'],
                yams['nodes']['bottom_heater_SV'],
                yams['nodes']['bottom_heater_PV'],
                yams['nodes']['bottom_heater_enable'],
                yams['nodes']['cooling_fans'],
                yams['nodes']['line_speed'],
                yams['nodes']['waste_tension'],
                yams['nodes']['feed_tension'],
                yams['nodes']['roll_diameter'],
                yams['nodes']['start_mode'],
                yams['nodes']['slow_start_mode'],
                yams['nodes']['stop_mode'],
                yams['nodes']['jog_mode'],
                yams['nodes']['safety_ok'],
                yams['nodes']['system_enable'],
                yams['nodes']['waste_tension_enable'],
                yams['nodes']['feed_tension_enable']
                ]

    value = 0
    last_job = time.time()
    time_out = 60
    retry_time = 3
    retry_count = 0
    try:
        while OPC_Connector.client:
            new_value = OPC_Connector.get_node_value(yams['nodes']['total_part_count'])
            if value != new_value:
                value = new_value
                get_and_send()
                last_job = time.time()

            time.sleep(0.1) #just a "governor" of sorts

            if time.time() - last_job > time_out:
                get_and_send()
                last_job = time.time()

        if not OPC_Connector.client and time.time() - last_job > retry_time:
            print('Trying to reconnect to OPC server')
            OPC_Connector.connect()
            last_job = time.time()
            # retry_count += 1
            # if retry_count > 10:
            #     ConnectionError = True


    except KeyboardInterrupt:
        print('Keyboard Interrupt Pressed, trying to kill the session')
        OPC_Connector.kill_session()

    except TimeoutError:
        print("aw shippidy flomps  you've got a time out error")

    except:
        print("this was the catch-all exception")
        print("trying to reconnect")
        OPC_Connector.connect()
    # except ConnectionError:
    #     print("there was a connection error")


    finally:
        pass