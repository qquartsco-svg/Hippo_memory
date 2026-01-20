## 🧠 Hippo Memory 최종 결과 및 수식 정리

**Date**: 2026-01-20  
**Version**: v0.4.0-alpha

---

## 1. 시스템 구조 개념 정리

### 1.1 PID, Hippo Memory, Cerebellum 역할 분리

- **PID Controller**
  - **역할**: 순간 오차 \(e(t)\)에 대한 **즉각적인 반응** (단기 안정화, 진동 제어)
  - **입력/출력**:
    \[
    e(t) = r(t) - y(t)
    \]
    \[
    u_{\text{PID}}(t) = K_p e(t) + K_i \int_0^t e(\tau)\,d\tau + K_d \frac{de(t)}{dt}
    \]

- **Hippo Memory (Hippocampus Layer)**
  - **역할**: 동일한 PID, 동일한 외란 조건에서  
    **장기적으로 반복되는 편향(bias)과 드리프트를 “장소별·맥락별”로 기억하고 서서히 보정**.
  - **출력**: 느린 기준선 보정 항 \(b_{\text{hip}}(x, c)\)
    - \(x\): 상태/위치(Place)  
    - \(c\): 맥락(Context)

- **Cerebellum (향후 레이어)**
  - **역할**: Hippo Memory가 제공한 상태별 편향 정보를 바탕으로  
    **수렴 속도와 진동 폭을 줄이는 빠른 Feedforward/Variance Reduction 레이어**.

---

## 2. Bias 보정 수식

### 2.1 제어 루프 구조

기본 제어 루프:
\[
e(t) = r(t) - y(t)
\]
\[
u_{\text{PID}}(t) = \text{PID}(e(t))
\]

Hippo Memory가 추가된 구조:
\[
e_{\text{hip}}(t) = r(t) - \bigl(y(t) + b_{\text{hip}}(x(t), c(t))\bigr)
\]
\[
u_{\text{PID}}(t) = \text{PID}(e_{\text{hip}}(t))
\]

- 여기서 \(b_{\text{hip}}(x, c)\)는 **느리게 변화하는 장기 편향 보정 항**이다.
- PID 게인은 그대로 두고, **측정값 쪽에서 장기 편향을 보정**하는 구조.

### 2.2 Place-wise Bias 업데이트

각 Place \(i\)에 대해 Hippo Memory는 bias를 지수 이동 평균(EMA) 형태로 갱신한다.

\[
b_i^{(k+1)} = \alpha\, b_{\text{new}}^{(k)} + (1-\alpha)\, b_i^{(k)}
\]

- \(b_i^{(k)}\): Place \(i\)에 저장된 \(k\)번째 업데이트 시점의 bias 추정값  
- \(b_{\text{new}}^{(k)}\): 해당 Place에서 새로 관측된 편향 (오차 기반)  
  - 보다 엄밀하게는, 해당 Place/Context에서의 **조건부 평균 오차**로 볼 수 있다:
    \[
    b_{\text{new}}^{(k)}
    \approx
    \mathbb{E}\bigl[e(t)\mid x(t)\in \text{Place } i,\; c(t)\bigr]
    \]
- \(\alpha \in (0, 1]\): 학습률 (Learning Rate)

Replay/Consolidation은 여러 에피소드/반복에서 모인 \(b_{\text{new}}\) 집합을 통계적으로 검증한 뒤,  
**안정 구간에서만 위 EMA를 적용**하도록 Learning Gate를 통해 제어한다.

또한 시간 스케일 관점에서,
\[
\tau_{\text{hip}} \gg \tau_{\text{PID}}
\]
가 되도록 설계되어 있다.  
즉, Hippo Memory는 **PID가 다루는 고주파/단기 동역학에는 개입하지 않고**,  
훨씬 더 긴 시간 축에서 **느리게 변하는 장기 편향만 보정**한다.

---

## 3. RMS 오차 및 Drift Slope 수식

### 3.1 RMS 오차 정의

에러 시퀀스 \(\{e_t\}_{t=1}^T\)에 대해 전체 RMS 오차:
\[
\text{RMS}_{1:T} = \sqrt{\frac{1}{T} \sum_{t=1}^{T} e_t^2}
\]

벤치마크 코드에서는 **Rolling Window RMS**를 사용:

\[
\text{RMS}_w(t) = \sqrt{\frac{1}{w} \sum_{\tau=t-w+1}^{t} e_\tau^2}
\quad (t \ge w)
\]

- \(w\): 윈도우 길이 (예: \(w = 50\))
- 이 값이 시간에 따라 **Hippo Memory 곡선이 더 아래로 분리**되는 것이  
  “경험을 통한 장기 최적화”의 시각적 증거이다.

### 3.2 Drift Slope (시간당 오차 변화율)

Rolling RMS 곡선 \(\text{RMS}_w(t)\)에 대해,

\[
\text{DriftSlope} = \frac{\text{RMS}_w(t_{\text{end}}) - \text{RMS}_w(t_{\text{start}})}{t_{\text{end}} - t_{\text{start}}}
\]

- Baseline:
  - \(\text{DriftSlope}_{\text{base}} \gtrsim 0\) (평행 또는 미세 우상향)  
  - → **시간이 지나도 제어기가 드리프트를 줄이지 못함**
- Hippo Memory:
  - \(\text{DriftSlope}_{\text{hip}} < 0\) 이면  
  - → **경험이 쌓일수록 평균 오차가 실제로 감소하고 있다는 증거**

이 값은 향후 제품/논문에서  
**“Memory-Based Long-Horizon Bias Compensation”**의 핵심 수치로 사용할 수 있다.

---

## 4. 벤치마크 수치 요약

`benchmark_drift_before_after.py` 기준 대표 결과:

```
[Baseline PID]
  Drift RMS: 0.781
  Final Error: 1.024

[PID + Hippo Memory]
  Drift RMS: 0.767  (↓ 1.8%)
  Final Error: 0.982 (↓ 4.1%)
```

### 4.1 개선율 정의

\[
\text{Improvement}_{\text{RMS}} = 
\frac{\text{RMS}_{\text{base}} - \text{RMS}_{\text{hip}}}{\text{RMS}_{\text{base}}} \times 100 \,\%
\]

\[
\text{Improvement}_{\text{Final}} = 
\frac{E_{\text{base}} - E_{\text{hip}}}{E_{\text{base}}} \times 100 \,\%
\]

- 여기서 \(\text{RMS}_{\text{base}}\), \(E_{\text{base}}\)는 Baseline(PID only) 기준  
- \(\text{RMS}_{\text{hip}}\), \(E_{\text{hip}}\)는 PID + Hippo Memory 기준
- 실제 출력에서는 **오차 감소**를 명확히 하기 위해  
  `↓ 1.8%`, `↓ 4.1%` 형태로 표기.

Hippo Memory의 **목표 함수**는 개별 시점에서 \(\lVert e(t)\rVert\)를 즉각 최소화하는 것이 아니라,  
충분히 긴 시간 스케일에서의 **기대 오차**를 줄이는 데 있다:
\[
\lim_{T\to\infty} \mathbb{E}[e(t)] \;\;\text{를 감소시키는 것에 초점을 둔 계층이다.}
\]

---

## 5. 해석: “허접함”에 대한 정답

- Hippo Memory는:
  - **즉각적인 진동 억제 레이어가 아니다.** (그 역할은 PID/소뇌)
  - **동일 PID, 동일 외란 조건에서 “장기 평균 오차와 Drift를 조금씩 깎아내는 기억 레이어”**이다.
- 상단 Error vs Time 그래프:
  - 피크 오차와 중심선이 **조금 더 아래로 깔린다** → Bias 보정
- 하단 RMS Convergence 그래프:
  - Baseline 대비 Hippo 곡선이 **시간이 갈수록 아래로 분리**  
  - → **“어제보다 더 나은 오늘”을 만드는 누적 효과**

요약하면:

> **Hippo Memory는 PID를 바꾸지 않고,  
> 그 위에서 “경험을 통해 기준선을 맞춰가는 장기 편향 보정 수식”이다.**

이 문서는 그 동작을 **수식과 지표로 공식화한 최종 결과 정리**이다.


