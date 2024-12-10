import sys
import os
import time

# GPIO 경로 설정
GPIO_EXPORT_PATH = "/sys/class/gpio/export"
GPIO_UNEXPORT_PATH = "/sys/class/gpio/unexport"
GPIO_DIRECTION_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/direction"
GPIO_VALUE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/value"
GPIO_BASE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}"

# 음계에 해당하는 주파수
FREQUENCIES = {
    'C': 261.63,  
    'D': 293.66,  
    'E': 329.63,  
    'F': 349.23,  
    'G': 392.00,  
    'A': 440.00,  
    'B': 493.88  
}

# 버튼과 GPIO 핀 번호 매핑
BUTTON_PINS = {
    'C': 81,  # 핀 번호 3
    'D': 82,  # 핀 번호 5
    'E': 83,  # 핀 번호 7
    'F': 84,  # 핀 번호 11
    'G': 65,  # 핀 번호 18
    'A': 86,  # 핀 번호 15
    'B': 90   # 핀 번호 16
}

# 버저 핀
BUZZER_PIN = 89  # 핀 번호 12

# GPIO 초기화
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

def read_gpio_value(gpio_number):
    gpio_value_path = GPIO_VALUE_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_value_path, 'r') as value_file:
            return int(value_file.read().strip())
    except IOError as e:
        print(f"Error reading GPIO {gpio_number} value: {e}")
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

if __name__ == "__main__":
    try:
        # GPIO 초기화
        export_gpio(BUZZER_PIN)
        set_gpio_direction(BUZZER_PIN, "out")

        for pin in BUTTON_PINS.values():
            export_gpio(pin)
            set_gpio_direction(pin, "in")

        print("Press a button to play a tone!")

        while True:
            for note, pin in BUTTON_PINS.items():
                if read_gpio_value(pin) == 0:  # 버튼 눌림 감지
                    print(f"Playing {note} ({FREQUENCIES[note]} Hz)")
                    play_tone(BUZZER_PIN, FREQUENCIES[note], 0.5)
                    time.sleep(0.1)  # 버튼 debounce 방지

    except KeyboardInterrupt:
        print("\nOperation stopped by User")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # GPIO 해제
        unexport_gpio(BUZZER_PIN)
        for pin in BUTTON_PINS.values():
            unexport_gpio(pin)

    sys.exit(0)
