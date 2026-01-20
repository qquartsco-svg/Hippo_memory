"""
CNC 축 시뮬레이션: Hippo Memory를 사용한 열 변형 보정

실제 산업용 시나리오:
- CNC 머신의 X축이 온도에 따라 열 변형 발생
- 동일 위치 재방문 시 편향이 누적됨
- Hippo Memory가 위치별 편향을 기억하여 보정

Author: GNJz
Created: 2026-01-20
Made in GNJz
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from hippocampus import create_universal_memory


class CNCAxisSimulator:
    """CNC 축 시뮬레이터"""
    
    def __init__(self, use_hippo: bool = False):
        self.use_hippo = use_hippo
        self.memory = create_universal_memory(memory_dim=1) if use_hippo else None
        self.position = 0.0
        self.temperature = 25.0  # 초기 온도 (Celsius)
        
    def thermal_expansion(self, position: float) -> float:
        """열 변형 계산 (위치별)"""
        # 위치별 열 변형 계수 (실제로는 복잡하지만 간단히 모사)
        expansion_coeff = 0.00001  # 1mm per 100mm per degree
        thermal_drift = (self.temperature - 25.0) * expansion_coeff * position
        return thermal_drift
    
    def move_to(self, target: float, temperature: float = None):
        """목표 위치로 이동"""
        if temperature is not None:
            self.temperature = temperature
        
        # 열 변형으로 인한 실제 위치
        thermal_drift = self.thermal_expansion(target)
        actual_position = target + thermal_drift
        
        # Hippo Memory 보정
        correction = 0.0
        if self.use_hippo and self.memory:
            state = np.array([target])
            memories = self.memory.retrieve(state, context={"temperature": self.temperature})
            if memories:
                correction = -memories[0]['bias'][0]
        
        # 보정 후 위치
        corrected_position = actual_position + correction
        
        # 오차
        error = target - corrected_position
        
        # Hippo Memory에 편향 저장 (안정 구간에서만)
        if self.use_hippo and self.memory and abs(error) < 0.001:
            bias = np.array([thermal_drift])
            self.memory.store(
                key=state,
                value=bias,
                context={"temperature": self.temperature}
            )
        
        self.position = corrected_position
        return error, correction, thermal_drift


def simulate_cnc_operation(use_hippo: bool = False, n_cycles: int = 10):
    """CNC 작업 시뮬레이션"""
    
    simulator = CNCAxisSimulator(use_hippo=use_hippo)
    
    # 작업 경로: A -> B -> C -> B -> A (재방문)
    path = [0.0, 100.0, 200.0, 100.0, 0.0]  # mm
    
    errors = []
    corrections = []
    thermal_drifts = []
    positions = []
    temperatures = []
    
    for cycle in range(n_cycles):
        # 온도 변화 (작업 중 온도 상승)
        temperature = 25.0 + cycle * 0.5  # 매 사이클마다 0.5도 상승
        
        for target in path:
            error, correction, thermal_drift = simulator.move_to(target, temperature)
            
            errors.append(error)
            corrections.append(correction)
            thermal_drifts.append(thermal_drift)
            positions.append(simulator.position)
            temperatures.append(temperature)
        
        # Replay (휴지기)
        if use_hippo and simulator.memory:
            simulator.memory.replay(current_time=cycle * len(path) * 0.1)
    
    return {
        'errors': errors,
        'corrections': corrections,
        'thermal_drifts': thermal_drifts,
        'positions': positions,
        'temperatures': temperatures
    }


def main():
    """메인 실행 함수"""
    
    print("=" * 70)
    print("CNC 축 시뮬레이션: 열 변형 보정")
    print("=" * 70)
    print()
    
    # Baseline (Hippo Memory 없음)
    print("Baseline (Hippo Memory 없음) 실행 중...")
    baseline = simulate_cnc_operation(use_hippo=False, n_cycles=10)
    
    # Hippo Memory 사용
    print("Hippo Memory 사용 실행 중...")
    hippo = simulate_cnc_operation(use_hippo=True, n_cycles=10)
    
    # 결과 출력
    print()
    print("=" * 70)
    print("결과 비교")
    print("=" * 70)
    print()
    
    baseline_rms = np.sqrt(np.mean(np.array(baseline['errors'])**2))
    hippo_rms = np.sqrt(np.mean(np.array(hippo['errors'])**2))
    
    print(f"[Baseline]")
    print(f"  RMS Error: {baseline_rms:.6f} mm")
    print(f"  Max Error: {np.max(np.abs(baseline['errors'])):.6f} mm")
    print()
    
    print(f"[Hippo Memory]")
    print(f"  RMS Error: {hippo_rms:.6f} mm")
    print(f"  Max Error: {np.max(np.abs(hippo['errors'])):.6f} mm")
    print()
    
    improvement = (baseline_rms - hippo_rms) / baseline_rms * 100
    print(f"[개선율]")
    print(f"  RMS Error: {improvement:+.1f}%")
    print()
    
    # 시각화
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # 1. Error vs Time
    ax1 = axes[0]
    time_steps = range(len(baseline['errors']))
    ax1.plot(time_steps, baseline['errors'], 
             label='Baseline (No Hippo Memory)', alpha=0.7, linewidth=1.5)
    ax1.plot(time_steps, hippo['errors'], 
             label='With Hippo Memory', alpha=0.7, linewidth=1.5)
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('Error (mm)')
    ax1.set_title('CNC Axis Error: Before/After Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Thermal Drift vs Correction
    ax2 = axes[1]
    ax2.plot(time_steps, baseline['thermal_drifts'], 
             label='Thermal Drift', alpha=0.7, linewidth=1.5, linestyle='--')
    ax2.plot(time_steps, hippo['corrections'], 
             label='Hippo Memory Correction', alpha=0.7, linewidth=1.5)
    ax2.set_xlabel('Time Step')
    ax2.set_ylabel('Value (mm)')
    ax2.set_title('Thermal Drift vs Hippo Memory Correction')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('examples/cnc_axis_comparison.png', dpi=150, bbox_inches='tight')
    print(f"그래프 저장: examples/cnc_axis_comparison.png")
    plt.show()
    
    return baseline, hippo


if __name__ == "__main__":
    main()

