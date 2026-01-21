# Hippo Memory Package

**해마 메모리 패키지 - 완성된 해마 구조 독립 패키지**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.4.0--alpha-blue.svg)](https://github.com/qquartsco-svg/grid-engine)
[![Status](https://img.shields.io/badge/status-completed-green.svg)](https://github.com/qquartsco-svg/grid-engine)

**English**: [README_EN.md](README_EN.md)

---

## 🎯 무엇을 하는가

**Hippo Memory Package**는 Grid Engine에서 완성된 해마(Hippocampus) 구조를 독립적인 패키지로 정리한 것입니다. 

**해마 구조**는 생물학적 뇌 구조에서 공간 기억과 장기 기억을 담당하는 기관을 모방한 **공간 기반 기억 시스템**입니다.

**✅ 상태**: **완성 (v0.4.0-alpha)** - 모든 구성 요소가 구현 및 검증 완료되었습니다.

---

## 🎯 핵심 포지션: Hippo Memory의 역할

**⚠️ 중요**: Hippo Memory는 **PID 제어기를 대체하는 제어기가 아닙니다.**

**정확한 역할**:
- **PID**: 순간 오차에 대한 즉각 반응 (단기 안정화, 진동 제어)
- **Hippo Memory**: 동일한 PID, 동일한 외란 조건에서, **장기적으로 반복되는 편향(bias)과 드리프트를 '장소별·맥락별로 기억'하여 RMS 오차와 최종 편향을 서서히 줄여 나가는 기억 레이어**

**핵심 메시지**:
> Hippo Memory는 진동을 억제하는 레이어가 아니라,  
> **"평균값(기준선)을 천천히 맞춰가는 장기 편향 보정 레이어"**입니다.

---

## 📊 성능 개선 증거

**독립 벤치마크 결과** (Grid Engine 없이 Hippo Memory만으로 측정):

```
[Baseline PID]
  Drift RMS: 0.781
  Final Error: 1.024

[PID + Hippo Memory]
  Drift RMS: 0.767  (↓ 1.8%)
  Final Error: 0.982 (↓ 4.1%)
```

**해석**:
- 동일 PID, 동일 외란 조건에서 측정
- 제어기 튜닝 없이, 오직 '기억'만으로 장기 오차 감소
- → **"딕셔너리가 아닌 실제로 작동하는 학습 시스템"** 증명

자세한 수식 및 결과 해석:
- `docs/FINAL_RESULTS.md` – **공식 수식·지표 정의 및 벤치마크 수치 정리**
- `docs/WHY_HIPPO_MEMORY_WORKS.md` – **딕셔너리와의 차이, 구조적 동작 원리**
- 벤치마크 실행 코드는 `benchmarks/hippo_only/` 참조

---

## 📦 패키지 구성

### 핵심 모듈

```
hippo_memory_package/
├── hippocampus/              # 해마 메모리 모듈
│   ├── __init__.py
│   ├── place_cells.py       # Place Cells (장소별 기억)
│   ├── context_binder.py    # Context Binder (맥락별 기억 분리)
│   ├── learning_gate.py     # Learning Gate (학습 조건 제어)
│   ├── replay_consolidation.py  # Replay/Consolidation (기억 정제)
│   ├── replay_buffer.py     # Replay Buffer (안정 구간 추출)
│   ├── universal_memory.py  # Universal Memory (범용 인터페이스)
│   └── README.md            # 모듈 설명서
│
├── examples/                 # 예시 코드
│   ├── basic_usage.py       # 기본 사용 예시
│   └── universal_memory_demo.py  # 범용 메모리 데모
│
├── tests/                    # 테스트 코드
│   ├── test_place_cells.py  # Place Cells 테스트
│   └── test_universal_memory.py  # Universal Memory 테스트
│
├── benchmarks/               # 벤치마크 코드
│   ├── place_context_revisit_test.py  # Place/Context 재방문 테스트
│   └── context_split_test.py  # Context 분리 테스트
│
├── docs/                     # 문서
│   ├── HIPPOCAMPUS_COMPLETION.md
│   ├── HIPPOCAMPUS_UTILIZATION_GUIDE.md
│   ├── HIPPOCAMPUS_CEREBELLUM_INTEGRATION.md
│   └── HIPPOCAMPUS_FOLDER_INFO.md
│
├── README.md                 # 메인 README
├── QUICK_START.md            # 빠른 시작 가이드
├── PACKAGE_STRUCTURE.md      # 패키지 구조 문서
├── INSTALL.md                # 설치 가이드
├── SUMMARY.md                # 최종 요약
├── requirements.txt          # 의존성
├── setup.py                  # 설치 파일
└── LICENSE                   # MIT License
```

---

## 🧠 구성 요소

### 1. Place Cells (`place_cells.py`)
- **역할**: 장소별 독립적인 기억(bias) 저장
- **기능**: 위상 해싱을 통한 공간 분리, 장소별 독립적인 bias 저장
- **클래스**: `PlaceMemory`, `PlaceCellManager`

### 2. Context Binder (`context_binder.py`)
- **역할**: 맥락별 기억 분리
- **기능**: Place + Context 조합으로 기억 분리, 동일 장소에서도 맥락별 독립 기억
- **클래스**: `ContextMemory`, `ContextBinder`

### 3. Learning Gate (`learning_gate.py`)
- **역할**: 학습 조건 제어
- **기능**: 학습 조건 명시적 제어, 노이즈 학습 방지
- **클래스**: `LearningGateConfig`, `LearningGate`

### 4. Replay/Consolidation (`replay_consolidation.py`)
- **역할**: 기억 정제 및 장기 기억 고정
- **기능**: 휴지기에 기억 재검토, 통계적 유의성 검증을 통한 장기 기억 고정
- **클래스**: `PlaceMemoryWithHistory`, `ReplayConsolidation`, `ReplayConsolidationManager`

### 5. Replay Buffer (`replay_buffer.py`)
- **역할**: 안정 구간 추출을 위한 버퍼
- **기능**: Online phase에서 trajectory/error/state 기록, Replay phase에서 안정 구간 추출
- **클래스**: `TrajectoryPoint`, `ReplayBuffer`

### 6. Universal Memory (`universal_memory.py`)
- **역할**: 범용 기억 메모리 인터페이스
- **기능**: 어떤 시스템에도 붙일 수 있는 범용 인터페이스, RAG 스타일 API
- **클래스**: `UniversalMemory`

---

## 🚀 빠른 시작

### 설치

```bash
# 패키지 폴더로 이동
cd /Users/jazzin/Desktop/Hippo_memory/v3_Upgraded/hippo_memory_v3.0.0/release/hippo_memory_package

# Python 경로에 추가 (또는 pip install -e .)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 기본 사용법

```python
from hippocampus import UniversalMemory, create_universal_memory
import numpy as np

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

# 기억 검색
memories = memory.retrieve(state, context={"tool": "tool_A"})

# 기억 증강
augmented_context = memory.augment(state, context={"tool": "tool_A"})
```

---

## 📊 벤치마크 검증 결과

### ✅ 성공 사례

1. **장기 드리프트 억제**
   - Persistent Bias: **+51.3% 개선** (drift slope 감소)

2. **Place/Replay 재방문 효과**
   - Place(+Replay): **+5.9% 개선** (PID 대비)

---

## 🔗 통합

이 패키지는 독립적으로 사용할 수 있으며, Grid Engine이나 다른 시스템과 통합 가능합니다.

### Grid Engine 통합

```python
from grid_engine.hippocampus import UniversalMemory
from hippocampus import UniversalMemory as HippoMemory

# 둘 다 동일한 인터페이스 제공
```

### 쿠키 브레인 통합

```python
from hippocampus import UniversalMemory
from babyhippo.brain import PrefrontalCortex

# 해마 메모리를 쿠키 브레인에 연결
memory = UniversalMemory(memory_dim=5)
prefrontal = PrefrontalCortex()
# 통합 로직 구현
```

---

## 📚 문서

### 핵심 문서

- **해마 구조 완성**: [docs/HIPPOCAMPUS_COMPLETION.md](docs/HIPPOCAMPUS_COMPLETION.md)
- **해마 활용 가이드**: [docs/HIPPOCAMPUS_UTILIZATION_GUIDE.md](docs/HIPPOCAMPUS_UTILIZATION_GUIDE.md)
- **해마-소뇌 통합**: [docs/HIPPOCAMPUS_CEREBELLUM_INTEGRATION.md](docs/HIPPOCAMPUS_CEREBELLUM_INTEGRATION.md)
- **해마 폴더 정보**: [docs/HIPPOCAMPUS_FOLDER_INFO.md](docs/HIPPOCAMPUS_FOLDER_INFO.md)

### 모듈 문서

- **Place Cells**: [hippocampus/README.md](hippocampus/README.md)

---

## 🎯 활용 분야

### 1. 제어 시스템
- 위치별 편향 기억
- 맥락별 편향 분리
- 장기 드리프트 억제

### 2. LLM 애플리케이션
- 사용자 행동 패턴 기억
- 대화 맥락 기억
- 개인화 대화

### 3. 추천 시스템
- 사용자 선호도 기억
- 시간대별, 디바이스별 맥락 분리
- 개인화 추천

### 4. 게임 AI
- NPC 행동 패턴 기억
- 맵별, 시간대별 맥락 분리
- 자연스러운 NPC 행동

### 5. 에이전트 시스템
- 에이전트 상태/습관 기억
- 작업별, 환경별 맥락 분리
- 개성 있는 에이전트

---

## 📋 완성된 구성 요소 체크리스트

- [x] Place Cells (장소별 기억 저장)
- [x] Context Binder (맥락별 기억 분리)
- [x] Learning Gate (학습 조건 제어)
- [x] Replay/Consolidation (기억 정제)
- [x] Replay Buffer (안정 구간 추출)
- [x] Universal Memory (범용 인터페이스)
- [x] 문서화 (README, 문서들)
- [x] 벤치마크 검증

---

## 🔧 기술 스택

- **Python**: 3.8+
- **NumPy**: 수치 계산
- **타입 힌트**: 완전 지원
- **문서화**: 완전 지원

---

## 📝 라이선스

MIT License

---

## 👤 작성자

**GNJz (Qquarts)**

---

## 🌐 원본 저장소

이 패키지는 다음 저장소에서 추출되었습니다:
- **GitHub**: https://github.com/qquartsco-svg/grid-engine
- **해마 폴더**: https://github.com/qquartsco-svg/grid-engine/tree/main/grid_engine/hippocampus

---

**마지막 업데이트**: 2026-01-20

---

## 🧠 Memory Layers (Concept Alignment)

This project uses the same **memory-layer taxonomy** as the Brain Atlas:

- **L0** Ring Attractor → **Neural Intrinsic Memory** (local attractor dynamics)
- **L1** Grid Engine → **Spatial State Representation**
- **L2** Hippo Memory → **Contextual / Place Memory**
- **L3** Cerebellum → **Motor Pattern Optimizer**

See: `~/Desktop/Brain_Atlas/CONCEPTS_MEMORY_LAYERS.md`
