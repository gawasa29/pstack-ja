---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
disable-model-invocation: true
---

# 振り返る（Reflect）

現在の会話から長く残る学びを掘り出し、それをスキルの編集へと振り分けます。

ユーザーが「reflect」または「/reflect」と言ったときに呼び出します。会話が些細なとき、話がそれているとき、あるいは親が正しく従った既存のスキルで既にカバーされているときは飛ばします。一度きりの出来事は学びではありません。

## 1. アクティブなトランスクリプトを特定する

展開する前に、システムプロンプトが示す `agent-transcripts/` ディレクトリで、この会話のトランスクリプトを見つけます。`~/.cursor/projects/*/` を横断して glob してはいけません。ワークスペースの境界を越え、無関係なプロジェクトのプライベートチャットを読むことになります。

```bash
ls -t <agent-transcripts>/*.jsonl <agent-transcripts>/*/*.jsonl <agent-transcripts>/*/subagents/*.jsonl 2>/dev/null | head -10
```

これは、旧来のフラットな配置（`<id>.jsonl`）、現在のネストした配置（`<id>/<id>.jsonl`）、サブエージェントの配置（`<parent>/subagents/<child>.jsonl`）をカバーします。候補ごとに、JSONL の最初の行を読みます。`message.content[0].text` にその会話の冒頭のユーザープロンプトを含むファイルを選びます。どれも一致しなければ、代わりにセッションの簡潔なダイジェストを渡します。

## 2. 3 人のレビュアーを並行して起動する

1 つのメッセージで 3 つの `Task` 呼び出しを行います。`subagent_type: generalPurpose`、エージェントモード（`readonly: false`）です。レビュアーは、トランスクリプトが参照するチケット、チャットスレッド、オブザーバビリティのトレースを調べるために MCP へのアクセスを必要とし、readonly は MCP を剥ぎ取ります。

各レビュアーと統合役には、`pstack-models.mdc` ルールのロール行と既定値が対応します。`model` にはその行の値を設定します。ルールや行が無ければ既定値を設定します。値が `auto` か `inherit-parent` のときは `model` を未設定のままにします。Task ツールがスラッグを拒否したら、既定値を使い、そのことを伝えます。既定値も拒否したら、そのエラーメッセージから、同じファミリーで最も近い有効なスラッグを使います。サブエージェントごとの推論レベルと、fast か standard かの速度は、**poteto-mode** スキルの Subagents セクションに従い、作業に合わせて選びます。

| レンズ | ロール行 | 既定の `model` | プロンプトテンプレート |
|---|---|---|---|
| 判断 | `reflect judgment, divergent, synthesizer` | `claude-opus-5-5-xhigh` | `references/judgment-reviewer.md` |
| ツーリング | `reflect tooling` | `grok-4.7-xhigh-fast` | `references/tooling-reviewer.md` |
| 発散 | `reflect judgment, divergent, synthesizer` | `claude-opus-5-5-xhigh` | `references/divergent-reviewer.md` |

各テンプレートは、印の付いた箇所をトランスクリプトのパスやダイジェストで置き換えて、そのまま渡します。レビュアーは `Task` の応答本文で所見を返します。

## 3. 統合する

`Task` を 1 回呼び出します。`subagent_type: generalPurpose`、`model` は `reflect judgment, divergent, synthesizer` 行の値（既定は `claude-opus-5-5-xhigh`）、エージェントモード（`readonly: false`）です。MCP 経由で引用を抜き取り検証するので、readonly では MCP が剥ぎ取られます。`references/synthesizer.md` は、印の箇所に各レビュアーの出力全文を埋め込んで、そのまま渡します。Accepted / Rejected / Backlog のリストを返します。

## 4. 構造による強制の確認

lint ルール、スクリプト、メタデータのフラグ、実行時のチェックのほうが確実に強制できる Accepted の項目は、Backlog に移します。**encode-lessons-in-structure** 原則スキルを参照してください。

## 5. 適用する

統合役の Accepted / Rejected / Backlog の出力をすべて提示し、Accepted の編集を適用する前に、明示的な承認を待ちます。ユーザーが部分集合を選び、振り分け先を変えることもあります。スキルの変更は、組織内の将来のすべてのエージェントに影響します。自動適用してはいけません。

Backlog の各項目は、待たずにチームの devex トラッカーまたはバックログトラッカーに起票します。承認を待つのは Accepted のリストだけです。

`plugins/cache/` 配下のスキルを編集することは決してありません。承認の前に、その宛先（`.cursor/skills/<skill>/` または `~/.cursor/skills/<skill>/`）を示します。承認後、スキルのフォルダをそこにコピーし、コピーのほうを編集します。PR を開くことも push することも決してありません。

承認された各行の Routing には、そのとおり従います。

- 些細な既存スキルの編集（1 行の箇条書き、引き締めた 1 文、古くなった事実の修正）は、親が直接行います。
- 実質的な既存スキルの編集（新しいセクション、新しいパターン表、およそ 10 行超）は、Cursor 組み込みの `create-skill` スキルに渡し、その draft / test / iterate のループを回します。
- `tune description: <skill path>`（スキルはあるのに、発火すべきときに発火しなかった場合）は、`create-skill` に渡し、その description 最適化ループを回します。
- `new skill via create-skill: <kebab-name>` は、作成を `create-skill` に渡します。形をその場で勝手に作ってはいけません。

環境に SKILL.md のバリデータがあれば、完了を宣言する前に、触れたすべてのスキルに対して実行します。

## 6. ユーザーに要約する

前置きなしの短いリストです。

- 適用した編集: `<skill path>`。何が変わったかを 1 行ずつ。
- 作成した新しいスキル: `<skill path>`。1 行ずつ（まれ）。
- devex トラッカーに起票した Backlog: `<issue title>`（`<tags>`）。1 行ずつ。
- 却下: 統合役が却下した所見ごとに、その理由を 1 行ずつ。
