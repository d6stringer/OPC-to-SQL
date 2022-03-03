#Bay Materials
#Adapted from examples found here: https://github.com/FreeOpcUa/python-opcua/blob/master/examples/client-example.py

import logging
import time
from opcua import Client, ua
import utilities

#get your yams
yam_loaction = 'opc_config.yml'
yam = utilities.yaml_loader(yam_loaction)

#create client, timeout must match the server set in TIA portal
client = Client(yam['ip_addresses']['crc_opc'])
client.session_timeout = yam['timeouts']['default'] #actual timeout is changed in client.py
client.connect()

logging.basicConfig(level=logging.WARN)

class SubHandler(object):

    """
    I don't understand how this works yet.
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)

def kill_session():
    try:
        print("disconnecting client...")
        client.disconnect()
        time.sleep(1)
    except:
        print("Cant' kill session")
    finally:
        print("Disconnected")

def get_node_value(node):
    try:
        # get value of specific node
        node_value = client.get_node(node).get_value()
        if node_value:
            return node_value

    finally:
        #client.disconnect()
        pass

def get_node_values(nodes):
    data = []
    try:
        # get values from a list of nodes & returns a list of their values
        for node in nodes:
            node_value = client.get_node(node).get_value()
            if node_value is not None:
                data.append(node_value)
            else:
                data.append('bad_data')
        # node_values = client.set_values(nodes)
        # print(node_values)
    finally:
        #client.disconnect()
        return data


def int_change(node, val):
    try:
        int_var = client.get_node(node)
        dv = ua.DataValue(ua.Variant(val, ua.VariantType.Int32))
        dv.SourceTimestamp = None
        dv.ServerTimestamp = None
        int_var.set_value(dv)
    except:
        pass
    finally:
        #client.disconnect()
        pass






'''
This is newer junk:
    def write_ok(node):
        objects = client.get_node(node)
        objects.set_value(1)
    
    def write_not_ok(node):
        tag = client.get_node(node)
        tag.set_value(0)
    
    
    This is old junk
    def int_change():
    
        try:
            node_addrs = "ns=4;i=4"
            int_var = client.get_node(node_addrs)
    
            if int_var.get_value() == 0:
                print(int_var.get_value())
                dv = ua.DataValue(ua.Variant(5, ua.VariantType.Int16))
                dv.SourceTimestamp = None
                dv.ServerTimestamp = None
                int_var.set_value(dv)
    
            else:
                print("Womp womp")
                print(int_var.get_value())
                dv = ua.DataValue(ua.Variant(0, ua.VariantType.Int16))
                dv.SourceTimestamp = None
                dv.ServerTimestamp = None
                int_var.set_value(dv)
    
    
        finally:
            client.disconnect()
    
    def get_session_count():
        try:
            session_node = client.get_node("i=2277")
            session_count = session_node.get_value()
            print("Session count is: ", session_count)
            if session_count > 1:
                try:
                    dv = ua.DataValue(ua.Variant(1, ua.VariantType.Int16))
                    dv.SourceTimestamp = None
                    dv.ServerTimestamp = None
                    session_node.set_value(dv)
                    # client.disconnect()
                    print(session_count)
                    time.sleep(1)
                except:
                    pass
        finally:
            pass
        return int(session_count)
    def distance_sub(node):
        try:
            tag1 = client.get_node(node)
            handler = SubHandler()
            sub = client.create_subscription(1000, handler)
            handle1 = sub.subscribe_data_change(tag1)
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            kill_sub(sub, tag1)
            time.sleep(1)
            kill_session()
        finally:
            print("That was it")
    
        return
    
    def part_count_sub(node, list):
        try:
            tag1 = client.get_node(node)
            data = []
            handler = SubHandler()
            sub = client.create_subscription(1000, handler)
            print(data)
            handle1 = sub.subscribe_data_change(tag1)
            print(handle1)
            # while True:
            #     time.sleep(0.1)
        except KeyboardInterrupt:
            kill_sub(sub, tag1)
            time.sleep(1)
            kill_session()
        finally:
            print("Subscription Created")
    
        # last_value = 0
        # while True:
        #     if handle1 != last_value:
        #         for l in list:
        #             l_node = client.get_node(l)
        #             data.append(l_node.get_value())
        #         print(data)
        #         print('im a dummy', handle1)
        #         last_value = handle1
    
    
    def kill_sub(sub_name, tag):
        try:
            print("Trying to kill sub...")
            sub_name.unsubscribe(tag)
            time.sleep(1)
        except:
            print("Can't Unsubscribe")
        finally:
            print("sub dead")
    
        try:
            print("Trying to delete sub")
            sub_name.delete()
            time.sleep(1)
        except:
            print("Can't delete sub")
        finally:
            print("Sub deleted")

'''
