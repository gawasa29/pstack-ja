---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

# 仕組みを調べる（How）

「X はどう動くのか」という問いに答えるためにコードベースを調べます。サブシステムに初めて入るシニアエンジニアの水準で、動くメンタルモデルを組み立てられるだけのアーキテクチャ説明を作ります。注釈付きのソースコードのように読めるほど詳しくする必要はありません。

どのスポーンも、`subagent_type: generalPurpose` と `readonly: true` を付けた Task サブエージェントです。探索役は `pstack-models.mdc` ルールの `how explorer` 行（既定は `grok-4.7-xhigh-fast`）を使い、説明役はすべて `how explainer` 行（既定は `claude-opus-5-5-xhigh`）を使います。`model` にはその行の値を設定し、ルールか行が無ければ既定値を使います。値が `auto` か `inherit-parent` のときは `model` を未設定のままにします。Task ツールがスラッグを拒否したら既定値を使い、その旨を告げます。既定値を拒否したら、エラーメッセージから同じファミリーで最も近い有効なスラッグを使います。各サブエージェントの推論レベルと fast / standard の速度は、**poteto-mode** スキルの Subagents セクションに従って、その作業に合わせて選びます。

## 1. 複雑さを見積もる

範囲が曖昧なら、自分の解釈を述べて調べます。ユーザーは方向を変えられます。

- **単純**（単一のモジュール、小さなユーティリティ、「関数 X はどう動くか」のような狭い問い）: 探索役は置きません。`references/explainer-prompt.md` から探索役の所見セクションを除いて組み立てた説明役を 1 つ立ち上げ、探索と説明を 1 回でやらせます。ステップ 4 に進みます。
- **複雑**（複数のファイルやサービスにまたがるサブシステム、横断的な機能、アーキテクチャ全体の概観）: ステップ 2 に進みます。

迷ったら単純な道を選びます。

## 2. 探索する（複雑な場合のみ）

問いを 2〜4 の切り口に分解します。それぞれがサブシステムの異なる一面です。探索役をすべて 1 つのメッセージで立ち上げ、それぞれに `references/explorer-prompt.md` と担当の切り口を埋め込みます。

## 3. 統合する（複雑な場合のみ）

探索役がすべて戻ったら、`references/explainer-prompt.md` に全探索役の所見を埋め込んだ説明役を 1 つ立ち上げます。

## 4. 提示する

説明役の出力を提示します。明瞭さのための軽い編集や、会話から得た文脈の補足は構いません。大幅な書き直しはしません。

## 出力形式

説明は `references/explainer-prompt.md` で定義されたセクションを使い、当てはまらないものは落とします。Overview、Key Concepts、How It Works、Where Things Live、Gotchas です。
