# 인간 메커니즘 16축 엔진

> 🇺🇸 [English README](./README.md)

**16개 축과 44개 메타원리를 갖춘 인간 행동 메커니즘 엔진 — 인지과학, 영향력 이론, 동기, 행동설계 기반의 진단·예측·설계입니다.**

## 사전 요구사항

- **Claude Cowork 또는 Claude Code** 환경

## 목적

모든 제품, 정책, 메시지, 상호작용은 인간 행동을 기반으로 성공하거나 실패합니다. human-skill은 6개의 과학적 소스(Kahneman, Cialdini, SDT, 진화심리학, 정서이론, 행동설계)에서 16개 축으로 행동을 매핑하며, 3가지 모드를 제공합니다: 진단(왜), 예측(다음은), 설계(무엇이 유발하는가).

## 사용 시점 및 방법

제품 채택, 메시지, 채용, 팀 역학, 정책 설득, UX 등 인간 행동을 최적화해야 할 때 사용합니다. 모드를 선택하세요 — 진단, 예측, 또는 설계. 스킬은 16개 행동 축에 걸쳐 매핑되며 44개 메타원리를 중심으로 구조화된 결과물을 제공합니다.

## 사용 예시

| 상황 | 프롬프트 | 결과 |
|---|---|---|
| 전환율이 3%에서 멈춤 | `"human-skill 설계: 사람들이 왜 무료에서 유료로 업그레이드하지 않을까?"` | 동기 축→장벽 대 유발 요인 파악→중재 설계 |
| 팀이 데드라인 미스 | `"human-skill 진단: 팀이 약속하고 미스한다. 뭐가 일어나는가?"` | 인지 편향 분석→정서 요인→근본 원인→해결책 |
| 정책 채택이 낮음 | `"human-skill 예측: 이 정책을 의무화하면 사람들은 어떻게 반응할까?"` | 16축 예측: 자율성 위협→반발 위험→중재 지점 |

## 핵심 기능

- 16축 프레임워크: Kahneman(7), Cialdini(3), SDT(2), 진화심리(2), 정서(1), 행동설계(1)
- 과학적 소스를 실제 행동과 연결하는 44개 메타원리
- 3가지 모드: 진단, 예측, 설계
- 6개 통합 과학적 소스
- 제품, 정책, 마케팅, 채용, 운영, 팀 역학 전반에 적용

## 연관 스킬

- **[hit-skill](https://github.com/jasonnamii/hit-skill)** — hit-skill의 3층 아키텍처는 human-skill 진단으로 구동됨
- **[biz-skill](https://github.com/jasonnamii/biz-skill)** — 전략이 human-skill 행동설계를 통합
- **[ui-action-designer](https://github.com/jasonnamii/ui-action-designer)** — 사용자 상호작용 설계에 human-skill 사용

## 설치

```bash
git clone https://github.com/jasonnamii/human-skill.git ~/.claude/skills/human-skill
```

## 업데이트

```bash
cd ~/.claude/skills/human-skill && git pull
```

`~/.claude/skills/`에 배치된 스킬은 Claude Code 및 Cowork 세션에서 자동으로 사용할 수 있습니다.

## Cowork 스킬 생태계

25개 이상의 커스텀 스킬 중 하나입니다. 전체 카탈로그: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## 라이선스

MIT 라이선스 — 자유롭게 사용, 수정, 공유하세요.