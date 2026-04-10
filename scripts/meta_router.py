#!/usr/bin/env python3
"""
메타원리 라우팅 매트릭스 — 활성 축 입력 → 관련 메타원리 즉시 반환.

사용법:
  python meta_router.py 축1 축5 축H        # 활성 축 → 메타원리 라우팅
  python meta_router.py --detail 축1 축5    # 상세 모드: 자명명제+체인+설계원칙 포함
  python meta_router.py --axis 축1          # 특정 축 풀 상세 (체인 전문)
  python meta_router.py --axis 축E --table  # 축 상세 + 특수 테이블 포함
  python meta_router.py --mode 진단         # 모드별 실행 프로토콜
  python meta_router.py --all               # 전체 매트릭스 출력
  python meta_router.py --loops             # 자기강화 루프만 출력
  python meta_router.py --hubs              # 허브 축 연결 요약
"""

import sys
import json
from typing import NamedTuple

# ──────────────────────────────────────────────
# 데이터 정의
# ──────────────────────────────────────────────

class MetaPrinciple(NamedTuple):
    id: str           # M1, CM3, SM6 등
    series: str       # 카너먼/치알디니/SDT/진화심리/감정이론/행동설계
    axes: tuple       # (from_axis, to_axis) — 방향 있음
    direction: str    # → 단방향 / ↔ 쌍방향
    mechanism: str    # 1줄 메커니즘
    design_impl: str  # 1줄 설계 함의
    is_loop: bool     # 자기강화 루프 여부

# 축 이름 정규화 맵
AXIS_ALIASES = {
    "축1": "1", "축2": "2", "축3": "3", "축4": "4",
    "축5": "5", "축6": "6", "축7": "7",
    "고유축A": "A", "고유축B": "B", "고유축C": "C",
    "고유축D": "D", "고유축E": "E",
    "고유축F": "F", "고유축G": "G",
    "고유축H": "H", "고유축I": "I",
    "축A": "A", "축B": "B", "축C": "C",
    "축D": "D", "축E": "E", "축F": "F",
    "축G": "G", "축H": "H", "축I": "I",
    "1": "1", "2": "2", "3": "3", "4": "4",
    "5": "5", "6": "6", "7": "7",
    "A": "A", "B": "B", "C": "C", "D": "D",
    "E": "E", "F": "F", "G": "G", "H": "H", "I": "I",
}

# ──────────────────────────────────────────────
# 44개 메타원리 전수 등록
# ──────────────────────────────────────────────

META_PRINCIPLES = [
    # ── 카너먼 6 (M1~M6) ──
    MetaPrinciple("M1", "카너먼", ("1","5"), "→",
        "인지자원 유한→감정이 기본 판단 모드",
        "고부하 상황에서 감정 경로만 작동", False),
    MetaPrinciple("M2", "카너먼", ("3","5"), "↔",
        "손실고통(2.5배)+감정증폭→변화 거부 자동출력",
        "손실 프레이밍 회피, 참조점 선이동", False),
    MetaPrinciple("M3", "카너먼", ("2","4"), "→",
        "속성대체 왜곡→일관성 스토리→현실 괴리",
        "스토리 일관성↑ = 입력 왜곡 의심↑", False),
    MetaPrinciple("M4", "카너먼", ("4","6"), "↔",
        "현재 스토리↔과거 기억, 미래 예측 양방향 편집",
        "사전 예측 기록, 기억 편집 인식", False),
    MetaPrinciple("M5", "카너먼", ("5","6"), "↔",
        "감정필터→기억회수→감정강화(자기강화 루프)",
        "부정 감정 루프 차단: 감정 상태에서 의사결정 보류", True),
    MetaPrinciple("M6", "카너먼", ("4","4"), "→",
        "편향(방향)+잡음(분산)=총오류. 독립적 오류원",
        "편향 제거만으로 부족. 잡음 감소 별도 필요", False),

    # ── 치알디니 8 (CM1~CM8) ──
    MetaPrinciple("CM1", "치알디니", ("1","A"), "→",
        "인지절약: 호혜 의무감 무비판 실행 자동화",
        "고부하 시 호혜 요청 더 효과적", False),
    MetaPrinciple("CM2", "치알디니", ("3","B"), "↔",
        "손실회피+자기상 포기 고통→몰입 에스컬레이션",
        "매몰비용+자기상 이중 고착 인식", False),
    MetaPrinciple("CM3", "치알디니", ("2","A"), "→",
        "단일속성→'좋은 사람'단순화→호혜·통일성 입력 조작",
        "첫인상·단속성이 관계 전체 결정", False),
    MetaPrinciple("CM4", "치알디니", ("5","A"), "→",
        "감정이 호혜·통일성의 입구이자 증폭기",
        "감정 활성화 후 사회적 요청", False),
    MetaPrinciple("CM5", "치알디니", ("4","B"), "↔",
        "스토리텔링↔자기상. 쌍방향 자기강화 루프",
        "자기 서사 변화=자기상 변화=스토리 재편집", False),
    MetaPrinciple("CM6", "치알디니", ("6","A"), "→",
        "기억편향: 호의 과대/과소 저장, 미해결 부채감 선명",
        "미해결 호혜가 기억에 오래 남음", False),
    MetaPrinciple("CM7", "치알디니", ("A","B"), "↔",
        "보답행동→'갚는 사람' 정체성→호혜 지속(자기강화)",
        "최초 호혜가 정체성 고착=외적 동기 불필요", True),
    MetaPrinciple("CM8", "치알디니", ("C","B"), "→",
        "정체성통합→자기상 확장→이탈=자기상 파괴(비가역)",
        "강한 소속감: 이탈 방지 효과적이나 윤리 위험", False),

    # ── SDT 6 (SM1~SM6) ──
    MetaPrinciple("SM1", "SDT", ("1","E"), "→",
        "인지고갈→내면화 정체→외적/내사 조절 고착",
        "피로·스트레스: 내면화 기대 금물", False),
    MetaPrinciple("SM2", "SDT", ("5","D"), "→",
        "프레이밍(정보적 vs 통제적)→인과소재→동기 질 결정",
        "'왜'(정보적) vs '해야'(통제적)=자율성 보존 vs 파괴", False),
    MetaPrinciple("SM3", "SDT", ("B","E"), "↔",
        "건강한 자기상(가치내면화) vs 조건부 자기상(불안기반 내사)",
        "조건부 자기상='~해야만 나는 가치'=불안 동기", False),
    MetaPrinciple("SM4", "SDT", ("3","D"), "↔",
        "자율성 상실=손실→반항 2.5배 증폭",
        "자율성 박탈의 반발 비용 > 자율성 회복 비용", False),
    MetaPrinciple("SM5", "SDT", ("A","E"), "→",
        "호혜 의무감→내면화 우회→외적 조절 즉시 순응",
        "호혜 순응: 빠르나 비내면화. 의무감 사라지면 중단", False),
    MetaPrinciple("SM6", "SDT", ("D","E"), "↔",
        "마스터키: 자율+충족=상승나선 / 통제+좌절=하강나선",
        "상승/하강 나선 진입 판별이 최우선", True),

    # ── 진화심리 8 (EM1~EM8) ──
    MetaPrinciple("EM1", "진화심리", ("G","3"), "→",
        "손실회피=오류관리 특수사례. EEA 생존경계의 비선형 비용→2.5배",
        "손실 회피 강도는 진화적 교정됨. 변경 불가", False),
    MetaPrinciple("EM2", "진화심리", ("G","5"), "→",
        "감정선행=다시스템 동시조율의 진화적 필연",
        "감정 선행은 적응, 억제하면 비용 증가", False),
    MetaPrinciple("EM3", "진화심리", ("F","4"), "→",
        "과신=번식전략(지위획득·짝유인). 자기기만 적응적 이점",
        "지위 경쟁 맥락에서 과신 자동 증폭", False),
    MetaPrinciple("EM4", "진화심리", ("F","2"), "→",
        "속성대체=정보불투명 환경의 적응. 번식가치·위협·친족 추론",
        "신체적 단서→자동 속성 대체", False),
    MetaPrinciple("EM5", "진화심리", ("G","7"), "↔",
        "무임승차 탐지=호혜체계의 면역반응. 영역 특이적 자동모듈",
        "공정성 위반 탐지: 자동·즉각·강력", False),
    MetaPrinciple("EM6", "진화심리", ("G","C"), "→",
        "혐오=내/외집단 경계의 생물학적 기원. 행동면역 과잉일반화",
        "혐오 기반 편견: 인식 가능하나 자동 반응 제거 어려움", False),
    MetaPrinciple("EM7", "진화심리", ("G","1"), "→",
        "환경불일치: EEA적응+현대초과자극→부적응 체계적 생성",
        "정보·음식·위험신호 과잉: 기존 메커니즘 체계적 오작동", False),
    MetaPrinciple("EM8", "진화심리", ("F","E"), "→",
        "번식전략↔지위추구. 지위=내재적 동기로 설계",
        "지위 추구: 진화적 뿌리. 내재적 동기와 구분 어려움", False),

    # ── 감정이론 8 (EmoM1~EmoM8) ──
    MetaPrinciple("EmoM1", "감정이론", ("5","H"), "→",
        "감정선행→구성·조절의 전제(원재료+필요성) 설정",
        "감정 활성화 필수→구성·조절 과정 시작", False),
    MetaPrinciple("EmoM2", "감정이론", ("H","1"), "↔",
        "감정조절=인지자원 소모, 자원고갈=조절 실패(쌍방향)",
        "조절 과부하→인지 능력 전반 저하", False),
    MetaPrinciple("EmoM3", "감정이론", ("H","6"), "→",
        "감정구성→기억편집 감정적 필터. 감정종류=기억의 색",
        "감정 구성 변화=같은 경험의 기억 재편집", False),
    MetaPrinciple("EmoM4", "감정이론", ("3","H"), "↔",
        "참조점→감정구성 입력, 감정경험→참조점 이동(쌍방향)",
        "손실/이득 맥락↔감정 양방향 상호 결정", False),
    MetaPrinciple("EmoM5", "감정이론", ("H","E"), "↔",
        "감정조절→욕구충족 질 결정, 욕구충족→조절 자원 보충",
        "조절 역량=동기 체계 건강도. 상승/하강 나선 분기", True),
    MetaPrinciple("EmoM6", "감정이론", ("G","H"), "→",
        "위협관리체계→감정구성의 진화적 원형(공포·혐오·분노)",
        "기본 감정: 진화적 기원. 문화적 범주 추가", False),
    MetaPrinciple("EmoM7", "감정이론", ("H","7"), "→",
        "감정세분화 정밀도↔사회적 판단 차별성",
        "감정 세분화 높음=사회적 판단 정밀·공정", False),
    MetaPrinciple("EmoM8", "감정이론", ("H","D"), "↔",
        "자율적 조절→인과소재 내부, 인과소재→조절 동기(쌍방향)",
        "자율적 조절=인과소재 내부화. 강제=외부화", False),

    # ── 행동설계 8 (BM1~BM8) ──
    MetaPrinciple("BM1", "행동설계", ("I","1"), "↔",
        "습관자동화→인지자원 해방, 자원고갈→습관 퇴행(쌍방향)",
        "좋은 습관 자동화=인지 예산 확보. 피로→나쁜 습관 복귀", False),
    MetaPrinciple("BM2", "행동설계", ("5","I"), "→",
        "감정: 습관루프 트리거(부정→위안)+보상(긍정) 동시공급",
        "감정 드라이브 습관: 형성 빠르나 의존 위험", False),
    MetaPrinciple("BM3", "행동설계", ("I","B"), "↔",
        "습관반복→정체성 증거, 정체성→동기비용 제거(자기강화)",
        "'나는 ~하는 사람'=최견고 습관 앵커", True),
    MetaPrinciple("BM4", "행동설계", ("I","E"), "↔",
        "보상→욕구충족 경로 결정, 충족→루프 내재적 에너지(쌍방향)",
        "진짜 욕구 충족 확인. 대체물 보상=악순환", True),
    MetaPrinciple("BM5", "행동설계", ("I","D"), "↔",
        "자율적 선택습관→의지력 보호, 자동화→자율성 강화(쌍방향)",
        "강제 습관=의지력 소모. 자율적 선택=절약", False),
    MetaPrinciple("BM6", "행동설계", ("3","I"), "→",
        "손실회피: 기존 습관 고착+신규 포기 동시유발",
        "습관 전환: 손실 프레이밍 회피. 이득으로 전환", False),
    MetaPrinciple("BM7", "행동설계", ("H","I"), "→",
        "감정조절 실패→습관이 감정의 '비상출구'→습관 의존 증가",
        "감정 조절 강화=나쁜 습관 예방의 상류 개입", False),
    MetaPrinciple("BM8", "행동설계", ("G","I"), "→",
        "환경불일치+초과자극→습관루프 부적응적 과잉강화",
        "SNS·정크푸드·도파민 해킹: 습관 루프 과잉 강화", False),
]

# 자기강화 루프 6개
SELF_REINFORCING_LOOPS = [mp for mp in META_PRINCIPLES if mp.is_loop]

# 허브 축 정의
HUB_AXES = {
    "H": {"name": "감정", "meta_count": 8, "role": "인지-감정-동기 전체 중심"},
    "I": {"name": "행동", "meta_count": 8, "role": "모든 이론을 '실행'으로 통합"},
    "E": {"name": "동기", "meta_count": 6, "role": "자율적 행동의 에너지원. SM6 상승/하강 분기점"},
}

# 설계 최우선 3
DESIGN_PRIORITY = ["SM6", "EmoM5", "BM3"]


# ──────────────────────────────────────────────
# 라우팅 함수
# ──────────────────────────────────────────────

def normalize_axis(name: str) -> str:
    """축 이름을 정규화. '축1'→'1', '고유축A'→'A' 등."""
    return AXIS_ALIASES.get(name.strip(), name.strip().upper())


def route(active_axes: list[str]) -> dict:
    """
    활성 축 리스트 → 관련 메타원리 반환.

    Returns:
        {
            "active_axes": [...],
            "matched": [MetaPrinciple, ...],
            "loops": [MetaPrinciple, ...],
            "hub_involvement": {축: info},
            "design_priority_hit": [id, ...],
        }
    """
    normalized = {normalize_axis(a) for a in active_axes}

    matched = []
    for mp in META_PRINCIPLES:
        ax_from, ax_to = mp.axes
        # 축 쌍 중 하나라도 활성 축에 포함되면 매칭
        if ax_from in normalized or ax_to in normalized:
            # 양쪽 모두 활성이면 우선순위 높음
            both = ax_from in normalized and ax_to in normalized
            matched.append((mp, both))

    # 양쪽 활성 우선 정렬
    matched.sort(key=lambda x: (not x[1], x[0].id))

    loops = [mp for mp, _ in matched if mp.is_loop]
    hub_inv = {ax: HUB_AXES[ax] for ax in normalized if ax in HUB_AXES}
    dp_hit = [pid for pid in DESIGN_PRIORITY
              if any(mp.id == pid for mp, _ in matched)]

    return {
        "active_axes": sorted(normalized),
        "matched_count": len(matched),
        "both_active": [(mp, True) for mp, both in matched if both],
        "single_active": [(mp, False) for mp, both in matched if not both],
        "loops": loops,
        "hub_involvement": hub_inv,
        "design_priority_hit": dp_hit,
    }


def format_result(result: dict) -> str:
    """결과를 마크다운 테이블로 포맷."""
    lines = []
    lines.append(f"## 활성 축: {', '.join(result['active_axes'])}")
    lines.append(f"매칭 메타원리: {result['matched_count']}개")
    lines.append("")

    # 양쪽 활성 (핵심)
    if result["both_active"]:
        lines.append("### 🔴 양쪽 축 모두 활성 (핵심 상호작용)")
        lines.append("")
        lines.append("| ID | 계열 | 접합 | 방향 | 메커니즘 | 설계 함의 | 루프 |")
        lines.append("|---|---|---|---|---|---|---|")
        for mp, _ in result["both_active"]:
            loop_mark = "⟳" if mp.is_loop else ""
            lines.append(f"| {mp.id} | {mp.series} | {mp.axes[0]}→{mp.axes[1]} | {mp.direction} | {mp.mechanism} | {mp.design_impl} | {loop_mark} |")
        lines.append("")

    # 편측 활성
    if result["single_active"]:
        lines.append("### 🟡 한쪽 축만 활성 (잠재적 연결)")
        lines.append("")
        lines.append("| ID | 계열 | 접합 | 방향 | 메커니즘 | 루프 |")
        lines.append("|---|---|---|---|---|---|")
        for mp, _ in result["single_active"]:
            loop_mark = "⟳" if mp.is_loop else ""
            lines.append(f"| {mp.id} | {mp.series} | {mp.axes[0]}→{mp.axes[1]} | {mp.direction} | {mp.mechanism} | {loop_mark} |")
        lines.append("")

    # 자기강화 루프
    if result["loops"]:
        lines.append(f"### ⟳ 자기강화 루프 감지: {len(result['loops'])}개")
        for mp in result["loops"]:
            lines.append(f"- **{mp.id}** ({mp.axes[0]}↔{mp.axes[1]}): {mp.mechanism}")
        lines.append("")

    # 허브 축
    if result["hub_involvement"]:
        lines.append("### 🔵 허브 축 관여")
        for ax, info in result["hub_involvement"].items():
            lines.append(f"- **축{ax}** ({info['name']}): {info['role']}")
        lines.append("")

    # 설계 최우선
    if result["design_priority_hit"]:
        lines.append(f"### ⚡ 설계 최우선 히트: {', '.join(result['design_priority_hit'])}")
        lines.append("")

    return "\n".join(lines)


def print_all():
    """전체 44개 매트릭스 출력."""
    lines = ["## 전체 메타원리 매트릭스 (44개)", ""]
    lines.append("| ID | 계열 | 접합 | 방향 | 메커니즘 | 설계 함의 | 루프 |")
    lines.append("|---|---|---|---|---|---|---|")
    for mp in META_PRINCIPLES:
        loop_mark = "⟳" if mp.is_loop else ""
        lines.append(f"| {mp.id} | {mp.series} | {mp.axes[0]}→{mp.axes[1]} | {mp.direction} | {mp.mechanism} | {mp.design_impl} | {loop_mark} |")
    print("\n".join(lines))


def print_loops():
    """자기강화 루프 6개 출력."""
    lines = ["## 자기강화 루프 6개", ""]
    lines.append("| ID | 접합 | 메커니즘 | 위험/기회 |")
    lines.append("|---|---|---|---|")
    for mp in SELF_REINFORCING_LOOPS:
        lines.append(f"| {mp.id} | {mp.axes[0]}↔{mp.axes[1]} | {mp.mechanism} | {mp.design_impl} |")
    print("\n".join(lines))


def print_hubs():
    """허브 축 요약 출력."""
    lines = ["## 3대 허브 축", ""]
    lines.append("| 허브 | 접합 수 | 역할 |")
    lines.append("|---|---|---|")
    for ax, info in HUB_AXES.items():
        lines.append(f"| 축{ax} ({info['name']}) | {info['meta_count']} 메타원리 | {info['role']} |")
    print("\n".join(lines))


# ──────────────────────────────────────────────
# 상세 출력 함수 (axes_data 활용)
# ──────────────────────────────────────────────

def _load_axes_data():
    """axes_data.py를 lazy import."""
    try:
        from axes_data import AXES, SPECIAL_TABLES, MODE_PROTOCOLS
        return AXES, SPECIAL_TABLES, MODE_PROTOCOLS
    except ImportError:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        import importlib.util
        spec = importlib.util.spec_from_file_location("axes_data", os.path.join(script_dir, "axes_data.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.AXES, mod.SPECIAL_TABLES, mod.MODE_PROTOCOLS


def print_axis_detail(axis_id: str, include_tables: bool = False):
    """특정 축의 풀 상세 출력: 자명명제 + 인과 체인 + 설계 원칙."""
    AXES, SPECIAL_TABLES, _ = _load_axes_data()
    ax_id = normalize_axis(axis_id)

    if ax_id not in AXES:
        print(f"[오류] 축 '{axis_id}' 찾을 수 없음. 유효: 1~7, A~I")
        return

    ax = AXES[ax_id]
    lines = []
    lines.append(f"## 축{ax_id}. {ax['name']} ({ax['source']})")
    lines.append("")
    lines.append(f"**자명명제**: {ax['axiom']}")
    lines.append("")

    # 인과 체인
    for chain in ax.get("chains", []):
        lines.append(f"### 체인 {chain['id']} {chain['title']}")
        lines.append("")
        lines.append("```")
        for step in chain.get("steps", []):
            lines.append(step)
        lines.append("```")
        lines.append("")
        if chain.get("meaning"):
            lines.append(f"**의미**: {chain['meaning']}")
            lines.append("")

    # 설계 원칙
    if ax.get("design_principles"):
        lines.append("### 설계 원칙")
        lines.append("")
        for dp in ax["design_principles"]:
            lines.append(f"- {dp}")
        lines.append("")

    # 교차 참조
    if ax.get("cross_refs"):
        lines.append("### 축간 연동")
        lines.append("")
        for cr in ax["cross_refs"]:
            lines.append(f"- {cr}")
        lines.append("")

    # 특수 테이블
    if include_tables:
        table_map = {
            "E": "internalization_continuum",
            "H": ["emotion_granularity", "regulation_timing"],
            "I": ["friction_motivation", "design_matrix"],
        }
        table_keys = table_map.get(ax_id, [])
        if isinstance(table_keys, str):
            table_keys = [table_keys]

        for tk in table_keys:
            if tk in SPECIAL_TABLES:
                tdata = SPECIAL_TABLES[tk]
                lines.append(f"### 특수 테이블: {tk}")
                lines.append("")
                if tdata:
                    headers = list(tdata[0].keys())
                    lines.append("| " + " | ".join(headers) + " |")
                    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
                    for row in tdata:
                        lines.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
                    lines.append("")

    print("\n".join(lines))


def print_detail_route(active_axes: list[str]):
    """상세 라우팅: 메타원리 + 활성 축별 자명명제·체인·설계원칙 요약."""
    AXES, _, _ = _load_axes_data()
    result = route(active_axes)

    # 기본 라우팅 결과
    print(format_result(result))

    # 활성 축별 상세 요약 (체인 전문이 아닌 요약)
    normalized = {normalize_axis(a) for a in active_axes}
    lines = ["---", "## 활성 축 상세", ""]

    for ax_id in sorted(normalized):
        if ax_id not in AXES:
            continue
        ax = AXES[ax_id]
        lines.append(f"### 축{ax_id}. {ax['name']}")
        lines.append(f"**자명명제**: {ax['axiom']}")
        lines.append("")

        # 체인 요약 (제목 + 의미만)
        for chain in ax.get("chains", []):
            meaning = chain.get("meaning", "")
            lines.append(f"- **{chain['id']} {chain['title']}**: {meaning}")
        lines.append("")

        # 설계 원칙
        if ax.get("design_principles"):
            lines.append("**설계 원칙**: " + " | ".join(ax["design_principles"]))
            lines.append("")

    print("\n".join(lines))


def print_mode(mode_name: str):
    """모드별 실행 프로토콜 출력."""
    _, _, MODE_PROTOCOLS = _load_axes_data()

    if mode_name not in MODE_PROTOCOLS:
        print(f"[오류] 모드 '{mode_name}' 없음. 유효: 진단, 예측, 설계")
        return

    mode = MODE_PROTOCOLS[mode_name]
    lines = []
    lines.append(f"## {mode['title']}")
    lines.append(f"{mode['description']}")
    lines.append("")

    # 프로토콜
    lines.append("### 실행 프로토콜")
    lines.append("")
    lines.append("| 단계 | 작업 | 상세 | 체크포인트 |")
    lines.append("|---|---|---|---|")
    for step in mode.get("protocol", []):
        lines.append(f"| {step['step']} | {step['task']} | {step['detail']} | {step['checkpoint']} |")
    lines.append("")

    # 출력 형식
    lines.append("### 출력 형식")
    lines.append("")
    for fmt in mode.get("output_format", []):
        lines.append(f"- {fmt}")
    lines.append("")

    # 핵심 질문
    if mode.get("core_questions"):
        lines.append("### 핵심 질문")
        lines.append("")
        for q in mode["core_questions"]:
            lines.append(f"- {q}")
        lines.append("")

    print("\n".join(lines))


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    if "--all" in args:
        print_all()
    elif "--loops" in args:
        print_loops()
    elif "--hubs" in args:
        print_hubs()
    elif "--axis" in args:
        # 특정 축 상세
        remaining = [a for a in args if a not in ("--axis", "--table")]
        include_tables = "--table" in args
        for ax in remaining:
            print_axis_detail(ax, include_tables=include_tables)
    elif "--mode" in args:
        # 모드 프로토콜
        remaining = [a for a in args if a != "--mode"]
        for m in remaining:
            print_mode(m)
    elif "--detail" in args:
        # 상세 라우팅
        axes = [a for a in args if a != "--detail"]
        print_detail_route(axes)
    elif "--json" in args:
        # JSON 모드: 나머지 인자를 축으로
        axes = [a for a in args if not a.startswith("--")]
        result = route(axes)
        # NamedTuple → dict 변환
        out = {
            "active_axes": result["active_axes"],
            "matched_count": result["matched_count"],
            "both_active": [mp._asdict() for mp, _ in result["both_active"]],
            "single_active": [mp._asdict() for mp, _ in result["single_active"]],
            "loops": [mp._asdict() for mp in result["loops"]],
            "hub_involvement": result["hub_involvement"],
            "design_priority_hit": result["design_priority_hit"],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        result = route(args)
        print(format_result(result))
