import json
import socket
import sys
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
        # self.client_sock.settimeout(2)
        self.client_sock.setblocking(0)
        print ('Accepted connection from ', self.client_info, '. \nBluetooth server setup complete.👌\n\n')

    def recieve_data(self):
        data_recieved = None
        try:
            data_recieved = self.client_sock.recv(1024)
        except(socket.error):
            pass

        if data_recieved and len(data_recieved) > 0:
            return data_recieved
        return None

    def send_data(self, data=None):
        self.client_sock.send(data + '\r\n')

    # @param mode [Mode]: Current mode of the system
    # @returns mode, data_recieved
    # @return mode [Mode]: The mode that is set from data recieved from the
    #         bluetooth dewise, defaults to current mode
    # @return data_recieved [String]: recieved data
    def processInputFromBluetooth(self, mode, references):
        data_recieved = self.recieve_data()
        if data_recieved:
            payload = json.loads(data_recieved)
            recieved_mode = payload.get('mode', mode)
            references_string = payload.get('references')
            tare = payload.get('tare', False)
            should_send_next_frame = payload.get('should_send_next_frame', False)
            new_references = self.parse_references(references_string, references)

            roi_bounds = self.parse_roi_bounds(payload.get('rois', None))

            return data_recieved, Modes(recieved_mode), new_references, tare, should_send_next_frame, roi_bounds
        return None, mode, references, False, False, None

    # @param valid [Bool]: Flag if the cow_data is valid
    # @param cow_data [Dict]: Dict of the cow data to send to the front
    # @param cow_id: id of the cow
    def send_payload(self, valid=False, cow_data={}, cow_id=None, mode=Modes.IDLE, references={}, base_64_image=None):
        payload = {
            'valid': valid,
            'cowData': {**cow_data, 'id': cow_id},
            'mode': mode.value,
            'references': references,
            'base64Image': base_64_image
        }
        json_payload = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
        # print(json_payload)
        self.send_data(json_payload)

    def cleanup(self):
        self.client_sock.close()
        self.server_sock.close()

    def parse_references(self, references_string, references):
        if not references_string:
            return references
        references_values = references_string.split('\n')
        new_references = {
            'front_left_reference': int(references_values[0]),
            'front_right_reference': int(references_values[1]),
            'hind_right_reference': int(references_values[2]),
            'hind_left_reference': int(references_values[3])
        }
        if all(type(value) == int for value in new_references.values()):
            return new_references
        return references

    def parse_roi_bounds(self, roi_bounds_string):
        if roi_bounds_string is None:
            return None
        roi_values = roi_bounds_string.split('\n')
        new_references = {
            'lowX': int(roi_values[0]),
            'highX': int(roi_values[1]),
            'lowY': int(roi_values[2]),
            'highY': int(roi_values[3])
        }
        if all(type(value) == int for value in new_references.values()):
            return new_references
        return None

    def send_next_frame_base_64(self, base_64_image):
        if base_64_image is not None:
            # print(type(base_64_image))
            self.send_payload(base_64_image=base_64_image)
