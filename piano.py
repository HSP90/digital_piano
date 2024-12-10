import os
import time

# GPIO 설정 경로
GPIO_EXPORT_PATH = "/sys/class/gpio/export"
GPIO_UNEXPORT_PATH = "/sys/class/gpio/unexport"
GPIO_DIRECTION_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/direction"
GPIO_VALUE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/value"

# 버튼과 음 대응 설정
BUTTON_GPIO_MAP = {
    83: 'C',
    84: 'D',
    85: 'E',
    86: 'F',
    87: 'G',
    88: 'A',
    89: 'B',
    90: 'C5'
}

FREQ_VALUES = {
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00,
    'A': 440.00,
    'B': 493.88,
    'C5': 523.25
}

# 부저 GPIO 핀
BUZZER_GPIO = 91

# GPIO 유틸리티 함수
def export_gpio(gpio_number):
    if not os.path.exists(f"/sys/class/gpio/gpio{gpio_number}"):
        with open(GPIO_EXPORT_PATH, 'w') as export_file:
            export_file.write(str(gpio_number))

def set_gpio_direction(gpio_number, direction):
    with open(GPIO_DIRECTION_PATH_TEMPLATE.format(gpio_number), 'w') as direction_file:
        direction_file.write(direction)

def get_gpio_value(gpio_number):
    with open(GPIO_VALUE_PATH_TEMPLATE.format(gpio_number), 'r') as value_file:
        return value_file.read().strip()

def set_gpio_value(gpio_number, value):
    with open(GPIO_VALUE_PATH_TEMPLATE.format(gpio_number), 'w') as value_file:
        value_file.write(str(value))

# 음 재생 함수
def play_tone(gpio_number, frequency, duration):
    period = 1.0 / frequency
    half_period = period / 2
    end_time = time.time() + duration
    while time.time() < end_time:
        set_gpio_value(gpio_number, 1)
        time.sleep(half_period)
        set_gpio_value(gpio_number, 0)
        time.sleep(half_period)

# 메인 코드
if __name__ == "__main__":
    try:
        # GPIO 초기화
        for gpio in BUTTON_GPIO_MAP.keys():
            export_gpio(gpio)
            set_gpio_direction(gpio, 'in')

        export_gpio(BUZZER_GPIO)
        set_gpio_direction(BUZZER_GPIO, 'out')

        print("버튼을 누르면 음이 재생됩니다.")

        while True:
            for gpio, note in BUTTON_GPIO_MAP.items():
                gpio_value = get_gpio_value(gpio)
                print(f"GPIO {gpio}: {gpio_value}")  # 현재 상태 출력
                if gpio_value == '1':  # 버튼이 눌린 경우
                    print(f"Button pressed: {note}")
                    play_tone(BUZZER_GPIO, FREQ_VALUES[note], 0.5)

                    # 버튼 해제 대기
                    while get_gpio_value(gpio) == '1':
                        pass  # 버튼 해제 대기

            time.sleep(0.1)  # 루프 안정화

    except KeyboardInterrupt:
        print("프로그램 종료 중...")
    finally:
        # GPIO 정리
        for gpio in BUTTON_GPIO_MAP.keys():
            with open(GPIO_UNEXPORT_PATH, 'w') as unexport_file:
                unexport_file.write(str(gpio))
        with open(GPIO_UNEXPORT_PATH, 'w') as unexport_file:
            unexport_file.write(str(BUZZER_GPIO))
