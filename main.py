from image_processor import ImageProcessor
from blue import Blue
from weight_detector import WeightDetector
from modes import Modes
import time

mode = Modes.DETECT
## Setup image processing
image_processor = ImageProcessor(debug=True)

bluetooth = Blue()

weight_detector = WeightDetector(debug=False)

while True:
    try:
        print('Mode: ', mode)
        mode, data_recieved = bluetooth.processInputFromBluetooth(mode)
        if data_recieved:
            print('Recieved data: ', data_recieved)
            # bluetooth.processOutputToBluetooth(True, data_recieved, 1)
            continue

        if mode == Modes.DETECT:
            valid, cow_data = weight_detector.detectCowLameness()
            bluetooth.send_payload(
                valid=valid,
                cow_data=cow_data,
                mode=mode
            )

        if mode == Modes.IDLE:
            bluetooth.send_payload(mode=mode)

        time.sleep(0.5)
    except:
       bluetooth.setupBluetoothProcessing()

    # if mode == Modes.REGISTER:
        # # TODO: Lameness detector doesnt exist
        # valid, cow_data = weight_detector.detectCowLameness()
        # # TODO: registerEpoch does not exist
        # cow_id = image_processor.registerEpoch(cap, valid, cow_data)
        # bluetooth.processOutputToBluetooth(valid, cow_data, cow_id)
