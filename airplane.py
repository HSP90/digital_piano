import math

# GPIO 핀 번호 설정
GPIO_PIN = 90  # 사용하려는 GPIO 핀 번호 (예: 18번)

# 각 음표의 지속 시간을 설정 (초)
NOTE_DURATIONS = {
    '1': 0.5,  # 기본 음표 지속 시간
    '2': 1.0,  # 2배 음표 지속 시간
}

# "비행기 노래" 악보 (음표와 지속 시간)
FLYING_SONG = [
    ('C', '1'), ('C', '1'), ('G', '1'), ('G', '1'), 
    ('A', '1'), ('A', '1'), ('G', '2'),
    ('F', '1'), ('F', '1'), ('E', '1'), ('E', '1'),
    ('D', '1'), ('D', '1'), ('C', '2'),
]

def play_tone(gpio_number, frequency, duration):
    """특정 음을 GPIO로 재생"""
    if frequency == 0:  # 휴지(쉼표)
        time.sleep(duration)
        return

    period = 1.0 / frequency  # 주기 (초)
    half_period = period / 2  # 반주기
    cycles = int(duration * frequency)  # 주기 반복 횟수

    for _ in range(cycles):
        set_gpio_value(gpio_number, 1)
        time.sleep(half_period)
        set_gpio_value(gpio_number, 0)
        time.sleep(half_period)

def play_song(song):
    """악보를 재생"""
    for note, duration_key in song:
        frequency = FREQUENCIES.get(note, 0)
        duration = NOTE_DURATIONS.get(duration_key, 0.5)
        play_tone(GPIO_PIN, frequency, duration)
        time.sleep(0.1)  # 음표 간 간격

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
