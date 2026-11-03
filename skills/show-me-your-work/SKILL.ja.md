---
name: show-me-your-work
description: "Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, result). Local by default; commit it when a reviewer needs the trail to trust the result. Use for /show-me-your-work, autonomous or multi-phase runs, or work a human reviews after stepping away."
disable-model-invocation: true
---

# 自分の仕事を見せる（Show me your work）

正典となるログを 1 つだけ保ちます。

## 形式

TSV ファイル 1 つに、1 判断 1 行で記録します。セルは 1 行に収めます。証拠（evidence）はポインタであり、文章ではありません。

`references/decision-log-template.tsv`（ヘッダー行）をコピーして、まっさらなログを始めます。列は次のとおりです。

- **ts.** ISO8601 のタイムスタンプ。
- **phase.** フェーズまたはワークストリーム。
- **decision.** 何を選び、何を行ったか。1 行で。
- **why.** 理由を平易な言葉で。原則が動機なら、専門用語のタグではなく、そのままの言葉で書きます。
- **evidence.** それを裏づけるリンクまたはパス。コミット SHA、PR 番号、`file:line`、あるいは成果物・トレース・スクリーンショットのパス。文章で書くことは決してありません。
- **result.** 結果、または述語の状態。`tests green`、`reverted`、`pixel-diff 0`、`INCONCLUSIVE`、`open`。

例です。レビュアーがひと目で読めるよう、平易な言葉で書いています。

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## 行を記録する

各行は、同僚に自分のやったことを話すときと同じように書きます。平易な言葉、具体的な行動、AI っぽい言い回しや抽象的な専門用語は使いません（**unslop** スキルはログの文章にも当てはまります）。

ヘルパー `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>` を使います。これは `ts` を刻み、初回にヘッダーを書き、紛れ込んだタブや改行を取り除き、`=`、`+`、`-`、`@` で始まるセルの先頭にシングルクォートを付けます。`printf` でそのまま行を追記しても動きますが、セルが生成されたテキストやユーザー提供のテキストに由来する場合は、同じバイトに気を付けてください。

すべての行動ではなく、判断点とチェックポイントを記録します。選んだ分岐、検証結果とともに完了したユニット、きっかけとともに残す方針転換や取り消し、表面化したブロッカー、修正したゲートです。ループの実行では、1 イテレーションにつき 1 行です。些細なこと、自明なことは省きます。

実行（run）とは、エージェントの会話 1 つ分のことで、その後のターンやその会話の要約も含みます。引き継ぎ、エージェントの差し替え、新しいチャットは、新しい実行の開始です。ある実行が、すでに行のあるログに追記するとき、その最初の行の phase は `start` です。別の実行の `start` 行のあとに来る、この実行の最初の行も同じです。そのため、後のターンでログに戻ってくる実行は、まずログの末尾の行を読み、その間に別の実行が書いていないかを確かめます。`start` 行には、その手前にある行のうち、この実行が書いていない行の `ts` 範囲を記します。evidence には、この実行を指すもの（エージェント id など）を記します。phase の `start` は、それ以外の用途には使いません。

## 置き場所

既定では、ログは作業用の成果物であり、コミットしません。作業ディレクトリの `decisions.tsv` に置きます。複数の作業が同時に走るときは `.audit/<task-slug>.tsv` に置き、git には含めません。

コミットするのは、レビュアーが結果を信頼するために証跡（trail）を必要とするほど、作業が野心的なときだけです。

## ルール

- 追記のみです。誤った判断には、それを上書きする新しい行を足します。履歴を編集したり削除したりすることは決してありません。
- 手作りの一回限りのものより、コミットされたスクリプトが生み出した証拠を優先します（**encode-lessons-in-structure** 原則スキル）。

## ログをトランスクリプトと突き合わせて監査する

実行の終わりに、結果を返す前に、ログが真実を語っているかを確かめます。アクティブなワークスペースの `agent-transcripts/` ディレクトリにある、この実行のトランスクリプトを読みます（パスはシステムプロンプトに書かれています）。`~/.cursor/projects/*/` を横断して glob してはいけません。無関係なプライベートチャットを読むことになります。この実行の行を、実際に起きたことと照らし合わせて 1 行ずつたどります。この実行の行の連なりは、この実行の `start` 行、あるいはこの実行がログを作った場合は先頭行から始まり、別の実行の次の `start` 行で終わります。

- すべての行が、実際の判断や行動に対応しているかを確かめます。
- 各行の証拠が解決でき、その行の主張を示しているかを確かめます。
- 作業の形を決めたのに記録されていない分岐、方針転換、捨てたアプローチは欠落です。追加します。

直すのはログであって、物語ではありません。監査は、でっち上げられた行であっても、行を編集したり削除したりすることは決してありません。ある行が実際の判断も行動も記録していない場合、あるいはその主張や証拠が誤っている場合は、実際に起きたことと、解決できるポインタを添えた、上書き用の新しい行を足します。この監査は、この実行の連なりの外にある行は確認しません。この実行の作業そのものが、それらの行の 1 つを誤りだと示したなら、他の誤った判断と同様に上書きします。

## 証跡のクロスモデルレビュー

結果を返す前に、作業を行ったモデルとは別のモデルファミリーのサブエージェントを起動します。自己レビューでは代わりになりません。サブエージェントは監査証跡と実行のトランスクリプトを読み、ユーザーが注意を払うべき点を指摘します。作業のやり直しではなく、最適でない点や危険な点の走査です。サブエージェントごとの推論レベルと、fast か standard かの速度は、**poteto-mode** スキルの Subagents セクションに従い、作業に合わせて選びます。

- 証拠が弱い、あるいは欠けている判断。
- 飛ばされた検証手順、またはトランスクリプトに裏づけなく主張された検証手順。
- 振り返ると危険に見える選択（早すぎる、スコープを広げすぎる、症状を覆い隠す）。
- ユーザーが流し読みでは見落とすであろう欠落。

証跡を生んだ実行では、どの返信も "Attention" セクションで終わります。まずレビュアーのモデルを単独の行に置き（`reviewed by <model>`）、次に各指摘を、特定の行や場面を指しながら並べます。"No flags" は有効な値です。モデル名は有効な値ではありません。

## 証跡をレビューする

上から下へ読み、証拠のポインタをたどり、抜き取りで確認します。コミットされた TSV は GitHub が表として表示します。`column -s$'\t' -t decisions.tsv` でターミナルに表示できます。

## このスキルの組み込み方

他のスキルは、自前の監査証跡を発明するのではなく、ここに流します。名前で参照し、形式はこのスキルに任せます。列を書き直してはいけません。
