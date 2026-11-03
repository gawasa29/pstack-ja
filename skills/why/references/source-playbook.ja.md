# ソースのプレイブック

why スキルは、利用できる証拠カテゴリごとに調査担当（investigator）を 1 つ起動し、それぞれが下のソース固有のプレイブックを 1 つ読みます。プレイブックは、よく使われる MCP の具体的な例です。同じカテゴリの別の MCP に合わせて読み替えてください。

| カテゴリ | プレイブック | 解説している MCP の例 |
|---|---|---|
| ソース管理の履歴 | [`code-archaeology.md`](sources/code-archaeology.ja.md) | git、`gh` |
| 課題 / チケットトラッカー | [`linear.md`](sources/linear.ja.md) | Linear（Jira、GitHub Issues、Plane、Shortcut 向けに読み替え） |
| 長文ドキュメント | [`notion.md`](sources/notion.ja.md) | Notion（Confluence、Google Docs、Coda 向けに読み替え） |
| リアルタイムのチームチャット | [`slack.md`](sources/slack.ja.md) | Slack（Discord、Microsoft Teams、Mattermost 向けに読み替え） |
| インフラの可観測性 | [`datadog.md`](sources/datadog.ja.md) | Datadog（New Relic、Honeycomb、Grafana、Splunk 向けに読み替え） |
| エラー / 例外トラッキング | [`sentry.md`](sources/sentry.ja.md) | Sentry（Rollbar、Bugsnag、Airbrake 向けに読み替え） |
| プロダクト分析のウェアハウス | [`databricks.md`](sources/databricks.ja.md) | Databricks SQL（Snowflake、BigQuery、ClickHouse、dbt 向けに読み替え） |

横断的なもの:

- [`incident-postmortem.md`](sources/incident-postmortem.ja.md)。対象のコードが防御的に見える場合（null チェック、リトライ、タイムアウト、レート制限、フィーチャーフラグ、egress ガード、OOM ハンドラ）に追加してください。
