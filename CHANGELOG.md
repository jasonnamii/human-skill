# Changelog — human-skill

All notable changes to this skill are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loose style.
Versioning: SemVer (MAJOR.MINOR.PATCH).

---

## [1.0.0] — 2026-04-17

### Baseline
- 16축(인지7·동기2·사회3·진화2·감정1·행동1) × 44메타원리 프레임 확립
- 3모드(진단·예측·설계) 자동 판별
- Python 라우터(`meta_router.py`, `axes_data.py`)로 토큰 효율 로딩
- 12개 references/ 스포크 분리 (허브스포크 아키텍처)
- §4.5 리포트 변환(3블록·서사) 규정
- §7 출력 QC 체크리스트 5항목

### Added (2026-04-17 prescription 반영)
- **frontmatter `version` 필드** — SemVer 버전 관리 시작 (1.0.0 baseline)
- **description 트리거 확장** — P3(영어)·P4(시점)·P5(포맷)·NOT(라우팅) 티어 신설
  - P1: +2 (심리분석, 행동예측)
  - P2: +4 (분석해줘, diagnose behavior, predict, design trigger)
  - P3: 신설 5개 (behavioral analysis, human mechanism, psychological mechanism, cognitive bias, motivation design)
  - P4: 신설 4개 (사용자/고객/넛지/조직원 시점)
  - P5: 신설 4개 (진단서로, 리포트로, .md로, 시나리오로)
  - NOT: 신설 5건 (→hit-skill, →copywriting-engine, →biz-skill, →management-skill, →ux-advisor)
- **`## NOT — 경계 라우팅` 섹션** — SKILL.md 말미 6건 라우팅 표
- **`evals/` 디렉터리** — 회귀 테스트 자산
  - `cases.json`: 3개 기준 케이스 (진단·예측·설계 각 1개)
  - `expected-outputs.md`: 케이스별 합격 기준·불합격 사유·채점표
  - `run-eval.sh`: 수동 실행 가이드
- **`scripts/validate.py`** — self-check 엔진
  - frontmatter 존재·version 필드 검증
  - @uses 파일 실존 확인
  - 16축 이름 일관성 (SKILL.md ↔ axes_data.py)
  - 44메타원리 번호 언급 스캔
  - 허브 축(H·I·E) 명시 확인
  - 필수 섹션 존재 확인
  - 트리거 티어 6종 완비 확인

### Diagnosis Trail
- 2026-04-17 skill-doctor 진단: 🟠 63.3/100 (ORANGE)
- Red flags: ②-2 미발동, ⑦-3 테스트부재, ⑧-1 자기진단불가
- 처방 반영 후 예상 점수: 🟢 83 (GREEN)

---

## Unreleased

### Deferred (P2 — 이번 릴리즈 제외)
- ①-2: 동시 로드 힌트 — Python 라우터가 이미 선택적 로드 수행
- ③-2·4: 예시·이름 개선 — 기능 안정 후 UX 최적화 단계
- ④-2·4: PREFLIGHT·상태 재검증 — evals 누적 후 결함 노출 시 착수
- ⑤-1: SKILL.md 크기 — 7929B (5KB 목표 경미 초과, 허브스포크 양호)
- ⑧-3·4: 피드백·학습 축적 — UP §H·session-briefing이 커버

---

## 원칙

- **SemVer 엄격 적용**: 프레임(16축·44메타) 변경 = MAJOR. 모드·섹션 추가 = MINOR. 트리거·QC 보강 = PATCH.
- **회귀 테스트 필수**: 모든 릴리즈는 evals/ 3케이스 통과 후 배포.
- **CHANGELOG 없이 릴리즈 금지**: skill-builder가 차단.
