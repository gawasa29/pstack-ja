---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
disable-model-invocation: true
---

# スワーム（Swarm）

## 始め方

何かを起動する前に、各フェーズに 1 項目ずつ todo リストを作ります。

1. 枠組み（Frame）
2. ファンアウト（Fan out）
3. 集約（Aggregate）
4. レポート（Report）

## フェーズ A: 枠組み（Frame）

1. 完了条件（done predicate）と、swarm が返さなければならない成果物またはレポートを述べます。
2. 形を選びます。スライスに分割する、同一のブリーフで N 人のワーカーをレースさせる、その両方を混ぜる、のいずれかです。レースか混合の形なら、起動する前に `first pass`、`rank all`、`best-of` のどれかを宣言します。
3. `~/.cursor/rules/pstack-models.mdc` の `swarm workers` 行からワーカーのモデルを選びます。ルールかその行がなければ、`grok-4.7-xhigh-fast` を使います。`auto` か `inherit-parent` なら、ワーカーが親モデルで走るよう `model` を省略します。Task ツールがスラッグを拒否したら、既定を使い、そう言います。既定を拒否したら、エラーメッセージにある同じファミリーの最も近い有効なスラッグを使います。モデル同士のレースなら、各腕のモデルを最初に名指しします。各サブエージェントの推論の段と、その仕事に合った fast か標準の速度は、**poteto-mode** スキルの Subagents セクションに従って選びます。
4. ワーカーが書き込むなら、それぞれに自分の書き込み可能な出力先を与えます。ワーカーがコミットを検証したり測ったりするときは、各ブリーフが正確な SHA を名指しします。計測のブリーフは方法（サンプル数、1 サンプルとは何か、順序）も名指しします。ワーカーはその両方を結果に記録します。

## フェーズ B: ファンアウト（Fan out）

N 人のワーカーを 1 つのメッセージで、`subagent_type: generalPurpose`、`environment: "cloud"`、`run_in_background: true`、そしてステップ 3 のモデル（`auto` か `inherit-parent` なら未設定）を付けて起動します。`environment: "local"` を使うのは、ワーカーがユーザーのコンピュータ上の何かにアクセスする必要があるときだけです。

ワーカーが既定ではない push 済みのブランチから始める必要があるときは、`cloud_base_branch` を渡します。

各ブリーフは単独で完結させます。目的、範囲、正確なスライスかレースの腕、検証のしかた、報告する内容を含めます。報告は証拠付きで `PASS`、`ISSUES`、`BLOCKED` のいずれかを使います。欠陥を証明できるワーカーは `ISSUES` を報告し、最初の 1 つだけでなく、証明できる問題をすべて並べます。

ワーカーが脱落したら、N-1 で進め、そう記録します。

## フェーズ C: 集約（Aggregate）

最終結果を読みます。ブリーフが名指しした SHA と方法を記録していない結果は捨て、そのワーカーを 1 回だけ再起動します。2 回目も欠けたら、欠落として記録します。欠落は合格として数えません。カバレッジなら、必要なスライスすべてに結果が要ります。レースなら、最初に宣言した選択ルールを適用します。first pass、rank all、best-of のいずれかです。ワーカーの生のダンプを貼ってはいけません。

## フェーズ D: レポート（Report）

結果表、問題の 1 行要約、欠落や脱落、レースなら使ったルールを含む、チャット内の統合レポートを 1 つ返します。
