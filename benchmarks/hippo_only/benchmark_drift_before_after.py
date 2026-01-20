"""
Hippo Memory 독립 벤치마크: Before/After 비교

목적:
- Grid Engine 없이 Hippo Memory만으로 실행 가능
- "딕셔너리 vs 실제로 작동하는 시스템" 차이를 수치로 증명
- Before (PID only) vs After (PID + Hippo Memory) 비교

시나리오:
1. 1D 위치 제어 시뮬레이션
2. 온도/부하에 따라 drift 발생
3. PID만 쓰면 누적 오차
4. Hippo Memory 붙이면 장소별 bias 기억

측정 지표:
- Drift RMS (누적 오차)
- Final Error (최종 오차)
- 재방문 시 오차 수렴 속도

Author: GNJz
Created: 2026-01-20
Made in GNJz
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import time
from typing import List, Tuple, Dict
from hippocampus import create_universal_memory


class SimplePID:
    """간단한 PID 제어기"""
    
    def __init__(self, kp=0.5, ki=0.05, kd=0.005):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.last_error = 0.0
        self.integral_limit = 0.1  # Integral windup 방지
    
    def compute(self, error: float, dt: float = 0.01) -> float:
        """PID 출력 계산"""
        self.integral += error * dt
        # Integral windup 방지
        self.integral = np.clip(self.integral, -self.integral_limit, self.integral_limit)
        derivative = (error - self.last_error) / dt if dt > 0 else 0.0
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.last_error = error
        return np.clip(output, -1.0, 1.0)  # 출력 제한
    
    def reset(self):
        """PID 리셋"""
        self.integral = 0.0
        self.last_error = 0.0


class DriftSimulator:
    """
    물리적 드리프트 시뮬레이터
    
    실제 CNC/로봇에서 발생하는 물리적 현상 모사:
    1. 열 변형: 위치별 고유한 열 팽창 계수 (재방문 시 동일)
    2. 시간 드리프트: 장시간 작동 시 누적되는 시스템 변형
    3. 백래시: 방향 전환 시 발생하는 유격
    """
    
    def __init__(
        self,
        thermal_coefficient: float = 0.00001,  # 열 팽창 계수 (mm/°C/mm)
        time_drift_rate: float = 0.0001,  # 시간 드리프트 속도 (mm/step)
        backlash: float = 0.0005,  # 백래시 (mm)
        temperature: float = 25.0  # 초기 온도 (°C)
    ):
        self.thermal_coefficient = thermal_coefficient
        self.time_drift_rate = time_drift_rate
        self.backlash = backlash
        self.temperature = temperature
        
        self.accumulated_time_drift = 0.0
        self.position_thermal_drifts = {}  # 위치별 열 변형 저장
        self.last_direction = 0  # 마지막 이동 방향 (백래시 계산용)
    
    def get_drift(
        self,
        position: float,
        time_step: int,
        target: float = None
    ) -> float:
        """
        물리적 드리프트 계산
        
        Args:
            position: 현재 위치 (mm)
            time_step: 시간 스텝
            target: 목표 위치 (백래시 계산용)
        
        Returns:
            총 드리프트 (mm)
        """
        # 1. 열 변형: 위치별 고유한 열 팽창 (재방문 시 동일)
        position_key = round(position, 1)
        if position_key not in self.position_thermal_drifts:
            # 각 위치마다 고유한 열 변형 계수 (물리적 특성)
            # 실제로는 재료/구조에 따라 다르지만, 여기서는 위치에 따라 변하는 것으로 모사
            thermal_expansion = self.thermal_coefficient * position_key * (self.temperature - 20.0)
            self.position_thermal_drifts[position_key] = thermal_expansion
        
        thermal_drift = self.position_thermal_drifts[position_key]
        
        # 2. 시간 드리프트: 장시간 작동 시 누적
        self.accumulated_time_drift += self.time_drift_rate
        
        # 3. 백래시: 방향 전환 시 발생
        backlash_drift = 0.0
        if target is not None:
            direction = 1 if target > position else -1
            if direction != self.last_direction and self.last_direction != 0:
                # 방향 전환 시 백래시 발생
                backlash_drift = self.backlash * direction
            self.last_direction = direction
        
        # 총 드리프트
        total_drift = thermal_drift + self.accumulated_time_drift + backlash_drift
        
        return total_drift


def run_simulation_without_hippo(
    target_positions: List[float],
    n_repeats: int = 10,
    thermal_coefficient: float = 0.00001,
    time_drift_rate: float = 0.0001,
    backlash: float = 0.0005,
    noise_std: float = 0.00001
) -> Dict:
    """
    Hippo Memory 없이 시뮬레이션 (Baseline)
    
    Args:
        target_positions: 목표 위치 리스트
        n_repeats: 반복 횟수
        thermal_coefficient: 열 팽창 계수
        time_drift_rate: 시간 드리프트 속도
        backlash: 백래시 크기
        noise_std: 노이즈 표준 편차
    """
    
    pid = SimplePID(kp=1.0, ki=0.1, kd=0.01)
    drift_sim = DriftSimulator(
        thermal_coefficient=thermal_coefficient,
        time_drift_rate=time_drift_rate,
        backlash=backlash
    )
    
    errors = []
    positions = []
    time_steps = []
    
    current_pos = 0.0  # 초기 위치
    
    for repeat in range(n_repeats):
        for step, target in enumerate(target_positions):
            time_step = repeat * len(target_positions) + step
            
            # 물리적 드리프트 계산
            drift = drift_sim.get_drift(current_pos, time_step, target=target)
            noise = np.random.normal(0, noise_std)
            measured_pos = current_pos + drift + noise
            
            # 오차 계산
            error = target - measured_pos
            
            # PID 제어
            control = pid.compute(error, dt=0.01)
            new_pos = current_pos + control
            
            errors.append(error)
            positions.append(new_pos)
            time_steps.append(time_step)
            
            current_pos = new_pos
    
    # 통계 계산
    errors_array = np.array(errors)
    drift_rms = np.sqrt(np.mean(errors_array[-len(target_positions):]**2))
    final_error = np.abs(errors_array[-1])
    
    return {
        'errors': errors,
        'positions': positions,
        'time_steps': time_steps,
        'drift_rms': drift_rms,
        'final_error': final_error,
        'all_errors': errors_array
    }


def run_simulation_with_hippo(
    target_positions: List[float],
    n_repeats: int = 10,
    thermal_coefficient: float = 0.00001,
    time_drift_rate: float = 0.0001,
    backlash: float = 0.0005,
    noise_std: float = 0.00001,
    learning_rate: float = 0.1,
    stability_threshold: float = 0.1
) -> Dict:
    """
    Hippo Memory와 함께 시뮬레이션
    
    Args:
        target_positions: 목표 위치 리스트
        n_repeats: 반복 횟수
        thermal_coefficient: 열 팽창 계수
        time_drift_rate: 시간 드리프트 속도
        backlash: 백래시 크기
        noise_std: 노이즈 표준 편차
        learning_rate: 학습률
        stability_threshold: 안정 구간 판단 임계값
    """
    
    pid = SimplePID(kp=1.0, ki=0.1, kd=0.01)
    drift_sim = DriftSimulator(
        thermal_coefficient=thermal_coefficient,
        time_drift_rate=time_drift_rate,
        backlash=backlash
    )
    memory = create_universal_memory(memory_dim=5)
    
    errors = []
    positions = []
    time_steps = []
    corrections = []
    stored_count = 0
    
    current_pos = 0.0
    
    for repeat in range(n_repeats):
        for step, target in enumerate(target_positions):
            time_step = repeat * len(target_positions) + step
            
            # 물리적 드리프트 계산
            drift = drift_sim.get_drift(current_pos, time_step, target=target)
            noise = np.random.normal(0, noise_std)
            measured_pos = current_pos + drift + noise
            
            # Hippo Memory에서 기억 검색
            state = np.array([current_pos, 0.0, 0.0, 0.0, 0.0])
            memories = memory.retrieve(state, context={})
            
            # 기억된 편향으로 보정 (물리적 보정)
            correction = 0.0
            if memories:
                learned_bias = memories[0]['bias'][0]
                visit_count = memories[0].get('visit_count', 1)
                confidence = min(visit_count / 5.0, 1.0)  # 5회 이상 방문 시 최대 신뢰도
                correction = -learned_bias * confidence
            
            # 오차 계산 (보정 전)
            error = target - measured_pos
            
            # PID 제어
            control = pid.compute(error, dt=0.01)
            # 물리적 위치 업데이트: 제어 출력 + 보정값
            # 보정값은 학습된 편향을 직접 보상하므로 위치에 추가
            new_pos = current_pos + control + correction
            
            # Hippo Memory에 편향 저장 (안정 구간에서만)
            is_stable = abs(error) < stability_threshold
            if is_stable:
                bias = np.array([drift, 0.0, 0.0, 0.0, 0.0])
                memory.store(
                    key=state,
                    value=bias,
                    context={},
                    timestamp=time_step * 0.01
                )
                stored_count += 1
            
            errors.append(error)
            positions.append(new_pos)
            time_steps.append(time_step)
            corrections.append(correction)
            
            current_pos = new_pos
        
        # Replay (휴지기)
        if repeat < n_repeats - 1:
            memory.replay(current_time=(repeat + 1) * len(target_positions) * 0.01)
    
    errors_array = np.array(errors)
    drift_rms = np.sqrt(np.mean(errors_array[-len(target_positions):]**2))
    final_error = np.abs(errors_array[-1])
    
    return {
        'errors': errors,
        'positions': positions,
        'time_steps': time_steps,
        'corrections': corrections,
        'drift_rms': drift_rms,
        'final_error': final_error,
        'all_errors': errors_array,
        'stored_count': stored_count
    }


def main():
    """메인 벤치마크 실행"""
    
    print("=" * 70)
    print("Hippo Memory 독립 벤치마크: Before/After 비교")
    print("=" * 70)
    print()
    
    # 물리적 시뮬레이션 파라미터 (하드코딩 제거)
    target_positions = [0.0, 1.0, 2.0, 1.0, 0.0]  # A->B->C->B->A (재방문)
    n_repeats = 50
    
    # 물리적 파라미터 (실제 CNC/로봇 값 기반)
    thermal_coefficient = 0.00001  # 알루미늄: ~23e-6 /°C/mm
    time_drift_rate = 0.0001  # 장시간 작동 시 누적 변형
    backlash = 0.0005  # 일반적인 백래시
    noise_std = 0.00001  # 센서 노이즈
    stability_threshold = 0.1  # 안정 구간 판단 (에러 < 0.1mm)
    
    print(f"시뮬레이션 파라미터:")
    print(f"  - 목표 위치: {target_positions}")
    print(f"  - 반복 횟수: {n_repeats}")
    print(f"  - 열 팽창 계수: {thermal_coefficient}")
    print(f"  - 시간 드리프트 속도: {time_drift_rate}")
    print(f"  - 백래시: {backlash}")
    print(f"  - 안정 구간 임계값: {stability_threshold}")
    print()
    
    # Baseline (PID only)
    print("Baseline (PID only) 실행 중...")
    baseline_result = run_simulation_without_hippo(
        target_positions=target_positions,
        n_repeats=n_repeats,
        thermal_coefficient=thermal_coefficient,
        time_drift_rate=time_drift_rate,
        backlash=backlash,
        noise_std=noise_std
    )
    
    # Hippo Memory (PID + Hippo Memory)
    print("Hippo Memory (PID + Hippo Memory) 실행 중...")
    hippo_result = run_simulation_with_hippo(
        target_positions=target_positions,
        n_repeats=n_repeats,
        thermal_coefficient=thermal_coefficient,
        time_drift_rate=time_drift_rate,
        backlash=backlash,
        noise_std=noise_std,
        stability_threshold=stability_threshold
    )
    
    # 결과 출력
    print()
    print("=" * 70)
    print("벤치마크 결과")
    print("=" * 70)
    print()
    
    print(f"[Baseline PID]")
    print(f"  Drift RMS: {baseline_result['drift_rms']:.6f}")
    print(f"  Final Error: {baseline_result['final_error']:.6f}")
    print()
    
    print(f"[PID + Hippo Memory]")
    print(f"  Drift RMS: {hippo_result['drift_rms']:.6f}")
    print(f"  Final Error: {hippo_result['final_error']:.6f}")
    print(f"  편향 저장 횟수: {hippo_result.get('stored_count', 0)}")
    print()
    
    # 개선율 계산
    drift_improvement = (baseline_result['drift_rms'] - hippo_result['drift_rms']) / baseline_result['drift_rms'] * 100
    error_improvement = (baseline_result['final_error'] - hippo_result['final_error']) / baseline_result['final_error'] * 100
    
    print(f"[개선율]")
    # 개선율은 음수로 표시 (오차 감소)
    print(f"  Drift RMS: {drift_improvement:+.1f}% (↓ {abs(drift_improvement):.1f}%)")
    print(f"  Final Error: {error_improvement:+.1f}% (↓ {abs(error_improvement):.1f}%)")
    print()
    
    # 보정값 통계
    corrections = np.array(hippo_result['corrections'])
    non_zero_corrections = corrections[np.abs(corrections) > 1e-6]
    if len(non_zero_corrections) > 0:
        print(f"[보정값 통계]")
        print(f"  보정값이 0이 아닌 경우: {len(non_zero_corrections)} / {len(corrections)}")
        print(f"  평균 보정값: {np.mean(np.abs(non_zero_corrections)):.6f}")
        print(f"  최대 보정값: {np.max(np.abs(non_zero_corrections)):.6f}")
        print()
    
    # 결과 반환 (시각화용)
    return {
        'baseline': baseline_result,
        'hippo': hippo_result,
        'improvements': {
            'drift_rms': drift_improvement,
            'final_error': error_improvement
        }
    }


if __name__ == "__main__":
    results = main()

