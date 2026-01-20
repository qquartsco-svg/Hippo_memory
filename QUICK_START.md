# Hippo Memory Package - 빠른 시작 가이드

**Date**: 2026-01-20  
**Version**: v0.4.0-alpha

---

## 🚀 5분 안에 시작하기

### 1단계: 설치

```bash
cd /Users/jazzin/Desktop/Hippo_memory/v3_Upgraded/hippo_memory_v3.0.0/release/hippo_memory_package
pip install -e .
```

또는 Python 경로 추가:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

### 2단계: 기본 사용

```python
from hippocampus import create_universal_memory
import numpy as np

# 메모리 생성
memory = create_universal_memory(memory_dim=5)

# 기억 저장
memory.store(
    key=np.array([1.0, 0.5, 0.3, 10.0, 5.0]),
    value=np.array([0.001, 0.002, 0.0, 0.0, 0.0]),
    context={"tool": "tool_A", "temperature": 25.0}
)

# 기억 검색
memories = memory.retrieve(
    query=np.array([1.0, 0.5, 0.3, 10.0, 5.0]),
    context={"tool": "tool_A"}
)

print(f"검색된 기억: {len(memories)}개")
```

---

### 3단계: 예시 실행

```bash
# 기본 사용 예시
python3 examples/basic_usage.py

# 범용 메모리 데모
python3 examples/universal_memory_demo.py
```

---

### 4단계: 테스트 실행

```bash
# Place Cells 테스트
python3 -m pytest tests/test_place_cells.py

# Universal Memory 테스트
python3 -m pytest tests/test_universal_memory.py
```

---

## 📚 더 알아보기

- **README.md**: 전체 문서
- **examples/**: 사용 예시
- **tests/**: 테스트 코드
- **docs/**: 상세 문서

---

**Author**: GNJz  
**Made in**: GNJz  
**License**: MIT License

