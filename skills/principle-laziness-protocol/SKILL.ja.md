---
name: principle-laziness-protocol
description: "Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem."
disable-model-invocation: true
---

# Laziness Protocol

- **判断を集約する。** 同じ選択を複数の場所で繰り返しません。1 つの正となる情報源の背後に置き、結果を単純なフラグとして渡します。
- **diff を最小化する。** 問題を解く最小の変更をします。行数が少ないほうが「エレガントな」定型より勝ります。
