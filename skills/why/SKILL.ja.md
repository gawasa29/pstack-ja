---
name: why
description: "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Discovers available MCPs and queries each evidence category (source control, issue tracker, long-form docs, real-time chat, infrastructure observability, error tracking, product analytics warehouse) in parallel, then returns a cited read on decisions and tradeoffs. Use how for runtime behavior."
disable-model-invocation: true
---

# なぜ（Why）

コードの背後にある動機と意図を調べます。対になる `how` スキルは、コードが何をしてどう動くかに答えます。`why` は、どんな力がその形を生んだかに答えます。

以下の各起動は、`pstack-models.mdc` ルールの役割の行と既定値を名指しします。`model` はその行の値にし、ルールか行がなければ既定値にします。値が `auto` か `inherit-parent` のときは `model` を未設定にします。Task ツールがスラッグを拒否したら、既定値を使い、そう言います。既定値も拒否したら、そのエラーメッセージから、同じファミリで最も近い有効なスラッグを使います。各サブエージェントの推論の段と、fast か標準かの速度は、**poteto-mode** スキルのサブエージェントのセクションに従って、仕事に合わせて選びます。

どの起動も `generalPurpose` で `readonly: false`（エージェントモード）です。**readonly / Ask モードは使わないでください。** MCP へのアクセスがはがされ、MCP に支えられた調査担当と、統合担当の引用の抜き取り確認が無効になります。調査担当はそれでも何も書くべきではありません。

## 作業の構え

**慎重で、用心深く、正確な調査担当**として動きます。自分が知っていることと推測していることを正直に分けます。信頼度の枠組みと表現のガイドの全体は `references/epistemics.md` を読んでください。統合担当はそれに従わなければなりません。

## ステップ 1. 対象と問いを理解する

**対象**はふつう、コードの一まとまり、パターン、機能、名前の付いた設計判断です。**問い**はふつう、設計の根拠、トレードオフ、動機になったエッジケース、外部の制約、死んだコード、広い履歴の調査です。

対象が曖昧なとき（"why do we do it this way?" に明確な指示対象がない）は、会話の文脈（開いているファイル、最近の編集、カーソル位置、直前に話していたこと）から最善の推測をします。解釈を短く述べて、外れていればユーザーが方向を直せるようにしてから、進みます。

## ステップ 2. コードのアンカーを確立する

調査担当を起動する前に、種になる文脈をインラインで組み立てます。ファイルのパスと行範囲、主要なシンボル（関数、クラス、定数）、対象に触れた直近のコミット、マージコミットから取った PR 番号（件名の `(#1234)` パターン）、リンクされたチケット ID です。最後に触れたコミットには `git blame -L <start>,<end> <file>`、名前変更をまたぐパッチ付きの全履歴には `git log --follow -p -- <file>`、PR 番号が見える直近のコミットには `git log --oneline -20 -- <file>`、PR 番号の抽出には `git log -1 --format=%B <commit>` を実行します。続いて、実質的なコミットがあれば、PR の本文と議論を取ります: `gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews`。このアンカーは、すべての調査担当と統合担当に渡します。

## ステップ 3. 調査担当を並列に起動する

**既定は完全な並列調査です。** 目指すのは完全なカバレッジマップで、最小のものではありません。該当なしも記録し、検索を飛ばしません。

### 発見

調査担当を起動する前に、Cursor 環境で使える MCP を列挙します。使えるツールのマップがあればそれを使います。なければ、Cursor が有効な MCP サーバ向けに公開している `mcps/` ディレクトリを調べます。

使える各 MCP を、証拠のカテゴリの 1 つに対応づけます。

1. ソース管理の履歴
2. 課題 / チケットトラッカー
3. 長文ドキュメント
4. リアルタイムのチームチャット
5. インフラの可観測性
6. エラー / 例外のトラッキング
7. プロダクト分析のウェアハウス

ソース管理は git と `gh` を通じて常に使えます。他の 6 つは、MCP の名前、サーバの指示、ツール名、リソースの記述子で分類します。MCP が複数のカテゴリに当てはまりうるときは、主たる証拠に合うほうを選びます。曖昧なケースはカバレッジマップに記録します。

対応する MCP があるカテゴリごとに調査担当を 1 体、すべて 1 つのメッセージで起動して同時に走らせます。各調査担当はちょうど 1 つのツールか MCP を持ちます。1 体のエージェントに複数の MCP を担当させないでください。`model`: `why investigators` の行、既定は `grok-4.7-xhigh-fast`。

各調査担当のプロンプトは、`references/investigator-prompt.md` を埋めたものに、次を加えたものです。
- 選んだ MCP のカテゴリのプレイブック `references/sources/<source>.md`（`references/source-playbook.md` の例から適応したもの）
- 対象のコードが防衛的に見えるなら `references/sources/incident-postmortem.md`（null チェック、リトライ、タイムアウト処理、レート制限、機能フラグ、外向き通信のガード、OOM ハンドラ）
- コードのアンカーと、ユーザーの元の問い

### 調査担当の名簿、使える証拠カテゴリごとに 1 体

下の各カテゴリは、「Best at」のあとに示す「why」の 1 つの形を浮かび上がらせるのに独特の位置にあります。何が返ってくるかを知るため、カテゴリが空を返したときに欠落を名指しするため、そして証明可能に無関係なまれな場合にだけ飛ばす理由に使います。

1. **ソース管理**（git 履歴、PR には `gh`、コードのコメント、テスト）。常に起動します。唯一保証された情報源です。*レビュー中に記録された実装時の根拠*が得意です。
2. **課題 / チケットトラッカー**（例: Linear、Jira、GitHub Issues、Plane、Shortcut の MCP）。*プロダクトやビジネスの推進力*が得意です。why がエンジニアリングの外にあるときに最も強いです。
3. **長文ドキュメント**（例: Notion、Confluence、Google Docs、Coda の MCP）。*コードになる前に書き出された、長文の設計根拠*が得意です。
4. **リアルタイムのチームチャット**（例: Slack、Discord、Microsoft Teams、Mattermost の MCP）。*ドキュメントに残らなかったリアルタイムの議論*が得意です。ソース管理、チケット、ドキュメントの記録が薄いときに特に重要です。
5. **インフラの可観測性**（例: Datadog、New Relic、Honeycomb、Grafana、Splunk の MCP）。*コードの動機になったインフラと実行時の現実*が得意です。対象がインフラのシグナル（タイムアウト、リトライ、レート制限、サーキットブレーカー）に反応するときに最も強いです。
6. **エラー / 例外のトラッキング**（例: Sentry、Rollbar、Bugsnag、Airbrake の MCP）。*防衛的・訂正的なコードの動機になった具体的な例外とエラーの軌跡*が得意です。catch ブロック、null ガード、型チェック、リトライなどの防御に最も強いです。
7. **プロダクト分析のウェアハウス**（例: Databricks、Snowflake、BigQuery、ClickHouse、dbt、Redshift の MCP）。*コードを形づくったプロダクトとデータの現実*が得意です。フラグで制御されたコード、実験に基づく出荷、データ移行、"where did this number come from" の問いに最も強いです。

### 調査担当を飛ばすとき

**明示的で書かれた正当化**があり、それが最終的な調査したソースに入るときだけです。有効な理由は 2 つです。

- **そのカテゴリに使える MCP がこの環境にない**。これは選択ではなく欠落として示します: "Real-time team chat skipped. No matching MCP available, so the conversational record was not searchable."
- **情報源が証明可能に無関係である**。「たぶん無関係」では足りません。高い基準です: "Error / exception tracking skipped. Target is a build-time script with no runtime code path."

範囲の評価から、PR の説明に完全な答えがすでにある 1 コミットの些細な対象だと分かっても、7 つすべての使えるカテゴリの検索が冗長だと確認した**後でだけ**、インラインで答えてよいです。そう明言します。これはまれであるべきです。

## ステップ 4. 統合する

統合担当を 1 体起動します。`model`: `why synthesizer` の行、既定は `claude-opus-5-5-xhigh`。渡すものは次のとおりです。
1. 調査担当の発見。該当なしの結果と、正当化付きで飛ばしたカテゴリを含みます
2. コードのアンカー
3. ユーザーの元の問い
4. `references/epistemics.md` の信頼度の枠組み
5. `references/synthesizer-prompt.md` の統合担当のプロンプトテンプレート

## ステップ 5. 提示する

統合担当の出力をユーザーに提示します。明瞭さのために軽く編集したり、会話から文脈を足したりしてよいですが、**信頼度の言葉は書き換えないでください**。

## 出力の形

構造は `references/synthesizer-prompt.md` にあるものと同じです。問い、対象のコード、わかったこと、合理的に推論できること、競合する仮説、わかっていないこと、調査したソース、信頼度のまとめ。必要に応じて適応してよいですが、信頼度の分離は保ち、調査したソースは調査担当ごとに 1 行、何も返さなかったものや飛ばしたものも理由付きで含めます。

調査したソースのあと、ユーザーの `why` の問いがこのコードを変える前触れなら、系譜の発見を、変更を計画するための Preserve / Change / Avoid / Risk の制約セットに変えます。

## 避けるべきよくある失敗

- **直近性バイアス**。最も新しいコミットが権威だと決めつけること。今の形は、多くの以前の判断が積み重なった結果であることがよくあります。遡ってください。
