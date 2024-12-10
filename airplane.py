import os
import time
import sys

# GPIO 파일 경로 템플릿
GPIO_EXPORT_PATH = "/sys/class/gpio/export"
GPIO_UNEXPORT_PATH = "/sys/class/gpio/unexport"
GPIO_DIRECTION_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/direction"
GPIO_VALUE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/value"
GPIO_BASE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}"

# GPIO 핀 번호
GPIO_PIN = 90

# 음계 주파수 (Hz)
FREQUENCIES = {
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00,
    'A': 440.00,
    'B': 493.88,
    'C5': 523.25
}

# 음표 지속 시간 (초)
NOTE_DURATIONS = {
    '1': 0.5,  # 기본 지속 시간
    '2': 1.0   # 두 배 지속 시간
}

# "비행기 노래" 악보
FLYING_SONG = [
    ('C', '1'), ('C', '1'), ('G', '1'), ('G', '1'),
    ('A', '1'), ('A', '1'), ('G', '2'),
    ('F', '1'), ('F', '1'), ('E', '1'), ('E', '1'),
    ('D', '1'), ('D', '1'), ('C', '2'),
]

# GPIO 관련 함수
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

# 음 재생 함수
def play_tone(gpio_number, frequency, duration):
    """특정 음을 GPIO로 재생"""
    if frequency == 0:  # 휴지(쉼표)
        time.sleep(duration)
        return

    period = 1.0 / frequency  # 주기 (초)
    half_period = period / 2  # 반주기
    cycles = int(duration * frequency)  # 주기 반복 횟수

    for _ in range(cycles):
        set_gpio_value(gpio_number, 1)  # GPIO ON
        time.sleep(half_period)
        set_gpio_value(gpio_number, 0)  # GPIO OFF
        time.sleep(half_period)

# 노래 재생 함수
def play_song(song):
    """악보를 재생"""
    for note, duration_key in song:
        frequency = FREQUENCIES.get(note, 0)
        duration = NOTE_DURATIONS.get(duration_key, 0.5)
        play_tone(GPIO_PIN, frequency, duration)
        time.sleep(0.1)  # 음표 간 짧은 간격 추가

# 메인 함수
def main():
    # GPIO 핀 설정
    export_gpio(GPIO_PIN)
    set_gpio_direction(GPIO_PIN, "out")

    try:
        # 노래 재생
        print("비행기 노래를 재생합니다!")
        play_song(FLYING_SONG)
    finally:
        # GPIO 핀 해제
        unexport_gpio(GPIO_PIN)
        print("재생 완료, GPIO 핀 해제됨.")

if __name__ == "__main__":
    main()
