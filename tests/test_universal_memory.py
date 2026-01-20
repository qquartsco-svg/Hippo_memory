"""
Universal Memory 테스트

Author: GNJz
Created: 2026-01-20
Made in GNJz
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import unittest
from hippocampus import UniversalMemory, create_universal_memory


class TestUniversalMemory(unittest.TestCase):
    """Universal Memory 테스트"""
    
    def setUp(self):
        """테스트 설정"""
        self.memory = create_universal_memory(memory_dim=5)
    
    def test_store_and_retrieve(self):
        """저장 및 검색 테스트"""
        state = np.array([1.0, 0.5, 0.3, 10.0, 5.0])
        bias = np.array([0.001, 0.002, 0.0, 0.0, 0.0])
        
        # 저장
        self.memory.store(
            key=state,
            value=bias,
            context={"tool": "tool_A"}
        )
        
        # 검색
        memories = self.memory.retrieve(state, context={"tool": "tool_A"})
        
        self.assertGreater(len(memories), 0)
        self.assertIn("bias", memories[0])
        self.assertIn("confidence", memories[0])
    
    def test_augment(self):
        """증강 테스트"""
        state = np.array([1.0, 0.5, 0.3, 10.0, 5.0])
        bias = np.array([0.001, 0.002, 0.0, 0.0, 0.0])
        
        # 저장
        self.memory.store(
            key=state,
            value=bias,
            context={"tool": "tool_A"}
        )
        
        # 증강
        augmented = self.memory.augment(state, context={"tool": "tool_A"})
        
        self.assertIn("query", augmented)
        self.assertIn("context", augmented)
        self.assertIn("memories", augmented)
        self.assertIn("summary", augmented)
    
    def test_replay(self):
        """Replay 테스트"""
        state = np.array([1.0, 0.5, 0.3, 10.0, 5.0])
        bias = np.array([0.001, 0.002, 0.0, 0.0, 0.0])
        
        # 여러 번 저장
        for i in range(10):
            self.memory.store(
                key=state,
                value=bias,
                context={"tool": "tool_A"},
                timestamp=i * 1000.0
            )
        
        # Replay 수행
        replay_result = self.memory.replay(current_time=10000.0)
        
        self.assertIn("segments_processed", replay_result)
        self.assertIn("consolidated_count", replay_result)
        self.assertIn("total_places", replay_result)


if __name__ == "__main__":
    unittest.main()

