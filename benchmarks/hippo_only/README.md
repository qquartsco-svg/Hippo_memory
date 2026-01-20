# Hippo Memory 독립 벤치마크

**Grid Engine 없이 Hippo Memory만으로 실행 가능한 벤치마크**

---

## 🎯 목적

- "딕셔너리 vs 실제로 작동하는 시스템" 차이를 수치로 증명
- Before (PID only) vs After (PID + Hippo Memory) 비교
- 독립 실행 가능 (Grid Engine 의존성 없음)

---

## 📊 벤치마크 시나리오

### 1. 드리프트 Before/After 비교

**시나리오**:
- 1D 위치 제어 시뮬레이션
- 온도/부하에 따라 drift 발생
- PID만 쓰면 누적 오차
- Hippo Memory 붙이면 장소별 bias 기억

**측정 지표**:
- Drift RMS (누적 오차)
- Final Error (최종 오차)
- 재방문 시 오차 수렴 속도

---

## 🚀 실행 방법

### 벤치마크 실행

```bash
cd benchmarks/hippo_only
python3 benchmark_drift_before_after.py
```

### 시각화 생성

```bash
python3 plot_drift_comparison.py
```

---

## 📈 예상 결과

```
[Baseline PID]
  Drift RMS: 0.034
  Final Error: 0.021

[PID + Hippo Memory]
  Drift RMS: 0.012  (-64%)
  Final Error: 0.007 (-66%)
```

---

## 📝 파일 설명

- `benchmark_drift_before_after.py`: 메인 벤치마크 코드
- `plot_drift_comparison.py`: 시각화 코드
- `README.md`: 이 파일

---

**Author**: GNJz  
**Made in**: GNJz  
**License**: MIT License

