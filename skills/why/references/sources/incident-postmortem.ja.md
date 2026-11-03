# インシデントとポストモーテムの文脈

- **Linear**: `incident`、`sev-*`、`postmortem-action-item`、`reliability` のラベルが付いたチケットを探してください。
- **Slack**: 対象のコードが追加された日付の前後で `#sev-*` と `#incident-*` のチャンネルを検索してください。
- **Git**: 「fix for incident」「add defensive check」のようなメッセージや、「revert」のあとに「re-apply with...」が続くコミットは、強いシグナルです。
