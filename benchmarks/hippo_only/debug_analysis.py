"""
벤치마크 디버깅 및 분석

Hippo Memory가 왜 효과를 보이지 않는지 분석

Author: GNJz
Created: 2026-01-20
Made in GNJz
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
from hippocampus import create_universal_memory


def analyze_memory_behavior():
    """메모리 동작 분석"""
    
    print("=" * 70)
    print("Hippo Memory 동작 분석")
    print("=" * 70)
    print()
    
    memory = create_universal_memory(memory_dim=5)
    
    # 테스트: 위치별 편향 저장 및 검색
    positions = [0.0, 0.1, 0.2, 0.1, 0.0]  # A->B->C->B->A
    
    print("1. 저장 테스트")
    print("-" * 70)
    
    for i, pos in enumerate(positions):
        state = np.array([pos, 0.0, 0.0, 0.0, 0.0])
        bias = np.array([0.001 * (i % 3), 0.0, 0.0, 0.0, 0.0])  # 위치별 다른 편향
        
        memory.store(
            key=state,
            value=bias,
            context={},
            timestamp=i * 0.01
        )
        
        print(f"  Step {i}: 위치={pos:.1f}, 편향={bias[0]:.6f} 저장")
    
    print()
    print("2. 검색 테스트")
    print("-" * 70)
    
    for i, pos in enumerate(positions):
        state = np.array([pos, 0.0, 0.0, 0.0, 0.0])
        memories = memory.retrieve(state, context={})
        
        print(f"  Step {i}: 위치={pos:.1f}")
        print(f"    검색된 기억: {len(memories)}개")
        if memories:
            for j, mem in enumerate(memories[:3]):  # 최대 3개만 출력
                print(f"      [{j}] 타입={mem['type']}, 편향={mem['bias'][0]:.6f}, 신뢰도={mem['confidence']:.3f}")
        else:
            print(f"      ❌ 기억 없음!")
        print()
    
    print("3. Place ID 분석")
    print("-" * 70)
    
    from hippocampus import PlaceCellManager
    place_manager = PlaceCellManager(num_places=1000, phase_wrap=2.0 * np.pi, quantization_level=100)
    
    for i, pos in enumerate(positions):
        state = np.array([pos, 0.0, 0.0, 0.0, 0.0])
        place_id = place_manager.get_place_id(state)
        place_memory = place_manager.get_place_memory(place_id)
        
        print(f"  위치={pos:.1f}: Place ID={place_id}, 방문={place_memory.visit_count}, 편향={place_memory.bias_estimate[0]:.6f}")
    
    print()
    print("4. 재방문 테스트 (A 재방문)")
    print("-" * 70)
    
    # A 위치 재방문
    state_A = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    memories_A = memory.retrieve(state_A, context={})
    
    print(f"  위치 A (0.0) 재방문:")
    print(f"    검색된 기억: {len(memories_A)}개")
    if memories_A:
        for j, mem in enumerate(memories_A[:3]):
            print(f"      [{j}] 타입={mem['type']}, 편향={mem['bias'][0]:.6f}, 신뢰도={mem['confidence']:.3f}")
    else:
        print(f"      ❌ 기억 없음!")
    
    print()
    print("5. Replay 테스트")
    print("-" * 70)
    
    replay_result = memory.replay(current_time=1.0)
    print(f"  Replay 결과:")
    print(f"    처리된 세그먼트: {replay_result.get('segments_processed', 0)}")
    print(f"    통합된 Place 수: {replay_result.get('consolidated_count', 0)}")
    
    # Replay 후 재검색
    memories_A_after = memory.retrieve(state_A, context={})
    print(f"  Replay 후 위치 A 재검색:")
    print(f"    검색된 기억: {len(memories_A_after)}개")
    if memories_A_after:
        for j, mem in enumerate(memories_A_after[:3]):
            print(f"      [{j}] 타입={mem['type']}, 편향={mem['bias'][0]:.6f}, 신뢰도={mem['confidence']:.3f}")


def analyze_benchmark_issues():
    """벤치마크 문제점 분석"""
    
    print()
    print("=" * 70)
    print("벤치마크 문제점 분석")
    print("=" * 70)
    print()
    
    print("가능한 문제점:")
    print()
    print("1. 위치 해상도 문제")
    print("   - 위치가 너무 가까워서 같은 Place ID로 매핑됨")
    print("   - 해결: quantization_level 조정 또는 위치 간격 증가")
    print()
    print("2. 편향 저장 조건이 너무 엄격함")
    print("   - abs(error) < 0.01 조건이 만족되지 않음")
    print("   - 해결: 조건 완화 또는 다른 조건 사용")
    print()
    print("3. 보정값이 너무 작아서 효과 없음")
    print("   - 학습된 편향이 작아서 보정 효과가 미미함")
    print("   - 해결: 드리프트 크기 증가 또는 학습률 조정")
    print()
    print("4. 재방문 시나리오가 제대로 작동하지 않음")
    print("   - 같은 위치를 재방문해도 다른 Place ID로 인식됨")
    print("   - 해결: 위치 정확도 향상 또는 Place ID 매핑 로직 수정")
    print()
    print("5. Replay가 제대로 작동하지 않음")
    print("   - Replay phase에서 학습이 발생하지 않음")
    print("   - 해결: Replay 조건 확인 및 로직 수정")


if __name__ == "__main__":
    analyze_memory_behavior()
    analyze_benchmark_issues()

