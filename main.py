import math
import platform

import matplotlib.pyplot as plt

class CoolingCalculator:
    """뉴턴의 냉각 법칙을 기반으로 수식 연산을 담당하는 엔진 클래스"""
    def __init__(self, t0, ts, k):
        self.t0 = t0  # 초기 온도
        self.ts = ts  # 주변 온도
        self.k = k    # 냉각 계수

    def calculate_at_time(self, t):
        """특정 시간(t)에서의 온도를 반환 [cite: 79]"""
        return self.ts + (self.t0 - self.ts) * math.exp(-self.k * t)

    def calculate_time_to_target(self, target_t):
        """특정 온도에 도달하는 시간(t)을 역산 [cite: 8, 80]"""
        if self.k <= 0:
            return None

        # 목표 온도가 초기 온도와 주변 온도 사이에 있는지 확인 (냉각/가열 모두 지원)
        if not (min(self.t0, self.ts) < target_t < max(self.t0, self.ts)):
            return None

        return -(1/self.k) * math.log((target_t - self.ts) / (self.t0 - self.ts))

class CLIHandler:
    """사용자 인터페이스 및 가시화를 담당하는 클래스 [cite: 92]"""
    @staticmethod
    def _input_float(prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("  [!] 유효한 숫자를 입력해주세요.")

    @staticmethod
    def get_user_input():
        print("\n=== Thermo-Barista 분석기 입력 ===")
        t0 = CLIHandler._input_float("음료 온도(T0, °C): ")
        ts = CLIHandler._input_float("환경 온도(Ts, °C): ")

        print("\n[Tip] 일반적인 냉각 계수(k) 참고값:")
        print("  - 머그컵 (뚜껑 X): 0.03 ~ 0.05")
        print("  - 종이컵 (뚜껑 O): 0.02 ~ 0.03")
        print("  - 보온 텀블러: 0.005 ~ 0.01")
        k = CLIHandler._input_float("냉각 계수(k): ")
        target_t = CLIHandler._input_float("적정 온도(°C): ")
        return t0, ts, k, target_t

    @staticmethod
    def display_results(t0, ts, target_t, target_time):
        print("\n" + "="*30)
        print(f"{'분석 항목':<15} | {'결과값':<10}")
        print("-" * 30)
        print(f"{'음료 온도':<15} | {t0}°C")
        print(f"{'환경 온도':<15} | {ts}°C")
        print(f"{'적정 온도':<15} | {target_t}°C")
        print(f"{'골든 타임':<15} | {target_time:.2f}분 후")
        print("="*30)

    @staticmethod
    def plot_cooling_curve(calculator, target_t, target_time):
        """냉각 곡선 및 골든 타임 시각화 [cite: 12, 13]"""
        # numpy 의존성 제거: 순수 파이썬으로 등간격 데이터 생성 (0 ~ target_time*1.5, 100개 구간)
        times = [i * (target_time * 1.5) / 99 for i in range(100)]
        temps = [calculator.calculate_at_time(t) for t in times]

        # 한글 폰트 설정 및 마이너스 기호 깨짐 방지
        system_name = platform.system()
        if system_name == 'Windows':
            plt.rc('font', family='Malgun Gothic')
        elif system_name == 'Darwin':
            plt.rc('font', family='AppleGothic')
        else:
            plt.rc('font', family='NanumGothic')
        plt.rcParams['axes.unicode_minus'] = False

        plt.figure(figsize=(10, 6))
        plt.plot(times, temps, label='Cooling Curve', color='blue')
        plt.axhline(y=target_t, color='red', linestyle='--', label=f'Golden Temp ({target_t}°C)')
        plt.scatter(target_time, target_t, color='red', s=100, zorder=5, label='Golden Time Point')

        plt.title("Thermo-Barista: Beverage Cooling Prediction", fontsize=14)
        plt.xlabel("Time (minutes)", fontsize=12)
        plt.ylabel("Temperature (°C)", fontsize=12)
        plt.annotate(
            f'Golden Time: {target_time:.2f}min',
            xy=(target_time, target_t),
            xytext=(target_time + target_time * 0.1, target_t + (calculator.t0 - target_t) * 0.15),
            arrowprops=dict(facecolor='black', shrink=0.05)
        )
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

def main():
    # 1. 입력 (Input)
    t0, ts, k, target_t = CLIHandler.get_user_input()

    # 2. 로직 처리 (Process)
    calc = CoolingCalculator(t0, ts, k)
    target_time = calc.calculate_time_to_target(target_t)

    # 3. 출력 (Output)
    if target_time:
        CLIHandler.display_results(t0, ts, target_t, target_time)
        CLIHandler.plot_cooling_curve(calc, target_t, target_time)
    else:
        print("\n[오류] 목표 온도가 도달 불가능한 범위에 있거나, 냉각 계수(k)가 유효하지 않습니다.")

if __name__ == "__main__":
    main()