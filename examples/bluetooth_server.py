#!/usr/bin/env python
'''
A simple test server that returns a random number when sent the text 'temp' via Bluetooth serial.
'''

from bluetooth import *

print('=========================\n')
print('Setting up bluetooth')
try:
    server_sock = BluetoothSocket( RFCOMM  )
    server_sock.bind(('',PORT_ANY))
    server_sock.listen(1)
except:
    print('Trouble binding to RFCOMM. Does your pc even have bluetooth?😕\n Bluetooth NOT setup.🖕\n\n')

port = server_sock.getsockname()[1]

print(server_sock.getsockname())
uuid = '94f39d29-7d6d-437d-973b-fba39e49d4ee'

advertise_service(
        server_sock, 'TestServer',
        service_id = uuid,
        service_classes = [ uuid, SERIAL_PORT_CLASS  ],
        profiles = [ SERIAL_PORT_PROFILE  ],
        #protocols = [ OBEX_UUID  ]
)
print('Waiting for connection on RFCOMM channel ', port)
client_sock, client_info = server_sock.accept()
print ('Accepted connection from ', client_info, '. Bluetooth server setup complete.👌\n\n')

while True:
    try:
        req = client_sock.recv(1024)
        if len(req) == 0:
            break
        print('received ', req)

        print('sending ', req)
        client_sock.send(req)

    except IOError:
        pass

    except KeyboardInterrupt:
        print('disconnected')

        client_sock.close()
        server_sock.close()
        print('all done')

        break

