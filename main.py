#Bay Materials
#Author: Daniel Woodson
#Started on: 8/25/2021
#Purpose: To create a bridge between the OPC server(s) of the custom BM equipment to the postgreSQL relational database

import postgreSQL_Connector as pSQL
import time
import OPC_Connector
import utilities

yams = utilities.yaml_loader('opc_config.yml')


# opc_data = list(yams['nodes'].values()) #while this does work, it may not be advised since it may not come in the same order every time
#removed this yams['nodes']['total_part_count'], from data to see if it will be more stable.
opc_data = [yams['nodes']['traveler_id'],
            yams['nodes']['part_count'],

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

def get_and_send(tc):
    data = OPC_Connector.get_node_values(opc_data)
    data.insert(2,tc)
    job_status = 1  # not really using right now but might implement in the future
    if job_status:
        print(data)
        pSQL.send_data_to_pSQL(data)
        # OPC_Connector.int_change(yams['nodes']['write_ok'],1) #this writes back to the PLC that the connection is OK
    else:
        # OPC_Connector.int_change(yams['nodes']['write_ok'],0) #this writes back to the PLC that the connection is NOT OK
        pass

def main_func():
    except_count = 0
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
                get_and_send(new_value)
                last_job = time.time()

            time.sleep(0.1) #just a "governor" of sorts

            if time.time() - last_job > time_out:
                ts = OPC_Connector.get_node_value(yams['nodes']['total_part_count'])
                get_and_send(ts)
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

    except ConnectionResetError:
        #this is what you get when you reboot the PLC
        pass

    # except:
    #     print("this was the catch-all exception")
    #     except_count += 1
    #     print("We've had {0} exceptions", except_count)
        # print("trying to reconnect")
        # OPC_Connector.kill_session()
        # time.sleep(5)
        # OPC_Connector.connect()
        # main_func()
    # except ConnectionError:
    #     print("there was a connection error")


    finally:
        pass

if __name__ == '__main__':
    main_func()

