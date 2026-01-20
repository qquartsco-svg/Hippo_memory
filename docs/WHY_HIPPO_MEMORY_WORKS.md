# 왜 Hippo Memory가 작동하는가?

**Date**: 2026-01-20  
**Version**: v0.4.0-alpha

---

## 🎯 핵심 질문

**"그냥 딕셔너리 아니냐?"**

**답: 아니요. Hippo Memory는 "기억이 형성되는 시스템"입니다.**

---

## ⚠️ 중요한 포지션 정의

**Hippo Memory는 PID 제어기를 대체하는 제어기가 아닙니다.**

**정확한 역할**:
- **PID**: 순간 오차에 대한 즉각 반응 (단기 안정화, 진동 제어)
- **Hippo Memory**: 동일한 PID, 동일한 외란 조건에서, **장기적으로 반복되는 편향(bias)과 드리프트를 '장소별·맥락별로 기억'하여 RMS 오차와 최종 편향을 서서히 줄여 나가는 기억 레이어**

**핵심 메시지**:
> Hippo Memory는 진동을 억제하는 레이어가 아니라,  
> **"평균값(기준선)을 천천히 맞춰가는 장기 편향 보정 레이어"**입니다.

---

## 🔍 딕셔너리 vs Hippo Memory

### 딕셔너리 (Dictionary)

```python
memory = {}
memory[key] = value  # 저장
value = memory.get(key)  # 검색
```

**특징**:
- ❌ 저장만 함
- ❌ 학습 안 함
- ❌ 시간이 지나도 변하지 않음
- ❌ 맥락 구분 안 함

### Hippo Memory

```python
memory = create_universal_memory(memory_dim=5)
memory.store(key=state, value=bias, context={"tool": "A"})
memories = memory.retrieve(query=state, context={"tool": "A"})
```

**특징**:
- ✅ 저장 + 학습
- ✅ 시간이 지날수록 더 정확해짐 (Replay/Consolidation)
- ✅ 맥락별 기억 분리 (Context Binder)
- ✅ 위치별 독립 기억 (Place Cells)
- ✅ 안정 구간만 학습 (Learning Gate)

---

## 💡 작동 원리

### 1. Place Cells: 위치별 독립 기억

**문제**: 동일 위치를 재방문할 때마다 편향이 누적됨

**해결**: 각 위치마다 독립적인 편향 기억

```python
# 위치 A 방문
memory.store(key=position_A, value=bias_A, context={})

# 위치 B 방문
memory.store(key=position_B, value=bias_B, context={})

# 다시 위치 A 재방문 → 이전에 학습한 bias_A 자동 적용
memories = memory.retrieve(query=position_A, context={})
correction = -memories[0]['bias']  # bias_A 자동 적용
```

**효과**: 재방문 시 편향 자동 보정

---

### 2. Context Binder: 맥락별 기억 분리

**문제**: 동일 위치에서도 공구/온도가 다르면 편향이 다름

**해결**: 맥락별로 독립적인 기억 저장

```python
# 위치 A, 공구 A, 온도 25도
memory.store(key=position_A, value=bias_A1, context={"tool": "A", "temp": 25})

# 위치 A, 공구 B, 온도 30도
memory.store(key=position_A, value=bias_A2, context={"tool": "B", "temp": 30})

# 검색 시 맥락별로 다른 기억 반환
memories_A1 = memory.retrieve(query=position_A, context={"tool": "A", "temp": 25})
memories_A2 = memory.retrieve(query=position_A, context={"tool": "B", "temp": 30})
```

**효과**: 맥락별로 정확한 편향 보정

---

### 3. Replay/Consolidation: 시간이 지날수록 더 정확해짐

**문제**: 초기 학습 데이터에 노이즈가 섞여 있음

**해결**: 휴지기에 안정 구간만 재생하여 정제

```python
# Online phase: 데이터 기록만
for step in trajectory:
    if is_stable(step):
        memory.store(key=state, value=bias, context={})

# Replay phase: 안정 구간만 재생하여 학습
memory.replay(current_time=idle_time)
# → 노이즈 필터링, 진짜 편향만 장기 기억으로 고정
```

**효과**: 시간이 지날수록 더 정확한 기억

---

### 4. Learning Gate: 안정 구간만 학습

**문제**: 움직이는 중에는 노이즈가 많음

**해결**: 안정 구간에서만 학습

```python
# Learning Gate 조건
if velocity < threshold and acceleration < threshold:
    # 안정 구간 → 학습 허용
    memory.store(key=state, value=bias, context={})
else:
    # 움직이는 중 → 학습 금지
    pass
```

**효과**: 노이즈 없는 깨끗한 기억만 저장

---

## 📊 실제 성능 개선

### 벤치마크 결과

```
[Baseline PID]
  Drift RMS: 0.034
  Final Error: 0.021

[PID + Hippo Memory]
  Drift RMS: 0.012  (-64%)
  Final Error: 0.007 (-66%)
```

### 왜 개선되는가?

1. **재방문 시 편향 자동 보정** (Place Cells)
2. **맥락별 정확한 편향** (Context Binder)
3. **시간이 지날수록 더 정확** (Replay/Consolidation)
4. **노이즈 없는 깨끗한 기억** (Learning Gate)

---

## 🎯 결론

**Hippo Memory는 "딕셔너리"가 아니라 "기억이 형성되는 시스템"입니다.**

**차이점**:
- 딕셔너리: 저장만 함
- Hippo Memory: 저장 + 학습 + 정제 + 분리

**효과**:
- 재방문 시 편향 자동 보정
- 맥락별 정확한 편향
- 시간이 지날수록 더 정확
- 노이즈 없는 깨끗한 기억

---

**Author**: GNJz  
**Made in**: GNJz  
**License**: MIT License

