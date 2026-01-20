"""
Hippo Memory Package
해마 메모리 패키지 - 완성된 해마 구조 독립 패키지

이 패키지는 Grid Engine에서 완성된 해마(Hippocampus) 구조를 
독립적인 패키지로 정리한 것입니다.

구성 요소:
- Place Cells: 장소별 독립적인 기억
- Context Binder: 맥락별 기억 분리
- Learning Gate: 학습 조건 제어
- Replay/Consolidation: 기억 정제 및 장기 기억 고정
- Replay Buffer: 안정 구간 추출을 위한 버퍼
- Universal Memory: 범용 기억 메모리 인터페이스

Author: GNJz
Created: 2026-01-20
Version: v0.4.0-alpha (Hippocampus Completion)
License: MIT License
"""

from .hippocampus import (
    # Place Cells
    PlaceMemory,
    PlaceCellManager,
    # Context Binder
    ContextMemory,
    ContextBinder,
    # Learning Gate
    LearningGateConfig,
    LearningGate,
    # Replay/Consolidation
    PlaceMemoryWithHistory,
    ReplayConsolidation,
    ReplayConsolidationManager,
    # Replay Buffer
    TrajectoryPoint,
    ReplayBuffer,
    # Universal Memory Interface
    UniversalMemory,
    create_universal_memory,
)

__version__ = '0.4.0-alpha'
__author__ = 'GNJz'
__license__ = 'MIT'

__all__ = [
    # Place Cells
    'PlaceMemory',
    'PlaceCellManager',
    # Context Binder
    'ContextMemory',
    'ContextBinder',
    # Learning Gate
    'LearningGateConfig',
    'LearningGate',
    # Replay/Consolidation
    'PlaceMemoryWithHistory',
    'ReplayConsolidation',
    'ReplayConsolidationManager',
    # Replay Buffer
    'TrajectoryPoint',
    'ReplayBuffer',
    # Universal Memory Interface
    'UniversalMemory',
    'create_universal_memory',
]

