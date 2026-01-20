"""
Place Cells 시각화: 기억이 형성되는 과정

Place Cells가 활성화되고 bias가 학습되는 과정을 시각화

Author: GNJz
Created: 2026-01-20
Made in GNJz
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from hippocampus import PlaceCellManager


def visualize_place_cells():
    """Place Cells 활성화 및 학습 과정 시각화"""
    
    # Place Cell Manager 생성
    place_manager = PlaceCellManager(
        num_places=100,
        phase_wrap=2.0 * np.pi,
        quantization_level=50
    )
    
    # 시뮬레이션: 여러 위치를 반복 방문하며 편향 학습
    positions = np.linspace(0, 2 * np.pi, 20)  # 20개 위치
    n_repeats = 5  # 5회 반복
    
    place_activations = []
    bias_estimates = []
    visit_counts = []
    
    for repeat in range(n_repeats):
        for pos in positions:
            phase_vector = np.array([pos])
            place_id = place_manager.get_place_id(phase_vector)
            place_memory = place_manager.get_place_memory(place_id)
            
            # Place center 설정
            if place_memory.place_center is None:
                place_memory.place_center = phase_vector.copy()
            
            # 편향 학습 (시뮬레이션: 위치별 고유 편향)
            true_bias = 0.001 * np.sin(pos)  # 위치별 고유 편향
            place_memory.update_bias(np.array([true_bias]), learning_rate=0.1)
            
            # 활성화 계산
            activation = place_manager._calculate_activation(phase_vector, place_memory.place_center)
            
            place_activations.append(activation)
            bias_estimates.append(place_memory.bias_estimate[0])
            visit_counts.append(place_memory.visit_count)
    
    # 시각화
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # 1. Place Cell 활성화 맵
    ax1 = axes[0]
    all_positions = np.tile(positions, n_repeats)
    scatter = ax1.scatter(all_positions, place_activations, 
                         c=visit_counts, cmap='viridis', 
                         s=50, alpha=0.6)
    ax1.set_xlabel('Position (rad)')
    ax1.set_ylabel('Place Cell Activation')
    ax1.set_title('Place Cell Activation Map')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax1, label='Visit Count')
    
    # 2. Bias 학습 곡선
    ax2 = axes[1]
    true_biases = 0.001 * np.sin(positions)
    learned_biases = []
    for pos in positions:
        phase_vector = np.array([pos])
        place_id = place_manager.get_place_id(phase_vector)
        place_memory = place_manager.get_place_memory(place_id)
        learned_biases.append(place_memory.bias_estimate[0])
    
    ax2.plot(positions, true_biases, 'r--', label='True Bias', linewidth=2)
    ax2.plot(positions, learned_biases, 'b-', label='Learned Bias', linewidth=2, marker='o')
    ax2.set_xlabel('Position (rad)')
    ax2.set_ylabel('Bias')
    ax2.set_title('Bias Learning: True vs Learned')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. 방문 횟수 히스토그램
    ax3 = axes[2]
    unique_place_ids = set()
    for pos in positions:
        phase_vector = np.array([pos])
        place_id = place_manager.get_place_id(phase_vector)
        unique_place_ids.add(place_id)
    
    visit_counts_per_place = []
    for place_id in unique_place_ids:
        place_memory = place_manager.get_place_memory(place_id)
        visit_counts_per_place.append(place_memory.visit_count)
    
    ax3.hist(visit_counts_per_place, bins=20, alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Visit Count')
    ax3.set_ylabel('Number of Places')
    ax3.set_title('Place Visit Count Distribution')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('examples/place_cells_visualization.png', dpi=150, bbox_inches='tight')
    print(f"그래프 저장: examples/place_cells_visualization.png")
    plt.show()
    
    print(f"\nPlace Cells 통계:")
    print(f"  총 Place 수: {len(unique_place_ids)}")
    print(f"  평균 방문 횟수: {np.mean(visit_counts_per_place):.1f}")
    print(f"  최대 방문 횟수: {np.max(visit_counts_per_place)}")


if __name__ == "__main__":
    visualize_place_cells()

