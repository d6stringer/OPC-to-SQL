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

    ls_data = [yams['nodes']['job_number'],
               yams['nodes']['count_of_blobs'],
               yams['nodes']['part_width'],
               yams['nodes']['histogram_avg'],
               yams['nodes']['histogram_contrast']
               ]

    value = 0
    try:
        while True:
            new_value = OPC_Connector.get_node_value(yams['nodes']['part_count'])
            if value != new_value:
                value = new_value
                data = OPC_Connector.get_node_values(ls_data)
                data.insert(0,value)
                job_status = OPC_Connector.get_node_value(yams['nodes']['job_active'])
                if job_status:
                    print(data)
                    pSQL.send_linescan_to_pSQL(data)
                    OPC_Connector.int_change(yams['nodes']['write_ok'],1)
                else:
                    OPC_Connector.int_change(yams['nodes']['write_ok'],0)

            time.sleep(0.1)


    except KeyboardInterrupt:
        print('break')
        OPC_Connector.kill_session()