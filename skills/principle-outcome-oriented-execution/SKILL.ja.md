---
name: principle-outcome-oriented-execution
description: "Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code."
disable-model-invocation: true
---

# Outcome-Oriented Execution

滑らかな中間状態を保つのではなく、意図した検証可能な最終状態に向けて最適化します。

**なぜ:** すべての中間ステップを完全に安定に保とうとすると、一時的な互換コードが生まれ、それが長く残る負債になります。目標のアーキテクチャに収束させ、明示的な検証境界で正しさを証明します。

**中核のルール:**
- 過渡的な安定より、最終状態の完全性を優先する
- 中間の破損は、計画され、範囲が定められ、可逆であるなら許容される

**ガードレール:**
- 明示的なフェーズ境界を持つ、計画的な書き換えと移行に使う
- 一時的な破損が許容される場所を宣言する
- 移行中も、活発に触っている領域にはシグナルの強いチェックを保つ
- 計画の完了時には、静的な検証と実行時の検証をすべて要求する
