#!/usr/bin/env python3
"""原文と訳文の Markdown 構造を比較する。

リンク先の集合、コードフェンス数、インラインコードの集合、見出しレベルごとの数を見る。
訳文側で構造が壊れていないかを機械的に検出するためのもの。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SRC = Path.home() / "work/cursor-plugins/pstack"
DST = Path.home() / "work/pstack-ja"

PATTERNS = [
    "README.md",
    "docs/**/*.md",
    "skills/**/SKILL.md",
    "skills/**/playbooks/*.md",
    "skills/**/references/**/*.md",
    "agents/*.md",
    "automations/**/*.md",
]

FENCE = re.compile(r"^\s*```")
HEADING = re.compile(r"^(#{1,6})\s")
LINK = re.compile(r"\]\(([^)\s]+)\)")
INLINE = re.compile(r"`([^`\n]+)`")


def stats(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    fences = 0
    headings: dict[int, int] = {}
    for line in lines:
        if FENCE.match(line):
            fences += 1
        m = HEADING.match(line)
        if m:
            headings[len(m.group(1))] = headings.get(len(m.group(1)), 0) + 1
    text = "\n".join(lines)
    # コードフェンスの中のインラインコードは数えない
    prose = []
    in_code = False
    for line in lines:
        if FENCE.match(line):
            in_code = not in_code
            continue
        if not in_code:
            prose.append(line)
    prose_text = "\n".join(prose)
    return {
        "fences": fences,
        "headings": headings,
        "links": set(LINK.findall(text)),
        "inline": set(INLINE.findall(prose_text)),
        "lines": len(lines),
    }


def main() -> int:
    problems = 0
    sources = sorted({p for pattern in PATTERNS for p in SRC.glob(pattern) if p.is_file()})
    for src in sources:
        rel = src.relative_to(SRC)
        dst = (DST / rel).with_suffix(".ja.md")
        if not dst.exists():
            continue
        a, b = stats(src), stats(dst)
        diffs = []
        if a["lines"] != b["lines"]:
            diffs.append(f"lines {a['lines']} -> {b['lines']}")
        if a["fences"] != b["fences"]:
            diffs.append(f"fences {a['fences']} -> {b['fences']}")
        if a["headings"] != b["headings"]:
            diffs.append(f"headings {a['headings']} -> {b['headings']}")
        # 訳文では .md を .ja.md に張り替えているので、比較時に戻す
        def norm(link: str) -> str:
            return link.replace(".ja.md", ".md").removeprefix("./").split("#")[0]

        missing_links = {norm(l) for l in a["links"]} - {norm(l) for l in b["links"]}
        if missing_links:
            diffs.append(f"links missing {len(missing_links)}: {sorted(missing_links)[:3]}")
        missing_inline = a["inline"] - b["inline"]
        if missing_inline:
            diffs.append(f"inline missing {len(missing_inline)}: {sorted(missing_inline)[:3]}")
        if diffs:
            problems += 1
            print(f"{rel}:")
            for d in diffs:
                print(f"  - {d}")
    print(f"\nchecked {sum(1 for src in sources if (DST / src.relative_to(SRC)).with_suffix('.ja.md').exists())} pairs, {problems} with diffs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
