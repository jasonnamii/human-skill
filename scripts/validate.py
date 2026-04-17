#!/usr/bin/env python3
"""
human-skill self-check validator
SKILL.md 구조 정합성·축 일관성·메타원리 번호·@uses 실존 검증

사용법:
    python validate.py                    # 현재 디렉토리 기준
    python validate.py /path/to/skill/    # 지정 경로
"""

import os
import re
import sys
import json
from pathlib import Path


def find_skill_root(hint: str = None) -> Path:
    """SKILL.md가 있는 루트 디렉토리 탐색."""
    if hint:
        p = Path(hint).resolve()
    else:
        p = Path(__file__).resolve().parent.parent
    if (p / "SKILL.md").exists():
        return p
    # fallback: walk up
    for parent in p.parents:
        if (parent / "SKILL.md").exists():
            return parent
    raise FileNotFoundError(f"SKILL.md not found near {p}")


def read_skill_md(root: Path) -> str:
    return (root / "SKILL.md").read_text(encoding="utf-8")


def parse_frontmatter(content: str) -> dict:
    """--- ... --- 구간을 간이 파싱."""
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    result = {"raw": block}
    for line in block.split("\n"):
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            result[k.strip().strip('"')] = v.strip().strip('"')
    # @uses 블록 추출
    uses = re.findall(r"^\s*-\s+(.+)$", block, re.MULTILINE)
    result["_uses_list"] = uses
    return result


def check_uses_files_exist(root: Path, uses: list) -> list:
    """@uses 파일 전부 실존 확인."""
    missing = []
    for rel in uses:
        p = root / rel
        if not p.exists():
            missing.append(rel)
    return missing


def check_axes_consistency(root: Path) -> dict:
    """
    16축 이름 일관성:
      SKILL.md §6의 축 이름 ↔ scripts/axes_data.py ↔ references/axes-*.md
    """
    skill_md = read_skill_md(root)
    # §6 계층도에서 축 이름 추출 (축1·축A·축G 등)
    axes_in_spine = set(re.findall(r"축[0-9A-I](?=\(|[^0-9A-I])", skill_md))

    # axes_data.py 존재 시 AXES 키 추출
    axes_data_path = root / "scripts" / "axes_data.py"
    axes_in_data = set()
    if axes_data_path.exists():
        txt = axes_data_path.read_text(encoding="utf-8")
        axes_in_data = set(re.findall(r'["\'](축[0-9A-I])["\']', txt))

    missing_in_data = axes_in_spine - axes_in_data if axes_in_data else set()
    extra_in_data = axes_in_data - axes_in_spine if axes_in_data else set()

    return {
        "spine_axes_count": len(axes_in_spine),
        "data_axes_count": len(axes_in_data),
        "missing_in_data": sorted(missing_in_data),
        "extra_in_data": sorted(extra_in_data),
    }


def check_meta_principles(root: Path) -> dict:
    """44 메타원리 번호 언급 확인 (M1~M7, CM1~CM7, SM1~SM6 등 6계열)."""
    skill_md = read_skill_md(root)
    meta_refs = set(re.findall(r"\b(M[0-9]+|CM[0-9]+|SM[0-9]+|BM[0-9]+|EmoM[0-9]+|EvoM[0-9]+)\b", skill_md))
    return {
        "meta_principles_referenced": sorted(meta_refs),
        "count": len(meta_refs),
    }


def check_hub_axes(root: Path) -> dict:
    """허브 축(H·I·E) 명시 확인."""
    skill_md = read_skill_md(root)
    hubs = {
        "축H": "축H" in skill_md and "허브" in skill_md,
        "축I": "축I" in skill_md,
        "축E": "축E" in skill_md,
    }
    return hubs


def check_required_sections(content: str) -> dict:
    """SKILL.md 필수 섹션 존재 확인."""
    required = {
        "절대 규칙": "절대 규칙" in content,
        "모드 자동 판별": "모드 자동 판별" in content,
        "스크리닝": "스크리닝" in content,
        "메타원리 라우팅": "메타원리 라우팅" in content,
        "리포트 변환": "리포트 변환" in content,
        "Gotchas": "Gotchas" in content,
        "NOT 섹션": "## NOT" in content or "NOT —" in content,
    }
    return required


def check_trigger_tiers(fm: dict) -> dict:
    """description에서 P1·P2·P3·P4·P5·NOT 키워드 존재 확인."""
    desc = fm.get("description", "")
    tiers = {
        "P1": "P1:" in desc,
        "P2": "P2:" in desc,
        "P3": "P3:" in desc,
        "P4": "P4:" in desc,
        "P5": "P5:" in desc,
        "NOT": "NOT:" in desc,
    }
    return tiers


def main():
    try:
        root = find_skill_root(sys.argv[1] if len(sys.argv) > 1 else None)
    except FileNotFoundError as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    content = read_skill_md(root)
    fm = parse_frontmatter(content)
    uses = fm.get("_uses_list", [])

    report = {
        "skill_root": str(root),
        "skill_name": fm.get("name"),
        "version": fm.get("version"),
        "size_bytes": len(content.encode("utf-8")),
        "checks": {
            "frontmatter_present": bool(fm),
            "uses_count": len(uses),
            "uses_missing_files": check_uses_files_exist(root, uses),
            "axes_consistency": check_axes_consistency(root),
            "meta_principles": check_meta_principles(root),
            "hub_axes": check_hub_axes(root),
            "required_sections": check_required_sections(content),
            "trigger_tiers": check_trigger_tiers(fm),
        },
    }

    errors = []
    if not fm:
        errors.append("frontmatter missing")
    if not fm.get("version"):
        errors.append("version field missing")
    if report["checks"]["uses_missing_files"]:
        errors.append(f"uses files missing: {report['checks']['uses_missing_files']}")
    if report["checks"]["axes_consistency"]["missing_in_data"]:
        errors.append(f"axes missing in data: {report['checks']['axes_consistency']['missing_in_data']}")
    missing_sections = [k for k, v in report["checks"]["required_sections"].items() if not v]
    if missing_sections:
        errors.append(f"required sections missing: {missing_sections}")
    missing_tiers = [k for k, v in report["checks"]["trigger_tiers"].items() if not v]
    if missing_tiers:
        errors.append(f"trigger tiers missing: {missing_tiers}")

    report["errors"] = errors
    report["ok"] = len(errors) == 0

    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
