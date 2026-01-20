"""
Hippo Memory Package - 기본 사용 예시

해마 메모리 패키지의 기본 사용법을 보여주는 예시

Author: GNJz
Created: 2026-01-20
Made in GNJz
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from hippocampus import (
    UniversalMemory,
    create_universal_memory,
    PlaceCellManager,
    ContextBinder,
    LearningGate,
    ReplayConsolidation,
    ReplayBuffer
)


def demo_basic_memory():
    """기본 메모리 사용 예시"""
    print("\n" + "=" * 70)
    print("예시 1: 기본 메모리 사용")
    print("=" * 70)
    
    # 범용 메모리 생성
    memory = create_universal_memory(memory_dim=5)
    
    # 기억 저장
    state = np.array([1.0, 0.5, 0.3, 10.0, 5.0])
    bias = np.array([0.001, 0.002, 0.0, 0.0, 0.0])
    
    memory.store(
        key=state,
        value=bias,
        context={"tool": "tool_A", "temperature": 25.0}
    )
    
    print(f"저장된 상태: {state}")
    print(f"저장된 편향: {bias}")
    print(f"맥락: {{'tool': 'tool_A', 'temperature': 25.0}}")
    
    # 기억 검색
    memories = memory.retrieve(state, context={"tool": "tool_A"})
    
    print(f"\n검색된 기억: {len(memories)}개")
    for i, mem in enumerate(memories):
        print(f"  기억 {i+1}: 타입={mem['type']}, 편향={mem['bias']}, 신뢰도={mem['confidence']:.2f}")


def demo_place_cells():
    """Place Cells 사용 예시"""
    print("\n" + "=" * 70)
    print("예시 2: Place Cells 사용")
    print("=" * 70)
    
    # Place Cell Manager 생성
    place_manager = PlaceCellManager(
        num_places=1000,
        phase_wrap=2.0 * np.pi,
        quantization_level=100
    )
    
    # 위상 벡터 생성
    phase_vector = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    
    # Place ID 할당
    place_id = place_manager.get_place_id(phase_vector)
    print(f"위상 벡터: {phase_vector}")
    print(f"Place ID: {place_id}")
    
    # Place Memory 가져오기
    place_memory = place_manager.get_place_memory(place_id)
    
    # Bias 업데이트
    bias = np.array([0.001, 0.002, 0.0, 0.0, 0.0])
    place_memory.update_bias(bias, learning_rate=0.1)
    place_memory.place_center = phase_vector.copy()
    
    print(f"Place Memory 편향: {place_memory.bias_estimate}")
    print(f"방문 횟수: {place_memory.visit_count}")


def demo_context_binder():
    """Context Binder 사용 예시"""
    print("\n" + "=" * 70)
    print("예시 3: Context Binder 사용")
    print("=" * 70)
    
    # Context Binder 생성
    context_binder = ContextBinder(num_contexts=10000)
    
    # Place ID
    place_id = 123
    
    # Context 설정
    context_1 = {"tool": "tool_A", "temperature": 25.0}
    context_2 = {"tool": "tool_B", "temperature": 30.0}
    
    # Context ID 할당
    context_id_1 = context_binder.get_context_id(context_1)
    context_id_2 = context_binder.get_context_id(context_2)
    
    print(f"Context 1: {context_1}")
    print(f"Context ID 1: {context_id_1}")
    print(f"Context 2: {context_2}")
    print(f"Context ID 2: {context_id_2}")
    
    # Context별 Bias 저장
    bias_1 = np.array([0.001, 0.002, 0.0, 0.0, 0.0])
    bias_2 = np.array([0.002, 0.001, 0.0, 0.0, 0.0])
    
    context_binder.update_context_memory(
        place_id=place_id,
        context_id=context_id_1,
        bias=bias_1,
        current_time=0.0,
        learning_rate=0.1
    )
    
    context_binder.update_context_memory(
        place_id=place_id,
        context_id=context_id_2,
        bias=bias_2,
        current_time=0.0,
        learning_rate=0.1
    )
    
    # Context별 Bias 검색
    retrieved_bias_1 = context_binder.get_bias_estimate(place_id, context_id_1)
    retrieved_bias_2 = context_binder.get_bias_estimate(place_id, context_id_2)
    
    print(f"\nContext 1 편향: {retrieved_bias_1}")
    print(f"Context 2 편향: {retrieved_bias_2}")
    print("→ 동일 Place에서도 Context별로 다른 편향 저장 확인!")


def demo_replay_consolidation():
    """Replay/Consolidation 사용 예시"""
    print("\n" + "=" * 70)
    print("예시 4: Replay/Consolidation 사용")
    print("=" * 70)
    
    from hippocampus.place_cells import PlaceMemory
    
    # Place Memory 생성
    place_memory = PlaceMemory(place_id=123)
    
    # 여러 번 Bias 업데이트
    for i in range(5):
        bias = np.array([0.001 + i * 0.0001, 0.002, 0.0, 0.0, 0.0])
        place_memory.update_bias(bias, learning_rate=0.1)
        place_memory.add_bias_to_history(bias)
        place_memory.visit_count += 1
    
    print(f"Bias 이력 길이: {len(place_memory.bias_history)}")
    print(f"방문 횟수: {place_memory.visit_count}")
    print(f"현재 편향: {place_memory.bias_estimate}")
    
    # Replay Consolidation 생성
    replay_consolidation = ReplayConsolidation(
        replay_threshold=1.0,
        consolidation_window=3,
        significance_threshold=0.1
    )
    
    # Consolidation 수행
    consolidated = replay_consolidation.consolidate_place_memory(
        place_memory,
        current_time=2.0
    )
    
    print(f"Consolidation 결과: {consolidated}")
    if consolidated and hasattr(place_memory, 'consolidated_bias'):
        print(f"Consolidated Bias: {place_memory.consolidated_bias}")


def main():
    """메인 함수"""
    print("\n" + "=" * 70)
    print("Hippo Memory Package - 기본 사용 예시")
    print("=" * 70)
    
    # 예시 실행
    demo_basic_memory()
    demo_place_cells()
    demo_context_binder()
    demo_replay_consolidation()
    
    print("\n" + "=" * 70)
    print("예시 완료")
    print("=" * 70)


if __name__ == "__main__":
    main()

