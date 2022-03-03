#Bay Materials
#Author: Daniel Woodson
#Started on: 8/25/2021
#Purpose: To create a bridge between the OPC server(s) of the custom BM equipment to the postgreSQL relational database

import postgreSQL_Connector as pSQL
import time
import OPC_Connector
import utilities

yams = utilities.yaml_loader('opc_config.yml')


if __name__ == '__main__':

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
                yams['nodes']['system_enable']
                ]

    value = 0
    try:
        while True:
            new_value = OPC_Connector.get_node_value(yams['nodes']['total_part_count'])
            if value != new_value:
                value = new_value
                # opc_data_string = ", ".join([str(opc_data[x]) for x in range(len(opc_data))])
                # print(opc_data_string)
                data = OPC_Connector.get_node_values(opc_data)
                # data.insert(0,value)
                job_status = 1
                if job_status:
                    print(data)
                    pSQL.send_data_to_pSQL(data)
                    # OPC_Connector.int_change(yams['nodes']['write_ok'],1)
                else:
                    # OPC_Connector.int_change(yams['nodes']['write_ok'],0)
                    pass

            time.sleep(0.1)


    except KeyboardInterrupt:
        print('break')
        OPC_Connector.kill_session()