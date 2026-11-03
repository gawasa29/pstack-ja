---
name: principle-explain-the-number
description: "Apply before you measure, and before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. Find what limits it, and rule out that it measured something other than the work you think."
disable-model-invocation: true
---

# Explain the Number

- **実行する前に判断を書く。** どの結果が出たら判断が変わるのか、ノイズフロアはどのくらいかを名指しします。実行間のばらつきが効果より大きくなったら止めます。
- **「なぜ 2 倍にならないのか」を問う。** 結果を制限している資源やコード経路を名指しします。コア、ロック、ディスク、ネットワーク、負荷生成器そのものなどです。プロファイル、または実行中に取ったシステムカウンタから得て、ソースに対応づけます。コードを読んでの推測はリミッターではありません。なぜその数値が 2 倍にならないのか言えないなら、何を測ったのかわかっていません。
- **その数値が測っているかもしれない別のものを列挙し、それぞれを証拠で排除する。** よくある容疑者は、エラー、スキップされた作業やキャッシュされた作業、一度も実行されなかったコード、チューニングされていない側（既定設定のままの側）、ノイズ、端から端まで通して影響が小さすぎる部分です。
- **証拠を数値と一緒に残す。** 実行回数、ばらつき、リミッターをノートかリンクした成果物に書きます。

パフォーマンスの数値なら、[benchmark-checklist](../benchmark-checklist/SKILL.ja.md) スキルで手順をすべて実行します。eval の結果なら、試行について同じことを問います。すべての実行がタスクを行ったか、差は試行やモデルをまたいで保たれるか、そのシナリオは意味を持つか。

次のいずれかに当たるなら、この原則を飛ばしています。判断を変えるはずの結果を書かずに実行を始めたとき。数値の背後にある証拠に実行回数、ばらつき、名指しされたリミッターがないとき。節約できた時間が、変更した部分の所要時間より大きいとき。

これは、出力が本物であることを確かめる [Prove It Works](../principle-prove-it-works/SKILL.ja.md) とは別のものです。
