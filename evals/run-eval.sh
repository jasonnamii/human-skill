#!/usr/bin/env bash
# human-skill 회귀 테스트 수동 실행 가이드
# 사용법: bash run-eval.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASES_FILE="$SCRIPT_DIR/cases.json"
EXPECTED_FILE="$SCRIPT_DIR/expected-outputs.md"

echo "================================================"
echo " human-skill Regression Test"
echo "================================================"
echo ""
echo "이 스크립트는 수동 회귀 테스트를 안내합니다."
echo "(자동 LLM 평가는 P2 이연 항목입니다.)"
echo ""

if [ ! -f "$CASES_FILE" ]; then
  echo "ERROR: cases.json 없음 ($CASES_FILE)"
  exit 1
fi

if [ ! -f "$EXPECTED_FILE" ]; then
  echo "ERROR: expected-outputs.md 없음 ($EXPECTED_FILE)"
  exit 1
fi

# 케이스 개수
CASE_COUNT=$(python3 -c "import json; print(len(json.load(open('$CASES_FILE'))['cases']))")
echo "총 ${CASE_COUNT}개 케이스 확인됨."
echo ""

# 각 케이스 입력 표시
python3 << 'EOF'
import json
import os

cases_path = os.environ.get('CASES_FILE') or os.path.join(os.path.dirname(__file__) if '__file__' in dir() else '.', 'cases.json')
with open(cases_path.replace('run-eval.sh', 'cases.json') if cases_path.endswith('.sh') else cases_path) as f:
    data = json.load(f)

for i, case in enumerate(data['cases'], 1):
    print(f"--- 케이스 {i}: {case['id']} ({case['mode']} 모드) ---")
    print(f"입력: {case['input']}")
    print(f"기대 축: {', '.join(case['expected'].get('active_axes_min', []))}")
    print(f"기대 메타원리: {', '.join(case['expected'].get('meta_principles_applied', []))}")
    print()
EOF

echo "================================================"
echo " 실행 절차"
echo "================================================"
echo "1. 각 케이스의 'input'을 Claude에게 전달 (human-skill 발동)"
echo "2. 출력을 expected-outputs.md의 합격 기준과 대조"
echo "3. 채점표에 PASS/FAIL 기록"
echo ""
echo "자동화 필요 시: scripts/validate.py로 구조 정합성만 먼저 점검"
echo "  python3 /sessions/\$SESSION/human-skill/scripts/validate.py"
echo ""
echo "완료."
