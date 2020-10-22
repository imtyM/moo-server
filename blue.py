import json
from bluetooth import *

from modes import Modes

class Blue:
    def __init__(self):
        self.client_sock = None
        self.server_sock = None
        self.setupBluetoothProcessing()

    def setupBluetoothProcessing(self):
        print('=========================\n')
        print('Setting up bluetooth')
        try:
            self.server_sock = BluetoothSocket( RFCOMM  )
            self.server_sock.bind(('',PORT_ANY))
            self.server_sock.listen(1)
        except:
            print('Trouble binding to RFCOMM. Does your pc even have bluetooth?😕\n Bluetooth NOT setup.🖕\n\n')
            return

        port = self.server_sock.getsockname()[1]

        uuid = '94f39d29-7d6d-437d-973b-fba39e49d4ee'

        advertise_service(
                self.server_sock, 'TestServer',
                service_id = uuid,
                service_classes = [ uuid, SERIAL_PORT_CLASS  ],
                profiles = [ SERIAL_PORT_PROFILE  ],
                #protocols = [ OBEX_UUID  ]
        )
        print('Waiting for connection on RFCOMM channel: ', port, '\nConnect with your phone to proceed.....\n\n')
        self.client_sock, self.client_info = self.server_sock.accept()
        print ('Accepted connection from ', self.client_info, '. \nBluetooth server setup complete.👌\n\n')

    def recieve_data(self):
        data_recieved = self.client_sock.recv(1024)
        if data_recieved && len(data_recieved) > 0:
            return data_recieved
        return None

    def send_data(self, data=None):
        print('sending: ', data)
        self.client_sock.send(data)

    # @param mode [Mode]: Current mode of the system
    # @returns mode, data_recieved
    # @return mode [Mode]: The mode that is set from data recieved from the
    #         bluetooth dewise, defaults to current mode
    # @return data_recieved [String]: recieved data
    def processInputFromBluetooth(self, mode):
        data_recieved = self.recieve_data()
        if data_recieved:
            recieved_mode = int(data_recieved)
            if not type(recieved_mode) == int or recieved_mode < 0 or recieved_mode > 2:
                raise('The recieved_mode needs to be an int, got this tho: ', data_recieved)
            else:
                return Modes(recieved_mode), data_recieved
        return mode, None

    # @param valid [Bool]: Flag if the cow_data is valid
    # @param cow_data [Dict]: Dict of the cow data to send to the front
    # @param cow_id: id of the cow
    def processOutputToBluetooth(valid, cow_data, cow_id):
        if not valid:
            return

        json_cow_data = json.dumps(cow_data, separators=(',', ':'))
        self.send_data(json_cow_data)

    def cleanup(self):
        self.client_sock.close()
        self.server_sock.close()
