---
name: human-skill
description: |
  인간행동·의사결정·심리 동인을 16축으로 분석하는 행동 진단 스킬. 트리거: 인간분석, 행동분석, 심리분석, 의사결정, 동기분석, 분석해줘, 진단해줘, 왜 그런지 봐줘, analyze behavior. NOT: 인물 프로필(→profiler-skill), 카피(→copywriting-skill), 시장조사(→research-skill).
---

# Human Skill

인간분석, 행동분석, 심리분석, 의사결정, 동기분석 요청이 오면 사람·고객·조직의 행동을 원인과 조건으로 나누어 본다. 결론은 성격 단정이 아니라 관찰 가능한 행동 가설이어야 한다.


## Skill Boundaries

- **하는 것** — "인간행동·의사결정·심리 동인을 16축으로 분석하는 행동 진단 스킬.
- **안 하는 것** — 인물 프로필(→profiler-skill), 카피(→copywriting-skill), 시장조사(→research-skill)."

## When to Use

- 사용자가 "분석해줘", "진단해줘", "왜 그런지 봐줘", "analyze behavior." 같은 표현으로 발동
- 사람·고객·조직 행동의 원인을 판단할 때.
- **안 쓸 때** — 인물 프로필(→profiler-skill), 카피(→copywriting-skill), 시장조사(→research-skill)."


## Prerequisites

| # | 체크 | 미충족 시 |
|---|------|-----------|
| 1 | 대상·입력 명확 (스킬 발동 의도 확인) | 1줄 확인 후 진입 |
| 2 | references/ 폴더 접근 가능 | inline fallback |
| 3 | scripts/ 실행 권한 | 권한 보정 후 재시도 |


## 절대 규칙

1. 개인 비난이나 성격 낙인으로 쓰지 않는다.
2. 관찰된 행동, 해석, 처방을 분리한다.
3. 근거가 약하면 `가능성`으로만 말한다.
4. 행동 변화 처방은 환경, 보상, 마찰, 타이밍으로 나눠 제시한다.

## 모드 자동 판별

| 입력 | 모드 | 산출 |
|---|---|---|
| 왜 이런 행동을 하나 | 진단 | 원인 가설 Top3 |
| 어떻게 설득하나 | 설계 | 메시지·환경·순서 |
| 조직이 왜 안 움직이나 | 조직 | 병목과 개입점 |

## 스크리닝

먼저 네 가지를 짧게 확인한다.

1. 관찰된 행동은 무엇인가.
2. 행동이 반복되는 상황은 언제인가.
3. 당사자가 얻는 이익이나 피하는 손실은 무엇인가.
4. 바꾸려는 행동의 기준은 무엇인가.

## 메타원리 라우팅

- 축H 허브: 행동을 움직이는 보상, 마찰, 사회적 신호를 먼저 본다.
- 축I: 정보 부족인지, 동기 부족인지, 신뢰 부족인지 구분한다.
- 축E: 개인 문제처럼 보여도 환경 설계 문제인지 확인한다.
- M1, M5, CM7, SM6, BM3, BM4, EmoM5는 반복 행동과 설득 실패를 볼 때 우선 참고한다.

## 16축 개요

축1 동기, 축2 보상, 축3 손실회피, 축4 습관, 축5 정체성, 축6 사회적 압력, 축7 신뢰, 축8 정보비대칭, 축9 인지부하, 축A 감정상태, 축B 시간압박, 축C 권력관계, 축D 관계자 이해, 축E 환경설계, 축F 실행마찰, 축G 변화저항, 축H 허브, 축I 판단게이트를 필요 범위에서만 사용한다.

## 리포트 변환

기본 출력은 짧게 유지한다.

| 구분 | 내용 |
|---|---|
| 관찰 | 실제 행동 |
| 해석 | 가능한 원인 |
| 개입 | 바꿀 수 있는 조건 |
| 맹점 | 놓치기 쉬운 반대 가능성 |

## NOT

인물 전체 프로필은 profiler-skill, 광고 카피는 copywriting-skill, 원자료 조사는 research-skill로 넘긴다.

## Output Path

| 산출물 | 경로 |
|---|---|
| 주 산출물 | `mnt/outputs/human-skill_{topic}_{YYYY-MM-DD}.md` |
| 형식 | 리포트로, 진단서로, .md로. |
| 리서치 결과 (해당 시) | `{VAULT}/_skills research/human-skill/{YYYY-MM-DD}_{topic}.md` |

## Reference Index

| 파일 | 내용 | 언제 |
|---|---|---|
| `references/axes-behavior.md` | axes behavior | 해당 단계 진입 시 |
| `references/axes-cognitive.md` | axes cognitive | 해당 단계 진입 시 |
| `references/axes-emotion.md` | axes emotion | 해당 단계 진입 시 |
| `references/axes-evolution.md` | axes evolution | 해당 단계 진입 시 |
| `references/axes-motivation.md` | axes motivation | 해당 단계 진입 시 |
| `references/axes-social.md` | axes social | 해당 단계 진입 시 |
| `references/low-usage-meta-guide.md` | low usage meta guide | 해당 단계 진입 시 |
| `references/meta-principles.md` | meta principles | 해당 단계 진입 시 |
| `references/mode-guide.md` | mode guide | 해당 단계 진입 시 |
| `references/output-qc.md` | output qc | 해당 단계 진입 시 |
| `references/report-template.md` | report template | 해당 단계 진입 시 |
| `references/screening-table.md` | screening table | 해당 단계 진입 시 |


## Next Phase

본 스킬 작업 후 자연스럽게 이어지는 흐름:

- 후속 작업 → `profiler-skill`
- 후속 작업 → `copywriting-skill`
- 후속 작업 → `research-skill`

## Failure Modes (Gotchas)

| 함정 | 대응 |
|---|---|
| 성격으로 단정 | 행동 조건으로 번역 |
| 한 가지 원인으로 몰기 | 원인 Top3와 반증 조건 제시 |
| 설득문만 고치기 | 환경·보상·마찰까지 함께 점검 |
| ❌ 사람 자체가 문제라고 결론 | ✅ 행동을 만든 조건과 유인을 먼저 본다 |
