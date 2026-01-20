# Hippo Memory Package - 사용 사례 (Use Cases)

**Date**: 2026-01-20  
**Version**: v0.4.0-alpha

---

## 🎯 무엇에 사용할 수 있는가?

**Hippo Memory Package**는 **공간 기반 기억 시스템**으로, 다음과 같은 용도로 사용할 수 있습니다:

---

## 1️⃣ 제어 시스템 (Control Systems)

### 용도
- **CNC 머신**: 위치별 편향(bias) 학습 및 보정
- **로봇 팔**: 관절 위치별 기억 및 반복 정밀도 향상
- **3D 프린터**: 레이어별 온도/속도 편향 학습
- **드론**: 위치별 바람/자기장 편향 보정

### 예시
```python
from hippocampus import create_universal_memory
import numpy as np

# 제어 시스템 메모리 생성
memory = create_universal_memory(memory_dim=5)  # X, Y, Z, A, B

# 특정 위치에서의 편향 저장
position = np.array([100.0, 50.0, 10.0, 0.0, 0.0])  # mm, deg
bias = np.array([0.01, 0.02, 0.0, 0.0, 0.0])  # 열 변형으로 인한 편향

memory.store(
    key=position,
    value=bias,
    context={"tool": "tool_A", "temperature": 25.0, "material": "aluminum"}
)

# 제어 시 편향 검색 및 보정
memories = memory.retrieve(position, context={"tool": "tool_A"})
correction = -memories[0]['bias']  # 보정값
```

### 효과
- ✅ 반복 가공 정밀도 향상
- ✅ 장기 드리프트 억제
- ✅ 위치별 편향 자동 학습

---

## 2️⃣ LLM 통합 (LLM Integration)

### 용도
- **대화형 AI**: 사용자별 행동 패턴 기억
- **맥락 인식**: 대화 상태별 기억 저장
- **개인화**: 사용자별 선호도 학습

### 예시
```python
from hippocampus import create_universal_memory
import numpy as np

# LLM 메모리 생성
memory = create_universal_memory(memory_dim=5)

# 사용자 행동 패턴 저장
conversation_state = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
user_behavior = np.array([0.01, 0.02, 0.0, 0.0, 0.0])  # 사용자가 항상 조금 느리게 반응

memory.store(
    key=conversation_state,
    value=user_behavior,
    context={"user": "user_123", "session": "session_1", "time": "morning"}
)

# LLM 쿼리 시 기억 검색
augmented_context = memory.augment(conversation_state, context={"user": "user_123"})
# → LLM이 사용자 특성을 고려한 응답 생성
```

### 효과
- ✅ 사용자별 맞춤 응답
- ✅ 대화 맥락 유지
- ✅ 장기 기억 형성

---

## 3️⃣ 추천 시스템 (Recommendation Systems)

### 용도
- **콘텐츠 추천**: 사용자 상태별 선호도 학습
- **상품 추천**: 구매 패턴 기억
- **개인화**: 사용자별 행동 패턴 저장

### 예시
```python
from hippocampus import create_universal_memory
import numpy as np

# 추천 시스템 메모리 생성
memory = create_universal_memory(memory_dim=5)

# 사용자 상태별 선호도 저장
user_state = np.array([0.5, 0.3, 0.2, 0.1, 0.0])
user_preference = np.array([0.1, 0.2, 0.0, 0.0, 0.0])

memory.store(
    key=user_state,
    value=user_preference,
    context={"user": "user_456", "time": "evening", "device": "mobile"}
)

# 추천 시 기억 검색
augmented_context = memory.augment(user_state, context={"user": "user_456"})
# → 사용자 상태에 맞는 콘텐츠 추천
```

### 효과
- ✅ 사용자별 맞춤 추천
- ✅ 시간대별 선호도 학습
- ✅ 장기 선호도 유지

---

## 4️⃣ 게임 AI (Game AI)

### 용도
- **NPC 행동**: 위치별 행동 패턴 기억
- **맵 기억**: 특정 위치에서의 이벤트 기억
- **적 AI**: 플레이어 위치별 대응 패턴 학습

### 예시
```python
from hippocampus import create_universal_memory
import numpy as np

# 게임 AI 메모리 생성
memory = create_universal_memory(memory_dim=5)

# NPC 위치별 행동 패턴 저장
npc_position = np.array([10.0, 5.0, 2.0, 0.0, 0.0])
npc_behavior = np.array([0.05, 0.0, 0.0, 0.0, 0.0])  # 이 위치에서 항상 조금 이렇게 행동

memory.store(
    key=npc_position,
    value=npc_behavior,
    context={"npc": "npc_001", "map": "forest", "time": "day"}
)

# 게임 시 기억 검색
memories = memory.retrieve(npc_position, context={"npc": "npc_001"})
behavior_correction = memories[0]['bias']
# → NPC가 이 위치에서 미묘하게 다른 행동을 보임
```

### 효과
- ✅ 위치별 행동 패턴 학습
- ✅ 맵별 기억 분리
- ✅ 자연스러운 NPC 행동

---

## 5️⃣ 센서 데이터 처리 (Sensor Data Processing)

### 용도
- **IoT 센서**: 위치별 센서 편향 보정
- **환경 모니터링**: 시간/위치별 데이터 패턴 학습
- **노이즈 필터링**: 안정 구간만 기억 저장

### 예시
```python
from hippocampus import create_universal_memory
import numpy as np

# 센서 메모리 생성
memory = create_universal_memory(memory_dim=5)

# 위치별 센서 편향 저장
sensor_position = np.array([1.0, 2.0, 3.0, 0.0, 0.0])
sensor_bias = np.array([0.001, 0.002, 0.0, 0.0, 0.0])  # 센서 고유 편향

memory.store(
    key=sensor_position,
    value=sensor_bias,
    context={"sensor": "sensor_001", "temperature": 25.0, "humidity": 50.0}
)

# 센서 데이터 보정
memories = memory.retrieve(sensor_position, context={"sensor": "sensor_001"})
corrected_value = raw_value - memories[0]['bias']
```

### 효과
- ✅ 센서 편향 자동 보정
- ✅ 환경별 편향 분리
- ✅ 장기 안정성 향상

---

## 6️⃣ 로봇 학습 (Robot Learning)

### 용도
- **강화 학습**: 상태별 행동 가치 기억
- **모방 학습**: 위치별 행동 패턴 학습
- **적응 제어**: 환경별 제어 파라미터 학습

### 예시
```python
from hippocampus import create_universal_memory
import numpy as np

# 로봇 학습 메모리 생성
memory = create_universal_memory(memory_dim=5)

# 상태별 행동 가치 저장
robot_state = np.array([1.0, 0.5, 0.3, 10.0, 5.0])
action_value = np.array([0.1, 0.2, 0.0, 0.0, 0.0])  # 이 상태에서의 행동 가치

memory.store(
    key=robot_state,
    value=action_value,
    context={"task": "pick_and_place", "object": "cup", "environment": "kitchen"}
)

# 행동 선택 시 기억 검색
memories = memory.retrieve(robot_state, context={"task": "pick_and_place"})
best_action_value = memories[0]['bias']
# → 이전 경험을 바탕으로 최적 행동 선택
```

### 효과
- ✅ 경험 기반 학습
- ✅ 환경별 행동 분리
- ✅ 장기 기억 형성

---

## 📊 테스트 파일 설명

### 1. `tests/test_place_cells.py`
**목적**: Place Cells 모듈의 기본 기능 검증

**테스트 내용**:
- Place ID 할당 테스트
- Place Memory 저장 테스트
- Place Blending 테스트

**실행 방법**:
```bash
python3 -m pytest tests/test_place_cells.py -v
```

### 2. `tests/test_universal_memory.py`
**목적**: Universal Memory 인터페이스 검증

**테스트 내용**:
- 저장 및 검색 테스트
- 증강(Augment) 테스트
- Replay 테스트

**실행 방법**:
```bash
python3 -m pytest tests/test_universal_memory.py -v
```

---

## 🚀 빠른 시작

### 1. 설치
```bash
cd /Users/jazzin/Desktop/Hippo_memory/v3_Upgraded/hippo_memory_v3.0.0/release/hippo_memory_package
pip install -e .
```

### 2. 기본 사용
```python
from hippocampus import create_universal_memory
import numpy as np

memory = create_universal_memory(memory_dim=5)
memory.store(key=state, value=bias, context={"tool": "tool_A"})
memories = memory.retrieve(query=state, context={"tool": "tool_A"})
```

### 3. 예시 실행
```bash
python3 examples/basic_usage.py
python3 examples/universal_memory_demo.py
```

### 4. 테스트 실행
```bash
python3 -m pytest tests/ -v
```

---

## 💡 핵심 특징

### ✅ 공간 기반 기억
- 위치별 독립적인 기억 저장
- 맥락별 기억 분리
- 장기 기억 형성

### ✅ 범용 인터페이스
- 어떤 시스템에도 붙일 수 있음
- RAG 스타일 API
- 최소 의존성 (NumPy만 필요)

### ✅ 검증 완료
- 단위 테스트
- 벤치마크
- 실제 사용 예시

---

## 📝 결론

**Hippo Memory Package**는 다음과 같은 용도로 사용할 수 있습니다:

1. **제어 시스템**: 위치별 편향 학습 및 보정
2. **LLM 통합**: 사용자별 행동 패턴 기억
3. **추천 시스템**: 사용자 상태별 선호도 학습
4. **게임 AI**: 위치별 행동 패턴 기억
5. **센서 데이터 처리**: 위치별 센서 편향 보정
6. **로봇 학습**: 상태별 행동 가치 기억

**모든 용도에서 공통적으로 필요한 것**:
- 공간/상태별 기억 저장
- 맥락별 기억 분리
- 장기 기억 형성

---

**Author**: GNJz  
**Made in**: GNJz  
**License**: MIT License

