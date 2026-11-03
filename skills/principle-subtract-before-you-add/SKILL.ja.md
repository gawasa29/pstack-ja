---
name: principle-subtract-before-you-add
description: "Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base."
disable-model-invocation: true
---

# Subtract Before You Add

システムを進化させるときは、まず複雑さを取り除き、それから築きます。既定は削除です。

単純化を持続的な投資にします。見つけたときと同じかより小さい表面のまま、設計を少しだけ単純に、より有能にして後に残します。

- 構築より先に削除を順序づける
- 磨く前に削る（品質に投資する前に最小まで到達する）
- 投機的なエッジケースではなく、観察された利用のために設計する
- 仕様が要求する以上の、投機的なバリデータ、パーサ、ガードを置かない
- プロンプトを単純化する（冗長な指示、過剰なテンプレートを取り除く）
- 参照に新しい内容がないときは、スタブを残すのではなく削除する
