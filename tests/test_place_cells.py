"""
Place Cells 테스트

Author: GNJz
Created: 2026-01-20
Made in GNJz
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import unittest
from hippocampus import PlaceCellManager, PlaceMemory


class TestPlaceCells(unittest.TestCase):
    """Place Cells 테스트"""
    
    def setUp(self):
        """테스트 설정"""
        self.place_manager = PlaceCellManager(
            num_places=1000,
            phase_wrap=2.0 * np.pi,
            quantization_level=100
        )
    
    def test_place_id_assignment(self):
        """Place ID 할당 테스트"""
        phase_vector = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        place_id = self.place_manager.get_place_id(phase_vector)
        
        self.assertIsInstance(place_id, int)
        self.assertGreaterEqual(place_id, 0)
        self.assertLess(place_id, 1000)
    
    def test_place_memory_storage(self):
        """Place Memory 저장 테스트"""
        phase_vector = np.array([1.0, 0.5, 0.3, 10.0, 5.0])
        place_id = self.place_manager.get_place_id(phase_vector)
        
        place_memory = self.place_manager.get_place_memory(place_id)
        place_memory.place_center = phase_vector.copy()
        
        bias = np.array([0.001, 0.002, 0.0, 0.0, 0.0])
        place_memory.update_bias(bias, learning_rate=0.1)
        
        self.assertIsNotNone(place_memory.place_center)
        self.assertIsNotNone(place_memory.bias_estimate)
        # 첫 방문 시에는 bias가 그대로 저장됨 (learning_rate 적용 안 됨)
        np.testing.assert_array_almost_equal(place_memory.bias_estimate, bias, decimal=5)
        
        # 두 번째 방문 시에는 learning_rate가 적용됨
        new_bias = np.array([0.002, 0.003, 0.0, 0.0, 0.0])
        place_memory.update_bias(new_bias, learning_rate=0.1)
        expected = 0.1 * new_bias + 0.9 * bias
        np.testing.assert_array_almost_equal(place_memory.bias_estimate, expected, decimal=5)
    
    def test_place_blending(self):
        """Place Blending 테스트"""
        phase_vector = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        
        # 여러 Place에 Bias 저장
        for i in range(3):
            test_phase = phase_vector + np.array([i * 0.01, 0, 0, 0, 0])
            place_id = self.place_manager.get_place_id(test_phase)
            place_memory = self.place_manager.get_place_memory(place_id)
            place_memory.place_center = test_phase.copy()
            place_memory.update_bias(np.array([i * 0.001, 0, 0, 0, 0]), learning_rate=0.1)
        
        # Blending으로 Bias 검색
        blended_bias = self.place_manager.get_bias_estimate(
            phase_vector,
            use_blending=True,
            top_k=3,
            sigma=0.5
        )
        
        self.assertIsNotNone(blended_bias)
        self.assertEqual(len(blended_bias), 5)


if __name__ == "__main__":
    unittest.main()

