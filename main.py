from image_processor import ImageProcessor
from blue import Blue
from weight_detector import WeightDetector
from modes import Modes
import time

mode = Modes.DETECT

image_processor = ImageProcessor(debug=False)
bluetooth = Blue()
weight_detector = WeightDetector(debug=False)

while True:
    # try:
    references = weight_detector.get_sensor_references()
    print('Mode: ', mode)

    data_recieved, mode, references, tare = bluetooth.processInputFromBluetooth(mode, references)
    if data_recieved:
        print('Recieved data: ', data_recieved)
        # bluetooth.processOutputToBluetooth(True, data_recieved, 1)
        weight_detector.set_sensor_references(references)
        weight_detector.tare(tare)
        continue

    if mode == Modes.DETECT:
        valid, cow_data = weight_detector.detectCowLameness()
        cow_id = image_processor.detectCow(valid)
        bluetooth.send_payload(
            valid=valid,
            cow_data=cow_data,
            cow_id=cow_id,
            mode=mode,
            references=references
        )

    if mode == Modes.IDLE:
        bluetooth.send_payload(mode=mode, references=references)

    time.sleep(0.5)
    # except:
       # bluetooth.setupBluetoothProcessing()

    # if mode == Modes.REGISTER:
        # # TODO: Lameness detector doesnt exist
        # valid, cow_data = weight_detector.detectCowLameness()
        # # TODO: registerEpoch does not exist
        # cow_id = image_processor.registerEpoch(cap, valid, cow_data)
        # bluetooth.processOutputToBluetooth(valid, cow_data, cow_id)
