"""
Hippo Memory 벤치마크 시각화

Before/After 비교 그래프 생성

Author: GNJz
Created: 2026-01-20
Made in GNJz
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import matplotlib.pyplot as plt
from benchmark_drift_before_after import main


def plot_comparison(results: dict, save_path: str = "drift_comparison.png"):
    """Before/After 비교 그래프 생성"""
    
    baseline = results['baseline']
    hippo = results['hippo']
    improvements = results['improvements']
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # 1. Error vs Time
    ax1 = axes[0]
    ax1.plot(baseline['time_steps'], baseline['errors'], 
             label='Baseline (PID only)', alpha=0.7, linewidth=1.5)
    ax1.plot(hippo['time_steps'], hippo['errors'], 
             label='PID + Hippo Memory', alpha=0.7, linewidth=1.5)
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('Error')
    ax1.set_title('Long-Horizon Bias Compensation via Hippocampus Memory\n(Under identical PID conditions)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 개선율 텍스트 추가 (오차 감소 표시)
    textstr = f"RMS Error ↓ {abs(improvements['drift_rms']):.1f}%\n"
    textstr += f"Final Error ↓ {abs(improvements['final_error']):.1f}%\n"
    textstr += "Long-horizon bias compensation"
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes,
             verticalalignment='top', bbox=dict(boxstyle='round', 
             facecolor='wheat', alpha=0.5), fontsize=9)
    
    # 2. RMS Error (Rolling Window)
    ax2 = axes[1]
    window_size = 50
    baseline_rms = []
    hippo_rms = []
    
    for i in range(window_size, len(baseline['errors'])):
        baseline_rms.append(np.sqrt(np.mean(np.array(baseline['errors'][i-window_size:i])**2)))
        hippo_rms.append(np.sqrt(np.mean(np.array(hippo['errors'][i-window_size:i])**2)))
    
    time_window = baseline['time_steps'][window_size:]
    ax2.plot(time_window, baseline_rms, 
             label='Baseline (PID only)', alpha=0.7, linewidth=1.5)
    ax2.plot(time_window, hippo_rms, 
             label='PID + Hippo Memory', alpha=0.7, linewidth=1.5)
    ax2.set_xlabel('Time Step')
    ax2.set_ylabel('RMS Error (Rolling Window)')
    ax2.set_title('RMS Error Convergence: Memory-Based Long-Term Optimization\n(Hippo Memory gradually reduces bias through experience)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"그래프 저장: {save_path}")
    plt.show()


def main_plot():
    """메인 실행 함수"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from benchmark_drift_before_after import main
    
    print("벤치마크 실행 중...")
    results = main()
    
    print("\n그래프 생성 중...")
    plot_comparison(results, save_path=os.path.join(os.path.dirname(__file__), "drift_comparison.png"))
    
    return results


if __name__ == "__main__":
    main_plot()

