import sys
import os
import time

GPIO_EXPORT_PATH = "/sys/class/gpio/export"
GPIO_UNEXPORT_PATH = "/sys/class/gpio/unexport"
GPIO_DIRECTION_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/direction"
GPIO_VALUE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/value"
GPIO_BASE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}"

FREQUENCIES = {
    'C': 261.63,  
    'D': 293.66,  
    'E': 329.63,  
    'F': 349.23,  
    'G': 392.00,  
    'A': 0,  
    'B': 493.88,  
    'C5': 523.25  
}

def is_gpio_exported(gpio_number):
    gpio_base_path = GPIO_BASE_PATH_TEMPLATE.format(gpio_number)
    return os.path.exists(gpio_base_path)

def export_gpio(gpio_number):
    if not is_gpio_exported(gpio_number):
        try:
            with open(GPIO_EXPORT_PATH, 'w') as export_file:
                export_file.write(str(gpio_number))
        except IOError as e:
            print(f"Error exporting GPIO {gpio_number}: {e}")
            sys.exit(1)

def unexport_gpio(gpio_number):
    try:
        with open(GPIO_UNEXPORT_PATH, 'w') as unexport_file:
            unexport_file.write(str(gpio_number))
    except IOError as e:
        print(f"Error unexporting GPIO {gpio_number}: {e}")
        sys.exit(1)

def set_gpio_direction(gpio_number, direction):
    gpio_direction_path = GPIO_DIRECTION_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_direction_path, 'w') as direction_file:
            direction_file.write(direction)
    except IOError as e:
        print(f"Error setting GPIO {gpio_number} direction to {direction}: {e}")
        sys.exit(1)

def set_gpio_value(gpio_number, value):
    gpio_value_path = GPIO_VALUE_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_value_path, 'w') as value_file:
            value_file.write(str(value))
    except IOError as e:
        print(f"Error setting GPIO {gpio_number} value to {value}: {e}")
        sys.exit(1)

def play_tone(gpio_number, frequency, duration):
    period = 1.0 / frequency
    half_period = period / 2
    end_time = time.time() + duration

    while time.time() < end_time:
        set_gpio_value(gpio_number, 1)
        time.sleep(half_period)
        set_gpio_value(gpio_number, 0)
        time.sleep(half_period)

def get_button_input():
    button_pins = {
        'C': 83,  # GPIO 83
        'D': 84,  # GPIO 84
        'E': 85,  # GPIO 85
        'F': 86,  # GPIO 86
        'G': 87,  # GPIO 87
        'A': 88,  # GPIO 88
        'B': 89,  # GPIO 89
    }
    for note, pin in button_pins.items():
        gpio_value_path = GPIO_VALUE_PATH_TEMPLATE.format(pin)
        try:
            with open(gpio_value_path, 'r') as value_file:
                value = value_file.read().strip()
                if value == '1':  # 버튼이 눌렸을 때
                    return note
        except IOError as e:
            print(f"Error reading GPIO {pin} value: {e}")
            sys.exit(1)
    return None  # 버튼이 눌리지 않으면 None을 반환

if __name__ == "__main__":
    gpio_pin = 90  # 버저가 연결된 핀 번호 (GPIO 90)

    try:
        export_gpio(gpio_pin)
        set_gpio_direction(gpio_pin, "out")

        button_input = None
        while True:
            button_input = get_button_input()
            if button_input:  # 버튼이 눌린 경우에만
                print(f"{button_input} 버튼이 눌렸습니다.")
                play_tone(gpio_pin, FREQUENCIES[button_input], 0.5)
                time.sleep(0.2)  # 버튼 눌림 인식 후 잠시 대기

    except KeyboardInterrupt:
        print("\nOperation stopped by User")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        unexport_gpio(gpio_pin)

    sys.exit(0)
