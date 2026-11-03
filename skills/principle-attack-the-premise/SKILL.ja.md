---
name: principle-attack-the-premise
description: "Apply when two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it."
disable-model-invocation: true
---

# Attack the Premise

同じ前提を共有する修正が 2 つ以上、同じゲートで失敗したら、疑うべきは修正ではなく前提です。

**なぜ:** 失敗した修正はそれぞれ、その修正が前提とした信念に対する反証です。同じ前提に 3 つ目の修正を重ねるのは、証拠がすでに「原因はそこではない」と言っている場所に労力を費やすことです。

**パターン:**
- **前提を書き出す。** 前提とは、失敗した修正のすべてが仮定していた 1 文のことです。
- **次の修正の前に前提を試す。** 前提が偽なら違う結果になる観察を見つけ、実行します。失敗の大きさだけでなく、失敗がどう分布しているかを見ます。チェックは [Build the Lever](../principle-build-the-lever/SKILL.ja.md) に従って再実行可能にします。
- **証拠に従う。** 証拠が前提と矛盾するなら、原因は別の場所にあります。失敗に共通していて、前提が予測していなかったものは何かを探します。証拠が前提を裏づけるなら、[Fix Root Causes](../principle-fix-root-causes/SKILL.ja.md) に従って次の「なぜ」を問います。以前の修正は、原因ではなく結果を扱っていたのかもしれません。
- **補償するのではなく、条件を取り除く。** [Laziness Protocol](../principle-laziness-protocol/SKILL.ja.md) に従います。証拠が、ある部分はいつも負ける側に落ちると示しているなら、そうさせているものを変えます。後始末をする仕組みは、原因をそのまま残し、実行のたびに作業を増やします。

**停止:** 前提を書き出して試す前に、次の修正に着手してはいけません。

この原則は、新しい要件に合わせて設計を作り直す [Redesign from First Principles](../principle-redesign-from-first-principles/SKILL.ja.md) とは別のものです。こちらは、現在の設計が事実として前提しているものを問います。
