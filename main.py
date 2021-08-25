#Bay Materials
#Author: Daniel Woodson
#Started on: 8/25/2021
#Purpose: To create a bridge between the OPC server(s) of the custom BM equipment to the postgreSQL relational database

#import postgreSQL_Connector
import OPC_Connector

def print_distance():
    print(OPC_Connector.get_distance())

if __name__ == '__main__':
    print_distance()



