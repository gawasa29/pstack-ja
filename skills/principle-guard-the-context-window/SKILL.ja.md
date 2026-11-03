---
name: principle-guard-the-context-window
description: "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads."
disable-model-invocation: true
---

# Guard the Context Window

**なぜ:** コンテキストのあふれは推論の質を下げ、圧縮のアーティファクトを生み、進行を止めます。

**パターン:**
- **フェーズを適切な大きさに分け、範囲に上限を置く。** フェーズあたりのファイル数を制限し、ターンの予算を決め、仕組みのコストを見込みます。
