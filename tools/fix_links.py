#!/usr/bin/env python3
"""pstack-ja 内の相対リンクを .ja.md に張り替える。

原文のリンクは `./x.md` や `../../skills/foo/SKILL.md` の形で残している。
訳文ツリーでは同名の `.ja.md` が存在するので、それを指すように直す。
存在しないリンク（未訳の references など）はそのまま残す。
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\]\(([^)\s]+)\)")


def resolve_target(path: Path, raw: str) -> str | None:
    if raw.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target, _, anchor = raw.partition("#")
    if not target.endswith(".md"):
        return None
    base = path.parent.resolve()
    candidate = (base / target).resolve()
    ja = candidate.with_suffix(".ja.md")
    if not ja.exists():
        return None
    rel = Path(os.path.relpath(ja, base))
    # 見出しを日本語化しているため、原文のアンカーは訳文では解決しない。
    # ページ自体には飛べるよう、アンカーは落とす。
    return rel.as_posix()


def main() -> int:
    changed_files = 0
    changed_links = 0
    for path in sorted(ROOT.rglob("*.ja.md")):
        text = path.read_text(encoding="utf-8")
        count = 0

        def repl(match: re.Match[str]) -> str:
            nonlocal count
            fixed = resolve_target(path, match.group(1))
            if fixed is None:
                return match.group(0)
            count += 1
            return f"]({fixed})"

        new_text = LINK.sub(repl, text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed_files += 1
            changed_links += count
    print(f"updated {changed_links} links in {changed_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
