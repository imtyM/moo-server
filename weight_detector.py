CLOCK_PIN = 1

FRONT_LEFT = 0
FRONT_RIGHT = 1
HIND_RIGHT = 2
HIND_LEFT = 3

FRONT_LEFT_PIN = 0
FRONT_RIGHT_PIN = 2
HIND_RIGHT_PIN = 3
HIND_LEFT_PIN = 5

import time

class WeightDetector():
    def __init__(self, debug=False):
        print('=========================\n')
        print('Setting up weight detector\n')
        self.front_left_reference = 2932.00
        self.front_right_reference = -3189.00
        self.hind_right_reference = 3525.00
        self.hind_left_reference = -2821.00

        if debug:
            from emulated_hx711 import HX711
        else:
            import Odroid.GPIO as GPIO
            from hx711 import HX711
        self.sensors = [
            HX711(FRONT_LEFT_PIN, CLOCK_PIN),
            HX711(FRONT_RIGHT_PIN, CLOCK_PIN),
            HX711(HIND_RIGHT_PIN, CLOCK_PIN),
            HX711(HIND_LEFT_PIN, CLOCK_PIN)
        ]
        self.init_sensor_references()
        self._setup_sensors()

        print('Weight detector setup complete.👌\n\n')

    def init_sensor_references(self):
        print('Connecting sensors...\n')
        self.sensors[FRONT_LEFT].set_reference_unit(self.front_left_reference)
        self.sensors[FRONT_RIGHT].set_reference_unit(self.front_right_reference)
        self.sensors[HIND_LEFT].set_reference_unit(self.hind_left_reference)
        self.sensors[HIND_RIGHT].set_reference_unit(self.hind_right_reference)

    def set_sensor_references(self, references):
        self.sensors[FRONT_LEFT].set_reference_unit(references.get('front_left_reference', self.front_left_reference))
        self.sensors[FRONT_RIGHT].set_reference_unit(references.get('front_right_reference', self.front_right_reference))
        self.sensors[HIND_LEFT].set_reference_unit(references.get('hind_right_reference', self.hind_right_reference))
        self.sensors[HIND_RIGHT].set_reference_unit(references.get('hind_left_reference', self.hind_left_reference))

        self.front_left_reference = references.get('front_left_reference', self.front_left_reference)
        self.front_right_reference = references.get('front_right_reference', self.front_right_reference)
        self.hind_right_reference = references.get('hind_right_reference', self.hind_right_reference)
        self.hind_left_reference = references.get('hind_left_reference', self.hind_left_reference)

    def get_sensor_references(self):
        return {
            'front_left_reference': self.front_left_reference,
            'front_right_reference': self.front_right_reference,
            'hind_right_reference': self.hind_right_reference,
            'hind_left_reference': self.hind_left_reference,
        }

    def _setup_sensors(self):
        for idx, sensor in enumerate(self.sensors):
            sensor.set_reading_format("MSB", "MSB")
            sensor.set_gain(128)
            sensor.reset()
            print(f'Taring {idx}....\n')
            sensor.tare()

    def take_weights(self):
        values = [sensor.get_weight(1) for sensor in self.sensors]
        for sensor in self.sensors:
            sensor.power_down()
            sensor.power_up()
        time.sleep(0.1)

        return values

    def print_weights(self, weights):
        print(f'Front left: {weights[FRONT_LEFT]}\nFront right: {weights[FRONT_RIGHT]}\nHind right: {weights[HIND_RIGHT]}\nHind left: {weights[HIND_LEFT]}\n\n')

    def detectCowLameness(self):
        weights = self.take_weights() # [120, 120, 120, 123]
        lameness_class = self.lamness_classification(weights)
        # self.print_weights(weights)
        cow_data = {
                'lameness_class': lameness_class,
                'frontLeft': weights[FRONT_LEFT],
                'frontRight': weights[FRONT_RIGHT],
                'hindRight': weights[HIND_RIGHT],
                'hindLeft': weights[HIND_LEFT],
                'weight': sum(weights)
        }
        return True, cow_data

    def lamness_classification(self, weights):
        front_ratio = self.calculate_ratio(weights[0:2])
        back_ratio = self.calculate_ratio(weights[2:5])

        leg_weight_ratio = min(front_ratio, back_ratio)

        return self.classify_leg_weight_ratio(leg_weight_ratio)


    def calculate_ratio(self, weights):
        if 0 in weights:
            return 0
        return min(weights)/max(weights)

    def classify_leg_weight_ratio(self, leg_weight_ratio):
        if leg_weight_ratio <= 1 and leg_weight_ratio > 0.85:
            return 'healthy'
        if leg_weight_ratio <= 0.85 and leg_weight_ratio > 0.80:
            return 'Mildly Lame'
        if leg_weight_ratio <= 0.80 and leg_weight_ratio > 0.75:
            return 'Moderately Lame'
        if leg_weight_ratio <= 0.75 and leg_weight_ratio > 0.70:
            return 'Lame'
        if leg_weight_ratio <= 0.70 and leg_weight_ratio >= 0:
            return 'Severely Lame'
        return f"Something is wrong: {leg_weight_ratio}"

    def tare(self, tare):
        if tare:
            self.init_sensor_references()
            self._setup_sensors()

