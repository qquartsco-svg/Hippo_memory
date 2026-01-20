# Hippo Memory Package 설치 가이드

**Date**: 2026-01-20  
**Version**: v0.4.0-alpha

---

## 📦 설치 방법

### 방법 1: 개발 모드 설치 (권장)

```bash
cd /Users/jazzin/Desktop/Hippo_memory/v3_Upgraded/hippo_memory_v3.0.0/release/hippo_memory_package
pip install -e .
```

### 방법 2: Python 경로 추가

```bash
export PYTHONPATH="${PYTHONPATH}:/Users/jazzin/Desktop/Hippo_memory/v3_Upgraded/hippo_memory_v3.0.0/release/hippo_memory_package"
```

### 방법 3: 직접 import (개발용)

```python
import sys
sys.path.insert(0, '/Users/jazzin/Desktop/Hippo_memory/v3_Upgraded/hippo_memory_v3.0.0/release/hippo_memory_package')

from hippocampus import UniversalMemory
```

---

## ✅ 설치 확인

```bash
python3 -c "from hippocampus import UniversalMemory; print('✅ 설치 완료')"
```

---

## 📝 의존성

- Python 3.8+
- NumPy >= 1.20.0

---

**Author**: GNJz  
**Made in**: GNJz  
**License**: MIT License
