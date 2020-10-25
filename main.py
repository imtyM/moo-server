from image_processor import ImageProcessor
from blue import Blue
from weight_detector import WeightDetector
from modes import Modes

mode = Modes.IDLE
## Setup image processing
image_processor = ImageProcessor(debug=True)

bluetooth = Blue()

weight_detector = WeightDetector(debug=False)

while True:
    # mode, data_recieved = bluetooth.processInputFromBluetooth(mode)
    # if data_recieved:
        # print('Recieved data: ', data_recieved)
        # bluetooth.processOutputToBluetooth(True, data_recieved, 1)
        # continue

    weights = weight_detector.take_weights()
    weight_detector.print_weights(weights)

    # if mode == Modes.REGISTER:
        # # TODO: Lameness detector doesnt exist
        # valid, cow_data = weight_detector.detectCowLameness()
        # # TODO: registerEpoch does not exist
        # cow_id = image_processor.registerEpoch(cap, valid, cow_data)
        # bluetooth.processOutputToBluetooth(valid, cow_data, cow_id)

    # if mode == Modes.DETECT:
        # valid, cow_data = weight_detector.detectCowLameness()
        # # TODO: detectEpoch does not exist
        # cow_id = image_processor.detectEpoch(cap)
        # bluetooth.processOutputToBluetooth(valid, cow_data, cow_id)
