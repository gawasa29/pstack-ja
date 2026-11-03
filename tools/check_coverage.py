#!/usr/bin/env python3
"""pstack 原文と pstack-ja 訳文の対応を検査する。

対象は読む価値のあるテキスト（README、docs、skills の SKILL.md と references、
agents、automations の Markdown）。コードや画像は対象外。
"""

from __future__ import annotations

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


def target_for(src: Path) -> Path:
    rel = src.relative_to(SRC)
    return (DST / rel).with_suffix(".ja.md")


def main() -> int:
    sources = sorted({p for pattern in PATTERNS for p in SRC.glob(pattern) if p.is_file()})
    missing: list[Path] = []
    translated = 0
    src_lines = 0
    dst_lines = 0
    for src in sources:
        dst = target_for(src)
        src_lines += len(src.read_text(encoding="utf-8").splitlines())
        if dst.exists():
            translated += 1
            dst_lines += len(dst.read_text(encoding="utf-8").splitlines())
        else:
            missing.append(src)

    print(f"source files : {len(sources)}  ({src_lines} lines)")
    print(f"translated   : {translated}  ({dst_lines} lines)")
    print(f"missing      : {len(missing)}")
    if missing:
        print("\n未訳:")
        for src in missing:
            print(f"  {src.relative_to(SRC)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
