# benny

benny は、Slack の不具合報告向けに 2 つの Cursor オートメーションを提供します。1 つが各報告をトリアージし、もう 1 つが確認済みの不具合を再現し、小さな修正のドラフトを用意することがあります。

このディレクトリのファイルは、休眠状態のセットアップとオートメーションのソースです。スラッシュスキルとしては表示されません。

## セットアップ

1. Cursor に [`FOR_AGENTS.md`](FOR_AGENTS.ja.md) を指定し、対象リポジトリを名指しする。
2. セットアップに、このディレクトリ全体を対象リポジトリの `.cursor/automations/benny/` へマージさせる。宛先にしかないファイルを保ち、ローカルの編集を上書きするのではなく、コンフリクトをレビューする必要がある。
3. セットアップに、共有の依存のために、対象リポジトリの `.cursor/settings.json` で pstack を有効にさせる:

```json
{
	"plugins": {
		"pstack": { "enabled": true }
	}
}
```

4. ユーザーが所有する設定は、コピーしたパックの外（たとえば `.cursor/benny/`）に置く。[`configuration.example.yaml`](./templates/configuration.example.yaml) と [`feature-map.example.md`](skills/reproduce-and-fix-issues/references/feature-map.example.ja.md) を自分の環境に合わせる。
5. どちらかのオートメーションを有効にする前に、`.cursor/settings.json`、`.cursor/automations/benny/`、秘密を含まない設定をコミットする。
6. 新しいオートメーションのドラフトをそれぞれレビューするか、既存のオートメーションをエディタで更新する。そのうえで無害なテスト報告を送り、ソースチャンネルへの各投稿が元のスレッドに留まることを確認する。
